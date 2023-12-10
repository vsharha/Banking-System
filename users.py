import csv
import os

from pwinput import pwinput

alnum = "abcdefghijklmnopqrtsuvwxyz1234567890"
acceptable_email_chars = alnum + "_.@"
acceptable_password_chars = alnum + "!_$#@*"

def is_valid_name(name):
    if "," in name:
        return False
    return True

def is_valid_email(email):
    if not email.islower():
        return False
    if "," in email or " " in email:
        return False
    if any(char.lower() not in acceptable_email_chars for char in email):
        return False
    if email.count("@") != 1 or "." not in email:
        return False
    if email.index("@") > email.index("."):
        return False
    return True

def is_valid_password(password):
    if "," in password or " " in password:
        return False
    if any(char.lower() not in acceptable_password_chars for char in password):
        return False
    return True

def is_valid_user(user):
    return is_valid_name(user.name) and is_valid_email(user.email) and is_valid_password(user.password)

class User:
    fieldnames = ("Name", "Email", "Password", "Balance")
    def __init__(self, name = "", email = "", password = "", balance = 0.0):
        self.name = name
        self.email = email
        self.password = password
        self.__balance = balance
    def __str__(self):
        return f"Account object with {self.email}"
    def __repr__(self):
        return self.__str__()

    def get_balance(self):
        return self.__balance

    def deposit(self, deposit_amount):
        if deposit_amount < 0:
            print("Invalid amount")
            return False
        self.__balance += deposit_amount
        return True
    
    def withdraw(self, withdraw_amount):
        if withdraw_amount < 0:
            print("Invalid amount")
            return False
        if self.__balance < withdraw_amount:
            print("Insufficient funds")
            return False
        self.__balance -= withdraw_amount
        return True
        
    def take_valid_name(self):
        while True:
            name = input("Name > ")
            if is_valid_name(name):
                self.name = name
                break
            print("Invalid name")
            
    def take_valid_email(self, users):
        while True:
            email = input("Email > ").casefold()
            if not is_valid_email(email):
                print("Invalid email")
            elif users.get_user_by_email(email):
                print("User exists")
            else:
                self.email = email
                break
                
    def take_valid_password(self):
        while True:
            password = input("Password > ")
            if is_valid_password(password):
                while True:
                    repeat_password = input("Repeat password > ")
                    if password == repeat_password:
                        self.password = password
                        break
                    print("Passwords don't match")
                break
            print("Invalid password")
            
    def take_valid_user(self, users):
        self.take_valid_name()
        self.take_valid_email(users)
        self.take_valid_password()
        
    def get_zip(self):
        return dict(zip(self.fieldnames, [self.name, self.email, self.password, self.__balance], strict = True))
    
class Users:
    def __init__(self, file_name):
        self.__file_name = ""
        self.__users = []
        self.__current_user = None
        self.read_users_from_csv(file_name)
    def __str__(self):
        return_str = ""
        if self.__current_user:
            return_str += f"Logged in as {self.__current_user.name}"
        else:
            return_str += "Not logged in"
        return_str += f"\n{self.__file_name}\n"
        for user in self.__users:
            return_str += user.__str__() + "\n"
        return return_str
    def __repr__(self):
        return self.__str__()        

    def read_users_from_csv(self, file_name):
        self.__file_name = file_name
        self.__users = []
        
        with open(file_name, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                user = User(
                    row["Name"],
                    row["Email"],
                    row["Password"],
                    float(row["Balance"])
                )

                if not self.get_user_by_email(user.email):
                    self.__users.append(user)

        if not self.get_user_by_email(self.get_current_user_email):
            self.__current_user = None

    def update_csv(self):
        with open(self.__file_name, "w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=User.fieldnames)
            csv_writer.writeheader()

            for user in self.__users:
                csv_writer.writerow(user.get_zip())

    def add_user(self, user):
        if self.get_user_by_email(user.email) or not is_valid_user(user):
            return

        self.__users.append(user)
        
        with open(self.__file_name, "a+") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=User.fieldnames)
            if os.path.getsize(self.__file_name) == 0:
                csv_writer.writeheader()
            csv_writer.writerow(user.get_zip())
    
    def get_user_by_email(self, email):
        email = email.casefold()
        for user in self.__users:
            if email == user.email:
                return user
        return None
    
    def logged_in(self):
        return self.__current_user is not None

    def get_current_user_email(self):
        return self.__current_user.email

    def get_current_user_balance(self):
        print(f"You have £{self.__current_user.get_balance()}")
    
    def log_in(self):
        while True:
            email = input("Email > ").casefold()
            user = self.get_user_by_email(email)
    
            if user:
                break
            print("Email not registered")

        while True:
            password = pwinput("Password > ")
            
            if user.password == password:
                break
            print("Invalid password") 

        print("Welcome,", user.name)
        self.__current_user = user

    def log_out(self):
        if not self.logged_in():
            print("Not logged in")
            return
        
        op = input("Are you sure? [Y/y, N/n] > ").casefold()

        if op == 'y':
            print("Logging out")
            self.__current_user = None
        else:
            print("Staying logged in")
    
    def sign_up(self):
        user = User()

        user.take_valid_user(self)
        
        self.add_user(user)
        self.__current_user = user
        print("Signed up successfully.")

    def edit(self):
        if not self.logged_in():
            print("Not logged in")
            return

        while True:
            op = int(input("What would you like to edit? (1 - name, 2 - email, 3 - password, 0 - CANCEL) > "))
    
            user = self.__current_user

            match(op):
                case 1:
                    print(user.name)
                    user.take_valid_name()
                case 2:
                    print(user.email)
                    user.take_valid_email(self)
                case 3:
                    user.take_valid_password()
                case 0:
                    return
                case _:
                    print("Invalid input")
                    continue

            self.__current_user = user
            self.__users[self.__users.index(user)] = user
            self.update_csv()
            break

    def transfer(self):
        if not self.logged_in():
            print("Not logged in")
            return

        while True:
            email = input("Who would you like to transfer to? (0 - CANCEL) > ")
            
            if email == '0':
                return
    
            user = self.get_user_by_email(email)
    
            if user:
                print(f"TRANSFERRING TO {email}")
                break
            print("Email not registered")
            
                
        while True:
            self.get_current_user_balance()
            amount = float(input("What amount would you like to transfer? > "))
            if amount >= 0:
                break
            print("Invalid input")

        if self.__current_user.withdraw(amount):
            user.deposit(amount)
            self.update_csv()

            self.get_current_user_balance()

    def handle_deposit_withdraw(self):
        if not self.logged_in():
            print("Not logged in")
            return

        self.get_current_user_balance()

        op = int(input("Would you like to deposit or withdraw? (1 - deposit, 2 - withdraw, 0 - CANCEL) > "))
        
        if op == 0:
            return

        while True:
            amount = float(input("Enter the amount > £"))
            if amount >= 0:
                break
            print("Invalid value")

        match(op):
            case 1:
                self.__current_user.deposit(amount)
            case 2:
                self.__current_user.withdraw(amount)
            case _:
                print("Invalid input")
                return

        self.update_csv()
        
        self.get_current_user_balance()