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

    let rules = parse_while_rules(&mut handle);

    (&mut handle).lines().next(); // Header for your ticket, ignore

    let your_ticket = parse_ticket(&(&mut handle).lines().next().unwrap().unwrap());

    (&mut handle).lines().next(); // Blank line, ignore
    (&mut handle).lines().next(); // Header for nearby tickets, ignore

    let nearby_tickets: Vec<Ticket> = handle.lines().map(|l| parse_ticket(&l.unwrap())).collect();

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

fn parse_while_rules<R: BufRead>(reader: &mut R) -> Rules {
    let mut rules = HashMap::new();
    for line in reader.lines() {
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

fn parse_ticket(line: &str) -> Ticket {
    let mut vec = Vec::new();
    for token in line.split(",") {
        vec.push(token.parse().expect("Should be int"));
    }
    vec
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

        let solved_field_name = remaining_choices.iter().find(|field_choices| {
            field_choices.len() == 1
                && !resolved_names.contains(field_choices.iter().next().unwrap())
        });

        if solved_field_name.is_none() {
            panic!("Cannot resolve!");
        }

        let solved_name = solved_field_name.unwrap().iter().next().unwrap().to_owned();

        for field_choices in &mut remaining_choices {
            field_choices.remove(&solved_name);

            if field_choices.is_empty() {
                // Put it back, as this is the right answer (hacky, I know)
                field_choices.insert(solved_name.to_owned());
                resolved_names.insert(solved_name.to_owned());
            }
        }
    }

    remaining_choices
        .iter()
        .map(|field_choices| field_choices.iter().next().unwrap().to_owned())
        .collect()
}
