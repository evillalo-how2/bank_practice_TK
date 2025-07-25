# #bank_accounts
# Crea un archivo llamado bank_accounts.py

# Define una clase llamada BankAccount. Usa el método init() para establecer los siguientes atributos:


# first_name: una cadena con el nombre del titular.
# last_name: una cadena con el apellido del titular.
# account_id: un número entero que identifique la cuenta.
# account_type: una cadena que indique el tipo de cuenta.
# pin: un número entero que represente el PIN.
# balance: un número flotante que represente el saldo de la cuenta.


# Crea tres métodos en la clase:


# .deposit(): agrega dinero a la cuenta y devuelve el nuevo balance.
# .withdraw(): retira dinero restando del balance y devuelve el importe retirado.
# .display_balance(): imprime el valor actual del balance.


# Inicializa un nuevo objeto de la clase BankAccount y realiza lo siguiente:


# Deposita $96 en la cuenta.
# Retira $25 de la cuenta.
# Imprime el saldo de la cuenta corriente.
# Depositar $50
# Depositar $6
# Retirar $17
# imprimir
# Extra, realizar tranferencias



# agregar validaciones.
# unos se manejan como self, y otros como otro tipo de cuenta.


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
