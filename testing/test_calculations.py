import pytest
from ..app.calculations import add, subtract, multiply, divide, BankAccount, InsufficentFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def init_val_bank_account():
    return BankAccount(10)


@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (0, 4, 4),
    (8, 9, 17),
    (10, 100, 110)
])
def test_add(num1, num2, expected):
    print("Testing addition")
    assert add(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, -1),
    (0, 4, -4),
    (8, 9, -1),
    (10, 100, -90)
])
def test_subtract(num1, num2, expected):
    print("Testing subtraction")
    assert subtract(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 6),
    (0, 4, 0),
    (8, 9, 72),
    (10, 100, 1000)
])
def test_multiply(num1, num2, expected):
    print("Testing multiplication")
    assert multiply(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (6, 3, 2),
    (0, 4, 0),
    (72, 9, 8),
    (1000, 100, 10)
])
def test_divide(num1, num2, expected):
    print("Testing division")
    assert divide(num1, num2) == expected


def test_bankaccount():
    print("Testing bank account")
    account = BankAccount()
    account2 = BankAccount(10)
    account2.collect_interest()
    assert account.balance == 0
    account.deposit(20)
    assert account.balance == 20
    assert account2.balance == 11
    account2.withdraw(10)
    assert account2.balance == 1


def test_zero_bank_account(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_init_val_bank_account(init_val_bank_account):
    assert init_val_bank_account.balance == 10


@pytest.mark.parametrize("depositAmount, withdrawAmount, expected", [
    (100, 50, 50),
    (300, 20, 280),
])
def test_bank_transaction(zero_bank_account, depositAmount, withdrawAmount, expected):
    print("Testing bank transaction")
    zero_bank_account.deposit(depositAmount)
    zero_bank_account.withdraw(withdrawAmount)

    assert zero_bank_account.balance == expected


def test_bank_transaction_exception(init_val_bank_account):
    with pytest.raises(InsufficentFunds):
        init_val_bank_account.withdraw(100)
