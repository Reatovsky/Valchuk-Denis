package main

import (
	"fmt"
)

func main() {

	fmt.Print("Введите число: ")
	var n int
	fmt.Scan(&n)

	if n > 0 {
		fmt.Printf("Число '%v' - положительное\n", n)
	} else if n == 0 {
		fmt.Printf("Число '%v' - это ноль\n", n)
	} else {
		fmt.Printf("Число '%v' - отрицательное\n", n)
	}

	if n%2 == 0 {
		fmt.Printf("Число '%v' - чётное\n", n)
	} else {
		fmt.Printf("Число '%v' - нечётное\n", n)
	}

	if n%3 == 0 && n%5 == 0 {
		fmt.Printf("Число '%v' - делится и на 3, и на 5", n)
	} else if n%3 == 0 {
		fmt.Printf("Число '%v' - делится на 3, но не на 5", n)
	} else if n%5 == 0 {
		fmt.Printf("Число '%v' - делится на 5, но не на 3", n)
	} else {
		fmt.Printf("Число '%v' - не делится ни на 3, ни на 5", n)
	}
}
