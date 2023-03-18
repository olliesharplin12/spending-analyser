from enum import Enum


class TransactionType(Enum):
    AUTOMATIC_PAYMENT = "Automatic Payment"
    BILL_PAYMENT = "Bill Payment"
    DEPOSIT = "Deposit"
    DIRECT_CREDIT = "Direct Credit"
    EFT_POS = "Eft-Pos"
    PAYMENT = "Payment"
    SALARY = "Salary"
    TRANSFER = "Transfer"
    VISA_PURCHASE = "Visa Purchase"
    VISA_REFUND = "Visa Refund"


EXPENSE_TRANSACTION_TYPES = [
    TransactionType.AUTOMATIC_PAYMENT.value,
    TransactionType.BILL_PAYMENT.value,
    TransactionType.DIRECT_CREDIT.value,
    TransactionType.EFT_POS.value,
    TransactionType.PAYMENT.value,
    TransactionType.TRANSFER.value,
    TransactionType.VISA_PURCHASE.value,
    TransactionType.VISA_REFUND.value,
]


class Transaction:
    def __init__(self, transaction_type, details, particulars, code, reference, amount, date, foreign_currency_amount, conversion_charge):
        # TODO: Set empty string values to None, could be done in parsing step.
        self.id = None
        self.transaction_type = transaction_type
        self.details = details
        self.particulars = particulars
        self.code = code
        self.reference = reference
        self.amount = amount
        self.date = date
        self.foreign_currency_amount = foreign_currency_amount
        self.conversion_charge = conversion_charge

        if transaction_type == TransactionType.AUTOMATIC_PAYMENT.value:
            self.title = f"{details} - {particulars} {code} {reference}"
        elif transaction_type == TransactionType.BILL_PAYMENT.value:
            self.title = details
        elif transaction_type == TransactionType.DEPOSIT.value:
            self.title = details
        elif transaction_type == TransactionType.DIRECT_CREDIT.value:
            self.title = f"{details} - {particulars} {code} {reference}"
        elif transaction_type == TransactionType.EFT_POS.value:
            self.title = details
        elif transaction_type == TransactionType.PAYMENT.value:
            self.title = f"{details} - {particulars} {code} {reference}"
        elif transaction_type == TransactionType.SALARY.value:
            self.title = details
        elif transaction_type == TransactionType.TRANSFER.value:
            self.title = f"{details} - {particulars} {code} {reference}"
        elif transaction_type == TransactionType.VISA_PURCHASE.value:
            self.title = code
        elif transaction_type == TransactionType.VISA_REFUND.value:
            self.title = code
        else:
            print(f"Warning: Unknown transaction type '{transaction_type}'")
    
    def set_category_id(self, category_id):
        self.category_id = category_id
    
    def set_id(self, id):
        self.id = id
    
    def is_expense(self):
        return self.transaction_type in EXPENSE_TRANSACTION_TYPES

    def __eq__(self, other):
        if isinstance(other, Transaction):
            return (self.transaction_type == other.transaction_type and
                self.details == other.details and
                self.particulars == other.particulars and
                self.code == other.code and
                self.reference == other.reference and
                self.amount == other.amount and
                self.date == other.date and
                self.foreign_currency_amount == other.foreign_currency_amount and
                self.conversion_charge == other.conversion_charge
            )
        else:
            return False

    def __str__(self):
        return f"{self.transaction_type}, {self.details}, {self.particulars}, {self.code}, {self.reference}, {self.amount}, {self.date}, {self.foreign_currency_amount}, {self.conversion_charge}"
