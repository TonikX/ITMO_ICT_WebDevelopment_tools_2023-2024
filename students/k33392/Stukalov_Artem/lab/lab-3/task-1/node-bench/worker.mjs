import { workerData, parentPort } from 'worker_threads'

const sumRange = (start, end) => {
  let res = 0
  for (let x = start; x <= end; x++) {
    res += x
  }
  return res
}

const sum = sumRange(workerData[0], workerData[1])
parentPort.postMessage(sum)
