class BankAccount:
    branch_name = "KKU Complex"
    branch_number = 1724
    last_loan_number = 0
    last_saving_number = 0

    __type_saving = 1
    __type_loan = 2

    def __init__(self, name, acc_type="saving", balance=0):
        self.name = name
        self.type = acc_type
        self.balance = balance

        if acc_type == "saving":
            BankAccount.last_saving_number += 1
            self.account_number = f"{BankAccount.branch_number}-{BankAccount.__type_saving}-{BankAccount.last_saving_number}"
        elif acc_type == "loan":
            BankAccount.last_loan_number += 1
            self.account_number = f"{BankAccount.branch_number}-{BankAccount.__type_loan}-{BankAccount.last_loan_number}"

    def print_customer(self):
        print("----- Customer Record -----")
        print(f"Name: {self.name}")
        print(f"Account number: {self.account_number}")
        print(f"Account type: {self.type}")
        print(f"Balance: {self.balance}")
        print("----- End Record -----\n")

    def deposit(self, amount=0):
        self.balance += amount
        return self.balance

    def pay_loan(self, amount=0):
        self.balance += amount
        return self.balance