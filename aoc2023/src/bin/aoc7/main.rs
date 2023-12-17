use std::{cmp::Ordering, collections::HashMap, time::Instant};

#[derive(Debug)]
enum HandType {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard,
    Empty,
}

#[derive(Debug)]
struct Hand {
    cards: String,
    counts: HashMap<char, i32>,
    bid: i32,
    hand_type: HandType,
}

impl HandType {
    fn value(&self) -> i32 {
        match self {
            HandType::FiveOfAKind => 7,
            HandType::FourOfAKind => 6,
            HandType::FullHouse => 5,
            HandType::ThreeOfAKind => 4,
            HandType::TwoPair => 3,
            HandType::OnePair => 2,
            HandType::HighCard => 1,
            HandType::Empty => 0,
        }
    }
}

impl Hand {
    fn new(cards: &str, bid: i32) -> Self {
        let mut counts = HashMap::new();
        for char in cards.chars() {
            *counts.entry(char).or_insert(0) += 1;
        }
        Self {
            cards: String::from(cards),
            counts,
            bid,
            hand_type: HandType::Empty,
        }
    }

    fn update_type(&mut self) {
        let mut ordered_counts = self
            .counts
            .iter()
            .map(|(key, value)| (key, *value))
            .collect::<Vec<_>>();
        ordered_counts.sort_by(|a, b| b.1.cmp(&a.1));
        let most_common = ordered_counts[0].1;
        let second_most_common = if let Some(x) = ordered_counts.get(1) {
            x.1
        } else {
            0
        };

        let hand_type = match (most_common, second_most_common) {
            (5, _) => HandType::FiveOfAKind,
            (4, _) => HandType::FourOfAKind,
            (3, 2) => HandType::FullHouse,
            (3, 1) => HandType::ThreeOfAKind,
            (2, 2) => HandType::TwoPair,
            (2, 1) => HandType::OnePair,
            _ => HandType::HighCard,
        };

        self.hand_type = hand_type;
    }

    fn update_type_with_jokers(&mut self) {
        let mut ordered_counts = self
            .counts
            .iter()
            .map(|(key, value)| (key, *value))
            .filter(|x| *x.0 != 'J')
            .collect::<Vec<_>>();
        ordered_counts.sort_by(|a, b| b.1.cmp(&a.1));

        let n_jokers = *self.counts.get(&'J').unwrap_or(&0);
        if n_jokers == 5 {
            self.hand_type = HandType::FiveOfAKind;
            return;
        }

        let most_common = ordered_counts[0].1 + n_jokers;
        let second_most_common = if let Some(x) = ordered_counts.get(1) {
            x.1
        } else {
            0
        };

        let hand_type = match (most_common, second_most_common) {
            (5, _) => HandType::FiveOfAKind,
            (4, _) => HandType::FourOfAKind,
            (3, 2) => HandType::FullHouse,
            (3, 1) => HandType::ThreeOfAKind,
            (2, 2) => HandType::TwoPair,
            (2, 1) => HandType::OnePair,
            _ => HandType::HighCard,
        };

        self.hand_type = hand_type;
    }

    fn compare_hands(h1: &Hand, h2: &Hand, card_to_value: &HashMap<char, i32>) -> Ordering {
        if h1.hand_type.value() == h2.hand_type.value() {
            for (c1, c2) in h1.cards.chars().zip(h2.cards.chars()) {
                let v1 = card_to_value.get(&c1).unwrap();
                let v2 = card_to_value.get(&c2).unwrap();
                match v1.cmp(v2) {
                    Ordering::Less => return Ordering::Less,
                    Ordering::Equal => continue,
                    Ordering::Greater => return Ordering::Greater,
                }
            }
        }
        h1.hand_type.value().cmp(&h2.hand_type.value())
    }
}

fn main() {
    let start_time = Instant::now();
    let current_dir = std::env::current_dir().expect("Cannot get current dir.");
    let path = current_dir.join("src/bin/aoc7/in.txt");
    let file = std::fs::read_to_string(path).expect("Cannot read file.");
    let mut card_to_value = HashMap::from([
        ('A', 14),
        ('K', 13),
        ('Q', 12),
        ('J', 11),
        ('T', 10),
        ('9', 9),
        ('8', 8),
        ('7', 7),
        ('6', 6),
        ('5', 5),
        ('4', 4),
        ('3', 3),
        ('2', 2),
    ]);

    let hands_and_bids: Vec<_> = file
        .lines()
        .map(|x| {
            let split: Vec<&str> = x.split(' ').collect();
            let first = *split.first().unwrap();
            let second = *split.get(1).unwrap();
            (first, second)
        })
        .collect();

    let mut hands: Vec<Hand> = Vec::new();
    for (hand_str, bid_str) in hands_and_bids {
        let bid: i32 = bid_str.parse().unwrap();
        let hand = Hand::new(hand_str, bid);
        hands.push(hand);
    }

    // First part
    hands.iter_mut().for_each(|h| h.update_type());
    hands.sort_by(|h1, h2| Hand::compare_hands(h1, h2, &card_to_value));
    let res: i32 = hands
        .iter()
        .enumerate()
        .map(|(idx, el)| ((idx as i32) + 1) * el.bid)
        .sum();
    println!("First part solution = {}", res);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );


    *card_to_value.entry('J').or_insert(1) = 1;
    hands.iter_mut().for_each(|h| h.update_type_with_jokers());
    hands.sort_by(|h1, h2| Hand::compare_hands(h1, h2, &card_to_value));

    let res: i32 = hands
        .iter()
        .enumerate()
        .map(|(idx, el)| ((idx as i32) + 1) * el.bid)
        .sum();
    println!("Second part solution = {}", res);
    println!(
        "Took {} seconds",
        (start_time.elapsed().as_nanos() as f32) * (1e-9)
    );
}
