use std::collections::HashMap;
use std::fs;
use std::time::Instant;

struct DigitsMatcher {
    mapping: HashMap<String, i32>,
}

fn match_digit(s: &str, i: usize, reverse: bool, digits_matcher: &DigitsMatcher) -> Option<i32> {
    if let Ok(x) = &s[i..i + 1].parse::<i32>() {
        return Some(*x);
    }
    let mapping = &digits_matcher.mapping;
    for (key, value) in mapping {
        let start = if reverse {
            if key.len() > i {
                0
            } else {
                i + 1 - key.len()
            }
        } else {
            i
        };
        let end = if reverse { i + 1 } else { i + key.len() };
        if let Some(sub_s) = s.get(start..end) {
            if sub_s.eq(key) {
                return Some(*value);
            }
        }
    }
    None
}

fn main() {
    let start_time = Instant::now();
    let path = std::env::current_dir().expect("Cannot get current dir.");
    let path = path.join("src/bin/aoc1/in.txt");
    let file = fs::read_to_string(path).expect("Cannot read input file.");

    let mapping = HashMap::from([
        (String::from("one"), 1),
        (String::from("two"), 2),
        (String::from("three"), 3),
        (String::from("four"), 4),
        (String::from("five"), 5),
        (String::from("six"), 6),
        (String::from("seven"), 7),
        (String::from("eight"), 8),
        (String::from("nine"), 9),
    ]);

    let mut sum: i32 = 0;

    let mut reverse_mapping = HashMap::new();
    for (key, value) in &mapping {
        reverse_mapping.insert(key.chars().rev().collect::<String>(), *value);
    }

    let digits_matcher = DigitsMatcher { mapping };

    for line in file.lines() {
        let mut two_digit_str = String::new();

        // First digit
        for i in 0..line.len() {
            if let Some(x) = match_digit(line, i, false, &digits_matcher) {
                two_digit_str.push_str(&x.to_string());
                break;
            }
        }

        // Last digit
        for i in (0..line.len()).rev() {
            if let Some(x) = match_digit(line, i, true, &digits_matcher) {
                two_digit_str.push_str(&x.to_string());
                break;
            }
        }
        let two_digit: i32 = two_digit_str.parse().unwrap();
        sum += two_digit;
    }

    println!("sum={}", sum);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );
}
