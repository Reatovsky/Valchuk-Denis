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

		if i%2 == 0 && i%3 == 0 {
			sum += i
		}
	}

	fmt.Printf("Сумма чисел, являющиеся чётными и делящимися на 3: %v", sum)
}
