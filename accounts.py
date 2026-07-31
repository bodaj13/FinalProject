class CheckingAccount:
    """
    Class to represent a checking account.
    """

    def __init__(self, name: str, balance: float = 0):
        """
        Constructor.
        :param name: name of the account.
        :param balance: balance of the account.
        """
        self.__account_name = name
        self.__account_balance = balance
        self.set_balance(self.__account_balance)

    def deposit(self, amount: float) -> bool:
        """
        Deposits an amount into the account.
        :param amount: amount to deposit
        :return: True if the deposit was successful, False if it was not successful.
        """
        if amount > 0:
            self.__account_balance += amount
            return True
        else:
            return False

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws an amount from the account.
        :param amount: amount to withdraw.
        :return: True if the withdrawal was successful, False if it was not successful.
        """
        if amount <= 0 or amount > self.__account_balance:
            return False
        else:
            self.__account_balance -= amount
            return True

    def get_balance(self) -> float:
        """
        Returns the balance of the account.
        :return: balance of the account as a float.
        """
        return self.__account_balance

    def get_name(self) -> str:
        """
        Returns the name of the account.
        :return: Name of the account as a string.
        """
        return self.__account_name

    def set_balance(self, value: float):
        """
        Sets the balance of the account.
        :param value: balance of the account.
        """
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def set_name(self, value):
        """
        Sets the name of the account.
        :param value: name of the account.
        """
        self.__account_name = value


class SavingsAccount(CheckingAccount):
    """
    Class to represent a savings account.
    """
    MINIMUM: float = 100
    RATE: float = 0.02

    def __init__(self, name: str):
        """
        Constructor.
        :param name: name of the account.
        """
        super().__init__(name, SavingsAccount.MINIMUM)
        self.__deposit_count = 0

    def apply_interest(self):
        """
        Applies the interest rate to the savings account.
        """
        x = self.get_balance() + (self.get_balance() * SavingsAccount.RATE)
        self.set_balance(x)

    def deposit(self, amount: float) -> bool:
        """
        Deposits an amount into the account.
        :param amount: amount to deposit.
        :return: True if the deposit was successful, False if it was not successful.
        """
        success = super().deposit(amount)

        if success:
            self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
        return success

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws an amount from the account.
        :param amount: amount to withdraw.
        :return: True if the withdrawal was successful, False if it was not successful.
        """
        if amount <= 0 or (self.get_balance() - amount) < SavingsAccount.MINIMUM:
            return False
        else:
            x = self.get_balance() - amount
            self.set_balance(x)
            return True

    def set_balance(self, value: float):
        """
        Sets the balance of the account.
        :param value: balance of the account.
        """
        if value < SavingsAccount.MINIMUM:
            super().set_balance(SavingsAccount.MINIMUM)
        else:
            super().set_balance(value)
