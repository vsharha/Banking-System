import os

from users import Users

FILE_NAME = "users.csv"

def menu(users):
    if not users.logged_in():
        print("+== Menu ==+")
        print("1. Log in")
        print("2. Sign up")
    else:
        print(f"Logged in as {users.get_current_user_email()}")
        print("+== Menu ==+")
        print("1. View balance")
        print("2. Deposit or withdraw")
        print("3. Transfer")
        print("4. Edit account details")
        print("5. Log out")
        
    print()
    op = int(input("> "))
    print()

    if not users.logged_in():
        match(op):
            case 1:
                users.log_in()
            case 2:
                users.sign_up()
            case _:
                print("Invalid input")
    else:
        match(op):
            case 1:
                users.get_current_user_balance()
            case 2:
                users.handle_deposit_withdraw()
            case 3:
                users.transfer()
            case 4:
                users.edit()
            case 5:
                users.log_out()
            case _:
                print("Invalid input")

# TODO:
# + Add edit
# + Add balance
# + Add deposit
# + Add withdraw
# + Add transfer
# Add password hint

if __name__ == "__main__":
    users = Users(FILE_NAME)

    while True:
        menu(users)
        
        input("Press any key to continue... ")
        os.system("clear")