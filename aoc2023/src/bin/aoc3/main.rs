use std::collections::{HashMap, HashSet};
use std::fmt::Display;
use std::time::Instant;

#[derive(Debug)]
struct GridNumber {
    digits: Vec<char>,
    near_symbols: HashSet<(usize, usize)>,
}

impl GridNumber {
    fn new() -> Self {
        Self { digits: Vec::new(), near_symbols: HashSet::new() }
    }
    fn add_digit(&mut self, char: char) {
        self.digits.push(char)
    }
    fn add_near_symbol(&mut self, symbol_pos: (usize, usize)) {
        self.near_symbols.insert(symbol_pos);
    }
    fn num(&self) -> i32 {
        self.digits.iter().collect::<String>().parse().unwrap()
    }
    fn is_part_number(&self) -> bool {
        !self.near_symbols.is_empty()
    }
}

struct Grid {
    grid: Vec<Vec<char>>,
}

impl Grid {
    fn is_cell_digit(&self, i: usize, j: usize) -> bool {
        self.grid[i][j].is_ascii_digit()
    }

    fn is_cell_dot(&self, i: usize, j: usize) -> bool {
        self.grid[i][j] == '.'
    }

    fn is_cell_special(&self, i: usize, j: usize) -> bool {
        !self.is_cell_digit(i, j) && !self.is_cell_dot(i, j)
    }

    fn get_symbol_near_cell(&self, i: usize, j: usize) -> Option<(usize, usize)> {
        let deltas: [(i32, i32); 8] = [
            (0, 1),
            (0, -1),
            (1, 0),
            (1, 1),
            (1, -1),
            (-1, 0),
            (-1, 1),
            (-1, -1),
        ];

        for (delta_i, delta_j) in &deltas {
            if (i as i32) + delta_i > 0
                && (i as i32) + delta_i < (self.grid.len() as i32)
                && (j as i32) + delta_j > 0
                && (j as i32) + delta_j < (self.grid[0].len() as i32)
            {
                let target_i = i + (*delta_i as usize);
                let target_j = j + (*delta_j as usize);
                if self.is_cell_special(target_i, target_j) {
                    return Some((target_i, target_j));
                }
            }
        }
        None
    }

    fn find_grid_numbers(&self) -> Vec<GridNumber> {
        let mut grid_numbers: Vec<GridNumber> = Vec::new();
        let mut scanning_number: Option<&mut GridNumber> = None;
        for (i, row) in self.grid.iter().enumerate() {
            for (j, cell) in row.iter().enumerate() {
                if self.is_cell_digit(i, j) {
                    if scanning_number.is_none() {
                        grid_numbers.push(GridNumber::new());
                        scanning_number = grid_numbers.last_mut();
                    }

                    let take_mut_scanning_number = scanning_number.as_mut().unwrap();
                    take_mut_scanning_number.add_digit(*cell);

                    if let Some(symbol_pos) = self.get_symbol_near_cell(i, j) {
                        take_mut_scanning_number.add_near_symbol(symbol_pos);
                    }
                } else {
                    scanning_number = None;
                }

                // Reset at the end of line
                if j == row.len() - 1 && scanning_number.is_some() {
                    scanning_number = None;
                }
            }
        }

        grid_numbers
    }
}

impl Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let grid_s = self
            .grid
            .iter()
            .map(|row| row.iter().collect())
            .collect::<Vec<String>>()
            .join("\n");
        write!(f, "{}", grid_s)
    }
}

fn first_part_solution(grid_numbers: &[GridNumber]) -> i32 {
    grid_numbers
        .iter()
        .filter(|&grid_num| grid_num.is_part_number())
        .map(|grid_num| grid_num.num())
        .sum()
}

fn second_part_solution(grid: &Grid, grid_numbers: &Vec<GridNumber>) -> i32 {
    let mut probable_gears: HashMap<(usize, usize), Vec<&GridNumber>> = HashMap::new();

    for grid_number in grid_numbers {
        for &(i, j) in &grid_number.near_symbols {
            if grid.grid[i][j] == '*' {
                probable_gears
                    .entry((i, j))
                    .or_default()
                    .push(grid_number);
            }
        }
    }

    probable_gears
        .values()
        .filter(|&v| v.len() == 2)
        .map(|parts| parts.iter().map(|&p| p.num()).product::<i32>())
        .sum()
}

fn main() {
    let start_time = Instant::now();
    let path = std::env::current_dir().expect("Cannot get current dir.");
    let path = path.join("src/bin/aoc3/in.txt");
    let file = std::fs::read_to_string(path).expect("Cannot read input file");

    let grid: Vec<Vec<char>> = file
        .lines()
        .map(|line| line.chars().collect::<Vec<char>>())
        .collect();
    let grid = Grid { grid };
    let grid_numbers = grid.find_grid_numbers();
    let first_solution = first_part_solution(&grid_numbers);
    println!("First part solution = {}", first_solution);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );

    let second_solution = second_part_solution(&grid, &grid_numbers);
    println!("Second part solution = {}", second_solution);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );
}
