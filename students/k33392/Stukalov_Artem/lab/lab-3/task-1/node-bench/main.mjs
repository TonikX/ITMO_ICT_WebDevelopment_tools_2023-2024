import { Worker } from 'worker_threads'

const runWorker = (data) =>
  new Promise((resolve, reject) => {
    const worker = new Worker('./worker.mjs', { workerData: data })
    worker.on('message', resolve)
    worker.on('error', reject)
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`))
    })
  })

const splitRanges = (start, end, count) => {
  const res = []
  const step = Math.floor((end - start + 1) / count)
  for (let i = 1; i <= count; i++) {
    const left = start + step * (i - 1) + (i !== 1 ? 1 : 0)
    const right = i === count ? end : start + step * i
    res.push([left, right])
  }

  return res
}

const TARGET = 100_000_000
const SPLIT_COUNT = 20

async function main() {
  const ranges = splitRanges(1, TARGET, SPLIT_COUNT)
  await Promise.all(ranges.map((range) => runWorker(range)))
}

main().catch((err) => console.error(err))
