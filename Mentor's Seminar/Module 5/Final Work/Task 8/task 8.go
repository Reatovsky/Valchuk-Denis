package main

import (
	"fmt"
)

func main() {

	fmt.Print("Введите число: ")
	var n int
	fmt.Scan(&n)

	if isPrime(n) {
		fmt.Printf("Число %v - простое", n)
	} else {
		fmt.Printf("Число %v - не простое", n)
	}
}

func isPrime(n int) bool {
	if n == 1 {
		return false
	}
	if n == 2 {
		return true
	}

	for i := 2; i <= n/2+1; i++ {
		if n%i == 0 {
			return false
		}
	}

	return true
}
