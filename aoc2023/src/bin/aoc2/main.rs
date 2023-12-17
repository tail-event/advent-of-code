use std::{collections::HashMap, time::Instant};

#[derive(Debug)]
struct Game {
    // Maps a colored cube to its count
    cubes_extracted: Vec<HashMap<String, i32>>,
    id: i32,
}

impl Game {
    fn is_valid(&self, cubes_in_bag: &HashMap<&str, i32>) -> bool {
        for extraction in &self.cubes_extracted {
            for (color, count) in extraction {
                let count_in_bag = cubes_in_bag.get(color.as_str()).unwrap();
                if count > count_in_bag {
                    return false;
                }
            }
        }
        true
    }

    fn get_power(&self) -> i32 {
        let mut color_to_fewest_count: HashMap<&str, i32> = HashMap::new();
        for extraction in &self.cubes_extracted {
            for (color, count) in extraction {
                let entry = color_to_fewest_count.entry(color).or_insert(0);
                *entry = std::cmp::max(*entry, *count);
            }
        }
        color_to_fewest_count.values().product()
    }
}

fn parse_games(input_content: &str) -> Result<Vec<Game>, Box<dyn std::error::Error>> {
    let mut games: Vec<Game> = Vec::new();

    for line in input_content.lines() {
        let line_split: Vec<_> = line.split(':').map(str::trim).collect();
        let game = line_split[0];
        let game: i32 = game.split(' ').collect::<Vec<_>>()[1].parse()?;
        let extractions: Vec<_> = line_split[1].split(';').map(str::trim).collect();
        let mut cubes_extracted: Vec<HashMap<String, i32>> = Vec::new();

        for extraction in extractions {
            let mut cubes_extraction: HashMap<String, i32> = HashMap::new();
            extraction.split(',').map(str::trim).for_each(|el| {
                let count_color = el.split(' ').collect::<Vec<_>>();
                cubes_extraction.insert(
                    String::from(count_color[1]),
                    count_color[0].parse().unwrap(),
                );
            });
            cubes_extracted.push(cubes_extraction);
        }

        games.push(Game {
            cubes_extracted,
            id: game,
        });
    }
    Ok(games)
}

fn first_part_solution(games: &[Game]) -> i32 {
    let cubes_in_bag = HashMap::from([("red", 12), ("green", 13), ("blue", 14)]);
    games
        .iter()
        .filter(|game| game.is_valid(&cubes_in_bag))
        .map(|game| game.id)
        .sum()
}

fn second_part_solution(games: &[Game]) -> i32 {
    games.iter().map(|game| game.get_power()).sum()
}

fn main() {
    let start_time = Instant::now();
    let path = std::env::current_dir().expect("Cannot get current path.");
    let path = path.join("src/bin/aoc2/in.txt");
    let file = std::fs::read_to_string(path).expect("Cannot read input file.");

    let games = parse_games(&file).expect("Cannot parse games.");
    let first_sol = first_part_solution(&games);
    println!("First sum={}", first_sol);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );

    let first_sol = second_part_solution(&games);
    println!("Second sum={}", first_sol);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );
}
