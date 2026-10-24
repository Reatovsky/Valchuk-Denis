package main

import (
	"fmt"
)

func main() {

	fmt.Print("Введите число: ")
	var n int
	fmt.Scan(&n)

	sum := 0
	for i := 1; i <= n; i++ {
		sum += i
	}

	avg := float64(sum) / float64(n)

	fmt.Printf("Сумма чисел от 1 до %v: %v\n", n, sum)
	fmt.Printf("Среднее значение чисел от 1 до %v: %g\n", n, avg)
}
