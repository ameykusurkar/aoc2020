package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Memory map[int64]int64
type memoryWriter func(memory Memory, addr int64, val int64, mask string)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var lines []string

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	sum := execute(lines, memoryWriterPartOne)
	fmt.Println(sum)

	sum = execute(lines, memoryWriterPartTwo)
	fmt.Println(sum)
}

func execute(lines []string, writer memoryWriter) int64 {
	var mask_str string
	memory := make(Memory)

	for _, s := range lines {
		if strings.Contains(s, "[") {
			var addr, val int64
			fmt.Sscanf(s, "mem[%d] = %d", &addr, &val)
			if mask_str != "" {
				writer(memory, addr, val, mask_str)
			}
		} else {
			mask_str = s[7:] // First 7 chars are "mask = "
		}
	}

	sum := int64(0)
	for _, val := range memory {
		sum += val
	}
	return sum
}

func memoryWriterPartOne(memory Memory, addr int64, val int64, mask string) {
	mask_map := makeMaskMap(mask)

	for i, bit := range *mask_map {
		index := 36 - i - 1 // MSB is on the left
		if bit == 0 {
			val &= ^(1 << index)
		} else {
			val |= 1 << index
		}
	}

	memory[addr] = val
}

func memoryWriterPartTwo(memory Memory, addr int64, val int64, mask string) {
	addrs := []int64{addr}
	for i, bit := range mask {
		index := 36 - i - 1 // MSB is on the left
		if bit == '1' {
			addrs = applySet(index, addrs)
		} else if bit == 'X' {
			addrs = applyFloat(index, addrs)
		}
	}

	for _, a := range addrs {
		memory[a] = val
	}
}

func makeMaskMap(s string) *map[int]int {
	mask := make(map[int]int)
	for i, char := range s {
		if char != 'X' {
			mask[i] = int(char - 48) // Convert ascii to int
		}
	}
	return &mask
}

func applyFloat(bit int, addrs []int64) []int64 {
	prev_len := len(addrs)
	for i := 0; i < prev_len; i++ {
		addrs[i] &= ^(1 << bit)
		addrs = append(addrs, addrs[i]|1<<bit)
	}
	return addrs
}

func applySet(bit int, addrs []int64) []int64 {
	for i := 0; i < len(addrs); i++ {
		addrs[i] |= 1 << bit
	}
	return addrs
}
