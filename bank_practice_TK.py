import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class BankAccount:
    def __init__(self,first_name,last_name,account_id,account_type,pin,balance):
        self.first_name= first_name
        self.last_name=last_name
        self.account_id=account_id
        self.account_type=account_type
        self.pin=pin
        self.balance=float(balance)
        self.history=[]

    def validate_pin(self, pin):
        return self.pin == str(pin)
    
    def add_history(self,type_of_transaction):
        if len(self.history) >= 5:
            self.history.pop(0)
        self.history.append(type_of_transaction)
        
    def display_balance(self):
        print("El saldo en la cuenta es de",self.balance)

    def withdraw(self, amnt):
        if amnt <= 0:
            print("La cantidad a retirar debe ser mayor que cero.")
        elif self.balance >= amnt:
            self.balance -= amnt
            print(f"Retiro exitoso por ${amnt}")
            self.add_history({"Tipo de transacción": "Retiro",
                          "Monto": amnt,
                          "Saldo": self.balance,
                          "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          "Cuenta destino": None})
            return True
        else:
            print("Fondos insuficientes para realizar el retiro.")
            return False

    def deposit(self,amnt):
        if amnt >=0:
            print("Deposito exitoso por $", amnt)
            self.balance += amnt
            self.add_history({"Tipo de transacción": "Deposito",
                          "Monto": amnt,
                          "Saldo": self.balance,
                          "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          "Cuenta destino": None})
        else:
            print("Por favor ingrese una cantidad valida para el deposito")
            
    def transfer(self,accnt,amnt):
        if self.account_id == accnt.account_id:
            print("No puedes transferir a la misma cuenta.")
        if self.withdraw(amnt):
            accnt.deposit(amnt)
            print(f"Transferencia de ${amnt} a la cuenta de {accnt.first_name} {accnt.last_name} exitosa\nSaldo actual de ${self.balance:.2f}.")
            self.add_history({"Tipo de transacción": "Transferencia",
                "Monto": amnt,
                "Saldo": self.balance,
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Cuenta destino": accnt.first_name+" "+accnt.last_name})
        else:
            print("Transferencia fallida.")

cuenta_patito={
"Selecciona la cuenta":BankAccount("Default","Default",0000,"Regular",0000,0.0),
"1224":BankAccount("Alberto","Rodriguez",1224,"Regular","1334",0.0),
"7795":BankAccount("Eriberto","Perez",7795,"Regular","9577",1150.00),
"5412": BankAccount("Karina", "López", 5412, "Premium","4312", 300.0),
"3312": BankAccount("Erick", "Lugo", 3312, "Premium","3121", 350.0)
}

class Interface:
    def __init__(self,root,accounts):
        self.root=root
        self.accounts=accounts
        self.current_account=None
        
        self.root.title("Banco patito: Inicio de Sesión")
        self.login_frame= tk.Frame(root)
        self.login_frame.pack(padx=10,pady=10)

        self.account_var=tk.StringVar(value=list(accounts.keys())[0])
        self.account_menu=tk.OptionMenu(self.login_frame,self.account_var, *accounts.keys())
        self.account_menu.pack(pady=10)

        self.pin_label=tk.Label(self.login_frame,text="",pady=20)
        self.pin_label.pack()

        self.pin_entry=None
        self.login_button = None
        self.account_var.trace('w', self.pin_showup)

    def pin_showup(self,*args):
        if self.account_var.get() != "Selecciona la cuenta" :
            self.pin_label.config(text="Ingresa tu pin:")
            if self.pin_entry is None:
                self.pin_entry = tk.Entry(self.login_frame, show="*")
                self.pin_entry.pack()
            if self.login_button is None:
                self.login_button = tk.Button(self.login_frame, text="Entrar", command=self.validate_pin)
                self.login_button.pack(pady=5)
        else:
            self.pin_label.config(text="")
            if self.pin_entry is not None:
                self.pin_entry.destroy()
                self.pin_entry=None
            if self.login_button is not None:
                self.login_button.destroy()
                self.login_button = None
    def validate_pin(self):
        account = self.accounts[self.account_var.get()]
        pin_ingresado = self.pin_entry.get()
        if account.validate_pin(pin_ingresado):
            messagebox.showinfo("Acceso concedido", f"Bienvenido/a {account.first_name}!")
            self.current_account = account
            self.clear_login()
            self.show_menu()
        else:
            messagebox.showerror("PIN incorrecto", "La información ingresada no es válida, por favor intente de nuevo")
            self.pin_entry.delete(0, tk.END)

    def clear_login(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()
        self.login_frame.pack_forget()
    def show_balance(self): 
        balance = self.current_account.balance
        messagebox.showinfo("Saldo", f"El saldo actual es: ${balance:.2f}")
    def prepare_deposit(self):
        self.clear_operation_frame()
        self.operation_frame = tk.Frame(self.menu_frame)
        self.operation_frame.pack(pady=10)
        tk.Label(self.operation_frame, text="Monto a depositar:").pack()
        amount_entry = tk.Entry(self.operation_frame)
        amount_entry.pack()
        tk.Button(self.operation_frame, text="Confirmar", command=lambda: self.do_deposit(amount_entry)).pack(pady=5)
    def do_deposit(self, entry_widget):
        try:
            monto = float(entry_widget.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
                return
            self.current_account.deposit(monto)
            messagebox.showinfo("Éxito", f"Depósito de ${monto:.2f} realizado.\nNuevo saldo: ${self.current_account.balance:.2f}")
            self.clear_operation_frame()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")
    def prepare_withdraw(self):
        self.clear_operation_frame()
        self.operation_frame = tk.Frame(self.menu_frame)
        self.operation_frame.pack(pady=10)
        tk.Label(self.operation_frame, text="Monto a retirar:").pack()
        amount_entry = tk.Entry(self.operation_frame)
        amount_entry.pack()
        tk.Button(self.operation_frame, text="Confirmar", command=lambda: self.do_withdraw(amount_entry)).pack(pady=5)
    def do_withdraw(self, entry_widget):
        try:
            monto = float(entry_widget.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0.")
                return
            if monto > self.current_account.balance:
                messagebox.showerror("Error", f"El monto no puede ser mayor al saldo actual (${self.current_account.balance:.2f}).")
                return
            if self.current_account.withdraw(monto):
                messagebox.showinfo("Éxito", f"Retiro de ${monto:.2f} realizado.\nNuevo saldo: ${self.current_account.balance:.2f}")
                self.clear_operation_frame()
            else:
                messagebox.showerror("Error", "No fue posible realizar el retiro. Verifique el monto y el saldo.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")
    def prepare_transfer(self):
        self.clear_operation_frame()
        self.operation_frame = tk.Frame(self.menu_frame)
        self.operation_frame.pack(pady=10)
        tk.Label(self.operation_frame, text="Cuenta destino:").pack()
        available_accounts= [k for k in self.accounts.keys()if k != str(self.current_account.account_id) and k !="Selecciona la cuenta"]
        account_var=tk.StringVar()
        account_menu=tk.OptionMenu(self.operation_frame,account_var, *available_accounts)
        account_menu.pack()
        tk.Label(self.operation_frame,text="Monto a transferir:").pack()
        amount_entry = tk.Entry(self.operation_frame)
        amount_entry.pack()
        tk.Button(self.operation_frame, text="Confirmar", command=lambda: self.do_transfer(account_var,amount_entry)).pack(pady=5)
    def do_transfer(self, cuenta_var, entry_widget):
        cuenta_destino_key = cuenta_var.get()
        if not cuenta_destino_key:
            messagebox.showerror("Error", "Seleccione una cuenta destino.")
            return
        try:
            monto = float(entry_widget.get())
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a 0.")
                return
            if monto > self.current_account.balance:
                messagebox.showerror("Error", f"El monto no puede ser mayor al saldo actual (${self.current_account.balance:.2f}).")
                return
            cuenta_destino = self.accounts[cuenta_destino_key]
            if self.current_account.account_id == cuenta_destino.account_id:
                messagebox.showerror("Error", "No puede transferir a la misma cuenta.")
                return
            self.current_account.transfer(cuenta_destino, monto)
            messagebox.showinfo("Éxito", f"Transferencia de ${monto:.2f} a {cuenta_destino.first_name} realizada.\nNuevo saldo: ${self.current_account.balance:.2f}")
            self.clear_operation_frame()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")
    def show_history(self):
        self.clear_operation_frame()
        self.operation_frame = tk.Frame(self.menu_frame)
        self.operation_frame.pack(pady=10)
        tk.Label(self.operation_frame, text="Últimos 5 movimientos:").pack()

        history_box = tk.Text(self.operation_frame, width=50, height=10)
        history_box.pack()
        for trans in self.current_account.history:
            line = f"{trans['Fecha']} - {trans['Tipo de transacción']}: ${trans['Monto']} (Saldo: ${trans['Saldo']})"
            if trans.get('Cuenta destino'):
                line += f" [Cuenta destino: {trans['Cuenta destino']}]"
            line += "\n"
            history_box.insert(tk.END, line)

        history_box.config(state=tk.DISABLED)

    def clear_operation_frame(self):
        if hasattr(self, "operation_frame") and self.operation_frame:
            self.operation_frame.destroy()
            self.operation_frame = None
    def show_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(padx=10, pady=10)
        tk.Label(self.menu_frame, text=f"Bienvenido/a, {self.current_account.first_name}").pack(pady=5)
        tk.Button(self.menu_frame, text="Consultar saldo", command=self.show_balance).pack(fill='x')
        tk.Button(self.menu_frame, text="Depositar", command=self.prepare_deposit).pack(fill='x')
        tk.Button(self.menu_frame, text="Retirar", command=self.prepare_withdraw).pack(fill='x')
        tk.Button(self.menu_frame, text="Transferir", command=self.prepare_transfer).pack(fill='x')
        tk.Button(self.menu_frame, text="Ver historial", command=self.show_history).pack(fill='x')



root = tk.Tk()
root.geometry("500x500")
Interface(root, cuenta_patito)
root.mainloop() 

