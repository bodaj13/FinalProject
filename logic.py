import csv
from PyQt6.QtWidgets import *
from gui import *
from accounts import *


class Logic(QMainWindow, Ui_MainWindow):
    """
    Class to control how the GUI functions.
    """

    def __init__(self):
        """
        Constructor.
        Sets GUI to page 0.
        Sets an instance of the Checking and SavingsAccount class.
        Sets current account selected to None.
        Sets how each button click functions.
        """
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)

        self.input_pin.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pin.setMaxLength(4)

        self.checking = CheckingAccount('')
        self.savings = SavingsAccount('')
        self.current_account = None

        self.current_first_name: str = ''
        self.current_last_name: str = ''
        self.current_pin: str = ''

        self.button_start.clicked.connect(lambda: self.start_button())

        self.button_enter.clicked.connect(lambda: self.account_enter_button())
        self.button_cancel.clicked.connect(lambda: self.account_cancel_button())
        self.button_clear.clicked.connect(self.account_clear_button)

        self.button_checking.clicked.connect(lambda: self.selected_account('Checking'))
        self.button_savings.clicked.connect(lambda: self.selected_account('Savings'))
        self.button_exitAccountSelect.clicked.connect(lambda: self.account_exit_button())

        self.button_withdraw.clicked.connect(lambda: self.withdraw_button())
        self.button_deposit.clicked.connect(lambda: self.deposit_button())
        self.button_balance.clicked.connect(lambda: self.balance_button())
        self.button_exitTransaction.clicked.connect(lambda: self.exit_transaction_button())

        self.button_submitWithdraw.clicked.connect(lambda: self.withdraw_submit_button())
        self.button_exitWithdraw.clicked.connect(lambda: self.withdraw_exit_button())

        self.button_submitDeposit.clicked.connect(lambda: self.deposit_submit_button())
        self.button_exitDeposit.clicked.connect(lambda: self.deposit_exit_button())

        self.button_exitBalance.clicked.connect(lambda: self.balance_exit_button())

        self.button_startOver.clicked.connect(lambda: self.start_over_button())

    def start_button(self):
        """
        Sets GUI to page 1 when the start button is clicked.
        """
        self.stackedWidget.setCurrentIndex(1)

    def account_enter_button(self):
        """
        Logic for what happens when the enter button is clicked on the Accounts Info page.
        Verifies the user login against the users.csv and sets the first name, last name and account balances.
        """

        first_name: str = self.input_firstName.text().strip()
        last_name: str = self.input_lastName.text().strip()
        full_name: str = f'{first_name} {last_name}'.strip()
        pin: str = self.input_pin.text()
        successful_login: bool = False
        checking_balance: float = 0.0
        savings_balance: float = 0.0

        if first_name == '' and last_name == '' and pin == '':
            QMessageBox.warning(self, 'Warning', 'Please enter account information.')
        elif first_name == '' and last_name == "":
            QMessageBox.warning(self, 'Warning', 'Please enter first and last name.')
        elif first_name == '':
            QMessageBox.warning(self, 'Warning', 'Please enter first name.')
        elif last_name == '':
            QMessageBox.warning(self, 'Warning', 'Please enter last name.')
        elif pin == '':
            QMessageBox.warning(self, 'Warning', 'Please enter pin.')
        elif pin.isalpha():
            QMessageBox.warning(self, 'Warning', 'Invalid pin.')
        elif len(pin) < 4:
            QMessageBox.warning(self, 'Warning', 'Pin must be 4 digits.')

        try:
            with open('users.csv', 'r') as csv_file:
                content = csv.reader(csv_file)
                next(content)

                for line in content:
                    csv_first_name = line[0].strip()
                    csv_last_name = line[1].strip()
                    csv_pin = line[2].strip()

                    if first_name.lower() == csv_first_name and last_name.lower() == csv_last_name and pin == csv_pin:
                        successful_login = True
                        checking_balance = float(line[3])
                        savings_balance = float(line[4])

                        self.current_first_name = csv_first_name
                        self.current_last_name = csv_last_name
                        self.current_pin = csv_pin
                        break

        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'User file not found.')

        if successful_login:
            self.checking.set_name(full_name)
            self.savings.set_name(full_name)
            self.checking.set_balance(checking_balance)
            self.savings.set_balance(savings_balance)
            self.label_welcomeName.setText(f'Welcome {full_name}!')
            self.stackedWidget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Warning', "Invalid Name or Pin.")

    def account_cancel_button(self):
        """
        Sets GUI to page 7 when the cancel button is clicked on the Accounts Info page.
        """
        self.stackedWidget.setCurrentIndex(7)

    def account_clear_button(self):
        """
        Clears the text boxes on the Accounts Info page when the clear button is clicked.
        """
        self.input_firstName.clear()
        self.input_lastName.clear()
        self.input_pin.clear()

    def selected_account(self, account_type: object):
        """
        Determines which account type is selected and sets labels to match that account type.
        Sets GUI to page 3.
        :param account_type: checking or saving account type.
        """
        if account_type == 'Checking':
            self.current_account = self.checking
        else:
            self.current_account = self.savings

        self.label_accountTypeHeaderTransaction.setText(account_type)
        self.label_accountTypeHeaderWithdraw.setText(account_type)
        self.label_accountTypeHeaderDeposit.setText(account_type)
        self.label_accountTypeHeaderBalance.setText(account_type)

        self.stackedWidget.setCurrentIndex(3)

    def account_exit_button(self):
        """
        Sets the GUI to page 7 when the exit button is clicked on the Account Select page.
        """
        self.stackedWidget.setCurrentIndex(7)

    def withdraw_button(self):
        """
        Sets the GUI to page 4 when the Withdraw button is clicked on the Transaction Select page.
        """
        self.input_withdrawAmount.clear()
        self.label_withdrawMessage.setText('')
        self.update_balances()
        self.stackedWidget.setCurrentIndex(4)

    def deposit_button(self):
        """
        Sets the GUI to page 5 when the Deposit button is clicked on the Transaction Select page.
        """
        self.input_depositAmount.clear()
        self.label_depositMessage.setText('')
        self.update_balances()
        self.stackedWidget.setCurrentIndex(5)

    def balance_button(self):
        """
        Sets the GUI to page 6 when the Balance button is clicked on the Transaction Select page.
        """
        self.update_balances()
        self.stackedWidget.setCurrentIndex(6)

    def exit_transaction_button(self):
        """
        Sets the GUI to page 7 when the Exit button is clicked on the Transaction Select page.
        :return:
        """
        self.stackedWidget.setCurrentIndex(7)

    def withdraw_submit_button(self):
        """
        Logic for what happens when the submit button is clicked on the Withdraw page.
        """
        try:
            amount = float(self.input_withdrawAmount.text())
            if amount <= 0:
                QMessageBox.warning(self, 'Warning', 'Please enter a positive amount.')
                self.input_withdrawAmount.clear()
            elif self.current_account.withdraw(amount):
                self.label_withdrawMessage.setText(f'You have withdrawn ${amount:.2f}')
                self.update_balances()
                self.input_withdrawAmount.clear()
            else:
                QMessageBox.warning(self, 'Warning', 'Insufficient funds')
                self.input_withdrawAmount.clear()
        except ValueError:
            QMessageBox.warning(self, 'Warning', 'Please enter a valid number.')
            self.input_withdrawAmount.clear()

    def withdraw_exit_button(self):
        """
        Sets the GUI to page 7 when the Exit button is clicked on the Withdraw page.
        """
        self.stackedWidget.setCurrentIndex(7)

    def deposit_submit_button(self):
        """
        Logic for what happens when the submit button is clicked on the Deposit page.
        """
        try:
            amount = float(self.input_depositAmount.text())
            if amount <= 0:
                QMessageBox.warning(self, 'Warning', 'Please enter a positive amount.')
                self.input_depositAmount.clear()
            elif self.current_account.deposit(amount):
                self.label_depositMessage.setText(f'You have deposited ${amount:.2f}')
                self.update_balances()
                self.input_depositAmount.clear()
        except ValueError:
            QMessageBox.warning(self, 'Warning', 'Please enter a valid number.')
            self.input_depositAmount.clear()

    def deposit_exit_button(self):
        """
        Sets the GUI to page 7 when the Exit button is clicked on the Deposit page.
        :return:
        """
        self.stackedWidget.setCurrentIndex(7)

    def balance_exit_button(self):
        """
        Sets the GUI to page 7 when the Exit button is clicked on the Balance page.
        :return:
        """
        self.stackedWidget.setCurrentIndex(7)

    def start_over_button(self):
        """
        Clears the account fields when the start over button is clicked on the Thank You page.
        Sets the GUI to page 0
        """
        self.account_clear_button()
        self.current_account = None
        self.stackedWidget.setCurrentIndex(0)

    def update_balances(self):
        """
        Sets the balance on the GUI for the withdraw, deposit and balance pages by which account type is selected.
        Updates balance in users.csv.
        """
        if self.current_account:
            balance = f'Account Balance: ${self.current_account.get_balance():.2f}'
            self.label_accountBalanceWithdraw.setText(balance)
            self.label_accountBalanceDeposit.setText(balance)
            self.label_accountBalance.setText(balance)

            update_rows = []

            try:
                with open('users.csv', 'r') as csv_file:
                    content = csv.reader(csv_file)

                    header = next(content)
                    update_rows.append(header)

                    for line in content:
                        csv_first_name = line[0].strip()
                        csv_last_name = line[1].strip()
                        csv_pin = line[2].strip()

                        if csv_first_name == self.current_first_name and csv_last_name == self.current_last_name and csv_pin == self.current_pin:
                            line[3] = f'{self.checking.get_balance():.2f}'
                            line[4] = f'{self.savings.get_balance():.2f}'

                        update_rows.append(line)

                with open('users.csv', 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerows(update_rows)

            except FileNotFoundError:
                print('Error: users.csv file not found.')
