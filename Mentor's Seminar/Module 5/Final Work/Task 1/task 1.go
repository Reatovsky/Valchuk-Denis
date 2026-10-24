package main

import (
	"fmt"
)

func main() {

	fmt.Print("Первое число: ")
	var a float64
	fmt.Scan(&a)

	fmt.Print("Второе число: ")
	var b float64
	fmt.Scan(&b)

	fmt.Print("Введите операцию (+, -, *, /): ")
	var op string
	fmt.Scan(&op)

	switch op {
	case "+":
		fmt.Printf("%g + %g = %g\n", a, b, a+b)
	case "-":
		fmt.Printf("%g - %g = %g\n", a, b, a-b)
	case "*":
		fmt.Printf("%g * %g = %g\n", a, b, a*b)
	case "/":
		if b == 0 {
			fmt.Println("Ошибка: Нельзя делить на ноль :c")
			return
		}
		fmt.Printf("%g / %g = %g\n", a, b, a/b)
	default:
		fmt.Println("Ошибка: Калькулятор не всемогущ! Попробуйте операции: +, -, * или /")
	}
}
