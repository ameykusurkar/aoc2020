use std::collections::{HashMap, HashSet};
use std::io::{self, BufRead};
use std::ops::RangeInclusive;

type Ticket = Vec<u32>;

struct Rules(HashMap<String, Vec<RangeInclusive<u32>>>);

impl Rules {
    fn possible_names(&self, field: u32) -> HashSet<String> {
        self.0
            .iter()
            .filter(|(_name, ranges)| ranges.iter().any(|r| r.contains(&field)))
            .map(|(name, _ranges)| name.to_owned())
            .collect()
    }

    fn names(&self) -> HashSet<String> {
        self.0.keys().map(|n| n.to_owned()).collect()
    }
}

fn main() {
    let stdin = io::stdin();
    let mut handle = stdin.lock();

    let mut lines = (&mut handle).lines();
    let rules = parse_while_rules(&mut lines);

    lines.next(); // Header for your ticket, ignore

    let your_ticket = parse_csv(&lines.next().expect("Should have more lines").unwrap());

    lines.next(); // Blank line, ignore
    lines.next(); // Header for nearby tickets, ignore

    let nearby_tickets: Vec<Ticket> = lines.map(|l| parse_csv(&l.unwrap())).collect();

    let mut valid_tickets = Vec::new();
    let mut invalid_total = 0;

    for t in nearby_tickets {
        let invalids = invalid_fields(&rules, &t);
        if invalids.is_empty() {
            valid_tickets.push(t);
        } else {
            invalid_total += invalids.iter().sum::<u32>();
        }
    }

    println!("{}", invalid_total);

    let num_fields = valid_tickets[0].len();

    let mut remaining_choices = Vec::new();
    for i in 0..num_fields {
        let mut choices = rules.names();
        for ticket in &valid_tickets {
            choices = choices
                .intersection(&rules.possible_names(ticket[i]))
                .map(|n| n.to_owned())
                .collect();
        }
        remaining_choices.push(choices);
    }

    let result = resolve_possibilities(remaining_choices)
        .iter()
        .enumerate()
        .filter(|(_i, name)| name.starts_with("depart"))
        .map(|(i, _name)| your_ticket[i])
        .fold(1u64, |acc, val| acc * val as u64);
    println!("{:?}", result);
}

fn parse_while_rules<I>(lines: &mut I) -> Rules
where
    I: Iterator<Item = std::io::Result<String>>,
{
    let mut rules = HashMap::new();
    for line in lines {
        let line = line.unwrap();

        if line.is_empty() {
            break;
        }

        let mut split_line = line.split(": ");
        let field = split_line.next().expect("Should have key: value pair");

        let ranges = split_line
            .next()
            .expect("Should have 2 ranges")
            .split(" or ");
        let mut ranges_int = Vec::with_capacity(2);
        for range in ranges {
            let mut split_range = range.split("-");
            let left = split_range.next().unwrap().parse().unwrap();
            let right = split_range.next().unwrap().parse().unwrap();
            ranges_int.push(RangeInclusive::new(left, right));
        }
        rules.insert(field.to_string(), ranges_int);
    }
    Rules(rules)
}

fn parse_csv(line: &str) -> Vec<u32> {
    line.split(",")
        .map(|token| token.parse().expect("Should be u32"))
        .collect()
}

fn invalid_fields(rules: &Rules, ticket: &Ticket) -> Vec<u32> {
    ticket
        .iter()
        .filter(|val| rules.possible_names(**val).is_empty())
        .map(|val| *val)
        .collect()
}

fn resolve_possibilities(choices: Vec<HashSet<String>>) -> Vec<String> {
    let mut remaining_choices = choices.clone();
    let mut resolved_names = HashSet::new();

    loop {
        if remaining_choices
            .iter()
            .all(|field_choices| field_choices.len() == 1)
        {
            break;
        }

        let solved_field = remaining_choices
            .iter()
            .enumerate()
            .find(|(_i, field_choices)| {
                field_choices.len() == 1
                    && !resolved_names.contains(field_choices.iter().next().unwrap())
            });

        let (solved_idx, solved_name) = solved_field.expect("Should have a HashSet!");
        let solved_name = solved_name.iter().next().unwrap().to_owned();
        resolved_names.insert(solved_name.to_owned());

        for (i, field_choices) in remaining_choices.iter_mut().enumerate() {
            if i == solved_idx {
                continue;
            }

            field_choices.remove(&solved_name);
        }
    }

    remaining_choices
        .iter()
        .map(|field_choices| field_choices.iter().next().unwrap().to_owned())
        .collect()
}
