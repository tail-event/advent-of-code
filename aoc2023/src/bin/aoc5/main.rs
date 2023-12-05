use std::time::Instant;

#[derive(Debug)]
struct Interval {
    source: u64,
    dest: u64,
    range: u64,
}

impl Interval {
    fn contains(&self, x: u64) -> bool {
        x >= self.source && x <= self.source + self.range
    }

    fn get_target(&self, x: u64) -> Option<u64> {
        if self.contains(x) {
            let diff = x - self.source;
            return Some(self.dest + diff);
        }
        None
    }
}

#[derive(Debug)]
struct Mapping {
    intervals: Vec<Interval>,
}

impl Mapping {
    fn get_target(&self, x: u64) -> u64 {
        for interval in &self.intervals {
            if let Some(target) = interval.get_target(x) {
                return target;
            }
        }
        x
    }
}

fn first_part_solution(seeds: &[u64], cascade_maps: &Vec<Mapping>) -> u64 {
    let mut lowest_num: u64 = u64::MAX;
    for &seed in seeds {
        let mut curr = seed;
        for map in cascade_maps {
            curr = map.get_target(curr);
        }

        lowest_num = std::cmp::min(curr, lowest_num);
    }
    lowest_num
}

fn second_part_solution(seeds: &[u64], ranges: &[u64], cascade_maps: &Vec<Mapping>) -> u64 {
    let mut lowest_num: u64 = u64::MAX;
    for (&start, &range) in seeds.iter().zip(ranges).collect::<Vec<_>>() {
        for i in 0..=range {
            let mut curr = start + i;
            for map in cascade_maps {
                curr = map.get_target(curr);
            }
            lowest_num = std::cmp::min(curr, lowest_num);
        }
    }
    lowest_num
}

fn main() {
    let start_time = Instant::now();
    let path = std::env::current_dir().expect("Cannot get current dir.");
    let path = path.join("src/bin/aoc5/in.txt");
    let file = std::fs::read_to_string(path).expect("Cannot read input file");

    let seeds_and_blocks = file.split("\n\n").collect::<Vec<_>>();
    let seeds = seeds_and_blocks
        .first()
        .unwrap()
        .split(": ")
        .collect::<Vec<_>>();
    let seeds = seeds.get(1).unwrap().split(' ').collect::<Vec<_>>();

    let seeds = seeds
        .iter()
        .map(|x| x.parse().unwrap())
        .collect::<Vec<u64>>();

    let mut cascade_maps: Vec<Mapping> = Vec::new();
    for &block in seeds_and_blocks.iter().skip(1) {
        let mut intervals: Vec<Interval> = Vec::new();
        for line in block.lines().skip(1) {
            let nums = line
                .split(' ')
                .map(|x| x.parse().unwrap())
                .collect::<Vec<u64>>();
            intervals.push(Interval {
                source: nums[1],
                dest: nums[0],
                range: nums[2],
            });
        }

        cascade_maps.push(Mapping { intervals });
    }

    println!(
        "first part solution = {}",
        first_part_solution(&seeds, &cascade_maps)
    );
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );

    let seeds_wo_ranges: Vec<u64> = seeds.iter().step_by(2).copied().collect::<Vec<_>>();
    let ranges: Vec<u64> = seeds.iter().skip(1).step_by(2).copied().collect::<Vec<_>>();
    let second_part_solution = second_part_solution(&seeds_wo_ranges, &ranges, &cascade_maps);

    println!("second part solution = {}", second_part_solution);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );
}
