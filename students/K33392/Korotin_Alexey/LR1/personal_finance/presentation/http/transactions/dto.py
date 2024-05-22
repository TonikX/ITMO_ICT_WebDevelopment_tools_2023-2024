from datetime import datetime

from pydantic import BaseModel

from personal_finance.application.users.dto import ReadUserDto
from personal_finance.domain.finance import Currency
from personal_finance.domain.transaction.transaction import TransactionType, TransactionStatus
from personal_finance.presentation.http.accounts.dto import AccountReadDto
from personal_finance.presentation.http.users.dto import UserReadDto


class TransactionReadDto(BaseModel):
    id: int
    transaction_type: TransactionType
    status: TransactionStatus
    comment: str
    user: UserReadDto
    timestamp: datetime
    currency: str
    amount: int


class TransactionWriteDto(BaseModel):
    comment: str
    timestamp: datetime
    currency: Currency
    amount: int


class TransferTransactionReadDto(TransactionReadDto):
    source: AccountReadDto
    destination: AccountReadDto


class TransferTransactionWriteDto(TransactionWriteDto):
    source_id: int
    destination_id: int
