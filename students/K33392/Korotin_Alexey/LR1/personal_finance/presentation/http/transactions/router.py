from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status

from personal_finance.application.auth.service import get_current_user
from personal_finance.application.transactions.dto import WriteTransferTransactionDto, ReadTransferTransactionDto
from personal_finance.application.transactions.service import TransferTransactionService
from personal_finance.application.users.dto import ReadUserDto
from personal_finance.domain.transaction.transaction import TransactionType, TransactionStatus
from personal_finance.infrastructure.persistance.postgres.database import get_session
from personal_finance.infrastructure.persistance.postgres.transaction.repository import TransferTransactionRepository
from personal_finance.presentation.http.transactions.dto import TransferTransactionWriteDto, TransferTransactionReadDto

transfer = APIRouter()


def _get_service(session: Session = Depends(get_session)) -> TransferTransactionService:
    return TransferTransactionService(TransferTransactionRepository(session))


@transfer.post("/", status_code=status.HTTP_201_CREATED)
def create_transfer(dto: TransferTransactionWriteDto,
                    current_user: ReadUserDto = Depends(get_current_user),
                    service: TransferTransactionService = Depends(_get_service)) -> TransferTransactionReadDto:
    dto = TransferTransactionWriteDto.validate(dto)
    write: WriteTransferTransactionDto = WriteTransferTransactionDto(**dto.model_dump(),
                                                                     user=current_user,
                                                                     transaction_type=TransactionType.TRANSFER,
                                                                     status=TransactionStatus.DRAFT)

    transaction: ReadTransferTransactionDto = service.save(write)
    return TransferTransactionReadDto(**transaction.model_dump())
