class BankAccount:
    def __init__(self,first_name,last_name,account_id,account_type,pin,balance):
        self.first_name= first_name
        self.last_name=last_name
        self.account_id=account_id
        self.account_type=account_type
        self.pin=pin
        self.balance=float(balance)
    def display_balance(self):
        print("El saldo en la cuenta es de",self.balance)
    def withdraw(self, amnt):
        if amnt <= 0:
            print("La cantidad a retirar debe ser mayor que cero.")
        elif self.balance >= amnt:
            self.balance -= amnt
            print(f"Retiro exitoso por ${amnt}")
            return True
        else:
            print("Fondos insuficientes para realizar el retiro.")
            return False

    def deposit(self,amnt):
        if amnt >=0:
            print("Deposito exitoso por $", amnt)
            self.balance += amnt
        else:
            print("Por favor ingrese una cantidad valida para el deposito")
            
    def transfer(self,accnt,amnt):
        if self.withdraw(amnt):
            accnt.deposit(amnt)
            print(f"Transferencia de ${amnt} a la cuenta de {accnt.first_name} {accnt.last_name} exitosa\nSaldo actual de ${self.balance:.2f}.")
        else:
            print("Transferencia fallida.")

            print("Transferencia fallida.")
