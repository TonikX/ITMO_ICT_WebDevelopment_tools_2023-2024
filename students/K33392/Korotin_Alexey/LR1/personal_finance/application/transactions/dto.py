from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Session

from personal_finance.application.accounts.dto import ReadAccountDto
from personal_finance.application.accounts.service import UserAccountService
from personal_finance.application.users.dto import ReadUserDto
from personal_finance.domain.finance import Currency, Money
from personal_finance.domain.transaction.transaction import TransactionType, TransactionStatus, TransferTransaction, \
    TransactionComment
from personal_finance.infrastructure.persistance.postgres.account.repository import UserAccountRepository
from personal_finance.infrastructure.persistance.postgres.database import get_session


def _get_account_service() -> UserAccountService:
    session: Session = next(get_session())
    return UserAccountService(UserAccountRepository(session))


class ReadTransactionDto(BaseModel):
    id: int
    transaction_type: TransactionType
    status: TransactionStatus
    comment: str
    user: ReadUserDto
    timestamp: datetime
    currency: str
    amount: int


class WriteTransactionDto(BaseModel):
    comment: str
    user: ReadUserDto
    timestamp: datetime
    currency: Currency
    amount: int


class ReadTransferTransactionDto(ReadTransactionDto):
    source: ReadAccountDto
    destination: ReadAccountDto

    @staticmethod
    def from_entity(transaction: TransferTransaction) -> "ReadTransferTransactionDto":
        return ReadTransferTransactionDto(
            id=transaction.id,
            transaction_type=transaction.transaction_type,
            status=transaction.status,
            comment=transaction.comment.value,
            user=ReadUserDto.from_entity(transaction.user),
            timestamp=datetime.now(),
            currency=transaction.money.currency,
            amount=transaction.money.amount,
            source=ReadAccountDto.from_entity(transaction.source),
            destination=ReadAccountDto.from_entity(transaction.destination)
        )


class WriteTransferTransactionDto(WriteTransactionDto):
    source_id: int
    destination_id: int

    def to_entity(self) -> TransferTransaction:
        service = _get_account_service()
        return TransferTransaction(
            None,
            TransactionStatus.DRAFT,
            TransactionComment(self.comment),
            self.user.to_entity(),
            Money(self.amount, self.currency),
            service.find_by_id(self.source_id).to_entity(),
            service.find_by_id(self.destination_id).to_entity()
        )

