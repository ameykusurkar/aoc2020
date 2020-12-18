package main

import (
	"bufio"
	"fmt"
	"os"
)

type Vertex struct {
	x, y, z int
}

type Grid struct {
	grid map[Vertex]bool
}

func NewGrid() *Grid {
	return &Grid{grid: make(map[Vertex]bool)}
}

func (g *Grid) Set(vert Vertex, active bool) {
	g.grid[vert] = active
}

func (g *Grid) GetAdjacents(vert Vertex) []Vertex {
	adjacents := make([]Vertex, 0, 26)
	for x := vert.x - 1; x <= vert.x+1; x++ {
		for y := vert.y - 1; y <= vert.y+1; y++ {
			for z := vert.z - 1; z <= vert.z+1; z++ {
				v := Vertex{x, y, z}
				if v != vert {
					adjacents = append(adjacents, v)
				}
			}
		}
	}
	return adjacents
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	grid := NewGrid()
	z, y := 0, 0
	for ; scanner.Scan(); y++ {
		x := 0
		for _, c := range scanner.Text() {
			grid.Set(Vertex{x, y, z}, c == '#')
			x++
		}
	}

	fmt.Printf("%v\n", grid)
	fmt.Printf("%d\n", grid.GetAdjacents(Vertex{0, 0, 0}))
}
