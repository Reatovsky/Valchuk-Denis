package main

import (
	"fmt"
	"math"
)

func main() {

	fmt.Print("Введите кол-во чисел: ")
	var n int
	fmt.Scan(&n)

	max_n := math.MinInt
	min_n := math.MaxInt
	for i := 1; i <= n; i++ {
		fmt.Print("Введите число: ")
		var a int
		fmt.Scan(&a)

		if a > max_n {
			max_n = a
		}
		if a < min_n {
			min_n = a
		}
	}

	fmt.Printf("Максимальное число: %v\nМинимальное число: %v", max_n, min_n)
}
