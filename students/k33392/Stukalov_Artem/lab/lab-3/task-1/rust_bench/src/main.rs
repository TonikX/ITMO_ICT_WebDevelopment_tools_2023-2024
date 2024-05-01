use std::thread::{self, available_parallelism};

fn get_ranges(start: u64, end: u64, count: u64) -> Vec<(u64, u64)> {
  let step = (end - start + 1) / count;
  (1..=count)
    .map(|i| {
      let mut left = start + step * (i - 1);
      if i != 1 {
        left += 1
      }

      if i == count {
        return (left, end);
      }

      (left, start + step * i)
    })
    .collect()
}

fn sum_range(start: u64, end: u64) -> u64 {
  (start..=end).sum()
}

fn main() {
  let target = 100_000_000_000;
  let split_count = available_parallelism().unwrap().get() as u64;
  let ranges = get_ranges(1, target, split_count);

  let threads: Vec<_> = ranges
    .iter()
    .map(|range| {
      let start = range.0;
      let end = range.1;
      thread::spawn(move || sum_range(start, end))
    })
    .collect();

  for thread in threads {
    thread.join().unwrap();
  }
}
