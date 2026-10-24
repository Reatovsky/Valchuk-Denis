package main

import (
	"fmt"
)

func main() {

	fmt.Print("Введите число: ")
	var n int
	fmt.Scan(&n)

	printTable(n)
}

func printTable(n int) {
	for i := 1; i <= 10; i++ {
		fmt.Printf("%v * %v = %v\n", n, i, n*i)
	}
}
