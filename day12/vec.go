package main

type Vec struct {
	x, y int
}

func (v Vec) rotate(deg int) Vec {
	x1 := cos(deg)*v.x - sin(deg)*v.y
	y1 := sin(deg)*v.x + cos(deg)*v.y
	return Vec{x1, y1}
}

var SIN = [4]int{0, 1, 0, -1}

func sin(deg int) int {
	if deg < 0 {
		deg += 360
	}
	index := int((deg % 360) / 90)
	return SIN[index]
}

var COS = [4]int{1, 0, -1, 0}

func cos(deg int) int {
	if deg < 0 {
		deg += 360
	}
	index := int((deg % 360) / 90)
	return COS[index]
}
