package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {

	balance := 0.0
	reader := bufio.NewReader(os.Stdin)

	for {
		fmt.Print("Введите операцию: ")
		op, _ := reader.ReadString('\n')
		op = strings.TrimSpace(op)

		switch op {
		case "Посмотреть баланс":
			{
				fmt.Printf("Текущий баланс: %v\n", balance)
			}
		case "Пополнить баланс":
			{
				fmt.Print("Введите сумму пополнения баланса: ")
				var input float64
				fmt.Scan(&input)

				balance += input
				fmt.Printf("Баланс успешно пополнен! Текущий баланс: %v\n", balance)
			}
		case "Снять средства":
			{
				fmt.Print("Введите сумму снятия баланса: ")
				var output float64
				fmt.Scan(&output)

				if balance >= output {
					balance -= output
					fmt.Printf("Средства успешно сняты! Текущий баланс: %v\n", balance)
				} else {
					fmt.Printf("Ошибка: на счёте недостаточно средств. Текущий баланс: %v\n", balance)
				}
			}
		case "Выход из банкомата":
			{
				return
			}
		default:
			{
				fmt.Printf("Банкомат исполняет следующие операции:\n1. Посмотреть баланс\n2. Пополнить баланс\n3. Снять средства\n4. Выход из банкомата\n")
			}
		}
	}
}
