package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func play(numbers []int, iters int) int {
	var t, last int
	seen := make(map[int][]int)

	for _, n := range numbers {
		t += 1
		last = n
		seen[last] = append(seen[last], t)
	}

	for t < iters {
		t += 1
		if len(seen[last]) == 1 {
			last = 0
		} else {
			prevs := seen[last]
			prev2 := prevs[len(prevs)-2]
			prev := prevs[len(prevs)-1]
			last = prev - prev2
		}
		seen[last] = append(seen[last], t)
	}
	return last
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()

	tokens := strings.Split(scanner.Text(), ",")

	var numbers []int
	for _, token := range tokens {
		n, _ := strconv.Atoi(token)
		numbers = append(numbers, n)
	}

	result := play(numbers, 2020)
	fmt.Println(result)

	// TODO: Try to make this more efficient
	result = play(numbers, 30000000)
	fmt.Println(result)
}
