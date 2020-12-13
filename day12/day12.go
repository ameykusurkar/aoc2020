package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var instructions []Instr

	for scanner.Scan() {
		instructions = append(instructions, makeInstr(scanner.Text()))
	}

	ship := Ship{x: 0, y: 0, v: Vec{x: 1, y: 0}}

	for _, instr := range instructions {
		ship.execute(instr)
	}

	fmt.Println(abs(ship.x) + abs(ship.y))

	wship := WaypointShip{x: 0, y: 0, v: Vec{x: 10, y: 1}}

	for _, instr := range instructions {
		wship.execute(instr)
	}

	fmt.Println(abs(wship.x) + abs(wship.y))
}

type Instr struct {
	op  string
	arg int
}

func makeInstr(line string) Instr {
	arg, _ := strconv.Atoi(line[1:])
	return Instr{string(line[0]), arg}
}

type Ship struct {
	x, y int
	v    Vec
}

func (ship *Ship) execute(instr Instr) {
	switch instr.op {
	case "N", "S", "E", "W":
		v := directionToVec(instr.op)
		ship.move(v, instr.arg)
	case "F":
		ship.move(ship.v, instr.arg)
	case "L":
		ship.rotate(instr.arg)
	case "R":
		ship.rotate(-instr.arg)
	}
}

func (ship *Ship) move(v Vec, dist int) {
	ship.x += dist * v.x
	ship.y += dist * v.y
}

func (ship *Ship) rotate(deg int) {
	ship.v = ship.v.rotate(deg)
}

func directionToVec(direction string) Vec {
	switch direction {
	case "N":
		return Vec{0, 1}
	case "S":
		return Vec{0, -1}
	case "E":
		return Vec{1, 0}
	case "W":
		return Vec{-1, 0}
	default:
		panic("Unknown direction!")
	}
}

func abs(x int) int {
	if x < 0 {
		return -x
	} else {
		return x
	}
}

type WaypointShip struct {
	x, y int // Ship position
	v    Vec // Waypoint position
}

func (ship *WaypointShip) execute(instr Instr) {
	switch instr.op {
	case "N", "S", "E", "W":
		v := directionToVec(instr.op)
		ship.moveWaypoint(v, instr.arg)
	case "F":
		ship.move(instr.arg)
	case "L":
		ship.rotate(instr.arg)
	case "R":
		ship.rotate(-instr.arg)
	}
}

func (ship *WaypointShip) moveWaypoint(v Vec, dist int) {
	ship.v.x += dist * v.x
	ship.v.y += dist * v.y
}

func (ship *WaypointShip) move(times int) {
	ship.x += times * ship.v.x
	ship.y += times * ship.v.y
}

func (ship *WaypointShip) rotate(deg int) {
	ship.v = ship.v.rotate(deg)
}
