package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var lines []string

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	memory := make(map[int64]int64)
	var mask *map[int]int

	for _, s := range lines {
		if strings.Contains(s, "[") {
			var addr, val int64
			fmt.Sscanf(s, "mem[%d] = %d", &addr, &val)
			if mask != nil {
				val = applyMask(mask, val)
			}
			memory[addr] = val
		} else {
			mask = makeMask(s[7:]) // First 7 chars are "mask = "
		}
	}

	sum := int64(0)
	for _, val := range memory {
		sum += val
	}
	fmt.Println(sum)

  var mask_str string
	memory = make(map[int64]int64)

	for _, s := range lines {
		if strings.Contains(s, "[") {
			var addr, val int64
			fmt.Sscanf(s, "mem[%d] = %d", &addr, &val)
			if mask_str != "" {
        addrs := applyMask2(mask_str, addr)
        for _, a := range addrs {
          memory[a] = val
          // fmt.Printf("mem[%d] = %d\n", a, val)
        }
			}
		} else {
			mask_str = s[7:] // First 7 chars are "mask = "
		}
	}

  sum = int64(0)
	for _, val := range memory {
		sum += val
	}
	fmt.Println(sum)
}

func makeMask(s string) *map[int]int {
	mask := make(map[int]int)
	for i, char := range s {
		if char != 'X' {
			mask[i] = int(char - 48) // Convert ascii to int
		}
	}
	return &mask
}

func applyMask(mask *map[int]int, val int64) int64 {
	for i, bit := range *mask {
		index := 36 - i - 1 // MSB is on the left
		if bit == 0 {
			val &= ^(1 << index)
		} else {
			val |= 1 << index
		}
	}
	return val
}

func applyMask2(mask string, addr int64) []int64 {
	addrs := []int64{addr}
	for i, bit := range mask {
		index := 36 - i - 1
		if bit == '1' {
			addrs = applySet(index, addrs)
		} else if bit == 'X' {
			addrs = applyFloat(index, addrs)
		}
	}
	return addrs
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
