package main

import (
	"fmt"
)

func main() {

	fmt.Print("Введите кол-во чисел: ")
	var n int
	fmt.Scan(&n)

	pos := 0
	neg := 0
	nul := 0
	for i := 1; i <= n; i++ {
		fmt.Print("Введите число: ")
		var a int
		fmt.Scan(&a)

		if a > 0 {
			pos++
		} else if a < 0 {
			neg++
		} else {
			nul++
		}
	}

	fmt.Printf("Кол-во положительных чисел: %v\nКол-во отрицательных чисел: %v\nКол-во нулей: %v", pos, neg, nul)
}
