use std::time::Instant;

fn main() {
    let start_time = Instant::now();
    let path = std::env::current_dir().expect("Cannot get current dir.");
    let file = path.join("src/bin/aoc9/in.txt");
    let file = std::fs::read_to_string(file).expect("Cannot read input file.");

    let sequences = file
        .lines()
        .map(|line| {
            line.split(' ')
                .map(|num_s| num_s.parse::<i32>().unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let mut first_part_res = 0;
    let mut second_part_res = 0;

    sequences.iter().for_each(|seq| {
        let mut reduced_sequences: Vec<Vec<i32>> = Vec::new();
        let mut curr: Vec<i32> = seq.clone();
        let mut seq_prediction: i32 = 0;
        loop {
            reduced_sequences.push(curr.clone());
            seq_prediction += curr.last().unwrap();
            curr = curr.windows(2).map(|window| window[1] - window[0]).collect();
            if curr.iter().all(|&x| x==0) {
                break;
            }
        }
        first_part_res += seq_prediction;

        let mut backward = 0;
        for rev_seq in reduced_sequences.iter().rev() {
            let first_rev_seq_elem = *rev_seq.first().unwrap();
            backward = first_rev_seq_elem - backward;
        }
        second_part_res += backward;

    });

    println!("First part solution = {}", first_part_res);
    println!("Second part solution = {}", second_part_res);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );
}
