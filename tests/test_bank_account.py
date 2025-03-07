import pytest
from practicas.bank_account import BankAccount

"""
The goal of this practice is to implement a simple BankAccount class that
supports the following operations:
- Create a new account with an owner and an initial balance.
- Get the owner of the account.
- Get the current balance of the account.
- Deposit money into the account.
- Withdraw money from the account.

To run these tests, use the following command:
    pytest -x -v tests/test_bank_account.py

The -x flag stops the test run after the first failure.
The -v flag increases verbosity.
Optional: the --ff flag runs the last failing test first.

This can be configured as default in the pyproject.toml file:
    [tool.pytest.ini_options]
    addopts = ["-vx"]
    testpaths = ["tests"]

The tests are run and code is modified to solve the reported error. After that,
tests are run again to check if the error was solved. This process is repeated
until all tests pass.

For instance, when running tests for the first time, the following error is
reported:

    tests/test_bank_account.py:17: in <module>
        from practicas.bank_account import BankAccount
    E   ModuleNotFoundError: No module named 'practicas.bank_account'

This error is solved by creating the practicas package and the bank_account
module inside it. After that, tests are run again to check if the error was
solved.

The main idea is to write only the necessary code to make the tests pass, guided
by the error messages.
"""


@pytest.fixture
def bank_account():
    """Fixture to create a BankAccount object"""
    return BankAccount("Pedro")


def test_owner_is_set():
    """Test that the owner is correctly set when creating a new account"""
    account = BankAccount("Ana")
    assert account.get_owner() == "Ana"


def test_initial_balance_defaults_to_0(bank_account):
    """Test that a new account has the correct initial balance"""
    assert bank_account.get_balance() == 0


def test_initial_balance_can_be_set():
    """Test that the initial balance can be set when creating a new account"""
    account = BankAccount("Pedro", initial_balance=100)
    assert account.get_balance() == 100


def test_initial_balance_is_non_negative():
    """Test that the initial balance must be non-negative"""
    with pytest.raises(ValueError):
        BankAccount("Pedro", initial_balance=-100)


def test_deposit(bank_account):
    """Test that depositing money increases the balance"""
    bank_account.deposit(100)
    assert bank_account.get_balance() == 100


def test_negative_deposit_raises_exception(bank_account):
    """Test that depositing a negative amount raises an exception"""
    with pytest.raises(ValueError):
        bank_account.deposit(-100)


def test_deposit_with_zero_amount_raises_exception(bank_account):
    """Test that depositing zero amount raises an exception"""
    with pytest.raises(ValueError):
        bank_account.deposit(0)


def test_withdraw_is_successful(bank_account):
    """Test that withdrawing money decreases the balance"""
    bank_account.deposit(100)
    bank_account.withdraw(50)
    assert bank_account.get_balance() == 50


def test_withdraw_insufficient_funds(bank_account):
    """Test that withdrawing more money than the account has raises an exception"""
    bank_account.deposit(100)
    with pytest.raises(ValueError):
        bank_account.withdraw(200)


def test_withdraw_negative_amount_raises_exception(bank_account):
    """Test that withdrawing a negative amount raises an exception"""
    bank_account.deposit(100)
    with pytest.raises(ValueError):
        bank_account.withdraw(-100)


def test_withdraw_with_zero_amount_raises_exception(bank_account):
    """Test that withdrawing zero amount raises an exception"""
    bank_account.deposit(100)
    with pytest.raises(ValueError):
        bank_account.withdraw(0)
