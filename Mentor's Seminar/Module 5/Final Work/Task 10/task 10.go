package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Print("Введите кол-во чисел:")
	var n int
	fmt.Scan(&n)

	sum := 0
	max_n := math.MinInt
	min_n := math.MaxInt
	e_count := 0
	ne_count := 0
	for i := 1; i <= n; i++ {
		fmt.Print("Введите число:")
		var a int
		fmt.Scan(&a)

		sum += a

		if a > max_n {
			max_n = a
		}
		if a < min_n {
			min_n = a
		}

		if a%2 == 0 {
			e_count++
		} else {
			ne_count++
		}
	}

	avg := float64(sum) / float64(n)

	fmt.Printf("Сумма чисел: %v\nСреднее значение: %g\nМаксимальное значение: %v\nМинимальное значение: %v\nКол-во чётных чисел: %v\nКол-во нечётных чисел: %v", sum, avg, max_n, min_n, e_count, ne_count)
}
