from P2f import BankAccount

john = BankAccount("John", "saving", 500)
tim = BankAccount("Tim", "loan", -1_000_000)
sarah_saving = BankAccount("Sarah", "saving")

john.deposit(3000)
tim.pay_loan(500_000)
sarah_saving.deposit(50_000_000)

sarah_loan = BankAccount("Sarah", "loan", -100_000_000)

accounts = [john, tim, sarah_saving, sarah_loan]

for acc in accounts:
    acc.print_customer()