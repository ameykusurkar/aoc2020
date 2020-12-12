package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var entries []int

	for scanner.Scan() {
		val, _ := strconv.Atoi(scanner.Text())
		entries = append(entries, val)
	}

	entrySet := makeSet(entries)

	a, b, _ := twoSum(entrySet, 2020)
	fmt.Println(a * b)

	a, b, c, _ := threeSum(entrySet, 2020)
	fmt.Println(a * b * c)
}

func twoSum(entries map[int]bool, target int) (int, int, bool) {
	for x, _ := range entries {
		_, ok := entries[target-x]
		if ok {
			return x, target - x, true
		}
	}

	return 0, 0, false
}

func threeSum(entries map[int]bool, target int) (int, int, int, bool) {
	for x, _ := range entries {
		remaining := target - x
		copies := copySet(entries)
		delete(copies, x)
		y, z, found := twoSum(copies, remaining)
		if found {
			return x, y, z, true
		}
	}

	return 0, 0, 0, false
}

func makeSet(entries []int) map[int]bool {
	set := make(map[int]bool)
	for _, e := range entries {
		set[e] = true
	}
	return set
}

func copySet(entries map[int]bool) map[int]bool {
	copies := make(map[int]bool)
	for k, v := range entries {
		copies[k] = v
	}
	return copies
}
