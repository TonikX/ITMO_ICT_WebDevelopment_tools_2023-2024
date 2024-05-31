from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette import status

from personal_finance.application.auth.service import get_current_user
from personal_finance.application.cashflow.dto import WriteCashFlowDto, ReadCashFlowDto
from personal_finance.application.cashflow.service import IncomeSourceService, ExpenseCategoryService
from personal_finance.application.exceptions import NotFoundException
from personal_finance.application.users.dto import ReadUserDto
from personal_finance.infrastructure.persistance.postgres.cashflow.repository import IncomeSourceRepository, \
    ExpenseCategoryRepository
from personal_finance.infrastructure.persistance.postgres.database import get_session
from personal_finance.presentation.http.cashflows.dto import CashFlowCreateDto, CashFlowReadDto

source = APIRouter()
category = APIRouter()


def get_source_service(session: Session = Depends(get_session)) -> IncomeSourceService:
    return IncomeSourceService(IncomeSourceRepository(session))


def get_category_service(session: Session = Depends(get_session)) -> ExpenseCategoryService:
    return ExpenseCategoryService(ExpenseCategoryRepository(session))


@source.post('/', status_code=status.HTTP_201_CREATED)
def create_income_source(dto: CashFlowCreateDto, service: IncomeSourceService = Depends(get_source_service),
                         user: ReadUserDto = Depends(get_current_user)) -> CashFlowReadDto:
    dto = CashFlowCreateDto.validate(dto)
    write: WriteCashFlowDto = WriteCashFlowDto(**dto.model_dump(), user=user)

    s: ReadCashFlowDto = service.save(write)
    return CashFlowReadDto(**s.model_dump())


@source.get('/{id}', status_code=status.HTTP_200_OK)
def get_income_source(id: int, service: IncomeSourceService = Depends(get_source_service)) -> CashFlowReadDto:
    try:
        s: ReadCashFlowDto = service.find_by_id(id)
        return CashFlowReadDto(**s.model_dump())
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@source.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_income_source(id: int, service: IncomeSourceService = Depends(get_source_service)) -> None:
    try:
        service.delete_by_id(id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@category.post('/', status_code=status.HTTP_201_CREATED)
def create_expense_category(dto: CashFlowCreateDto, service: ExpenseCategoryService = Depends(get_category_service),
                         user: ReadUserDto = Depends(get_current_user)) -> CashFlowReadDto:
    dto = CashFlowCreateDto.validate(dto)
    write: WriteCashFlowDto = WriteCashFlowDto(**dto.model_dump(), user=user)

    s: ReadCashFlowDto = service.save(write)
    return CashFlowReadDto(**s.model_dump())


@category.get('/{id}', status_code=status.HTTP_200_OK)
def get_expense_category(id: int, service: ExpenseCategoryService = Depends(get_category_service)) -> CashFlowReadDto:
    try:
        s: ReadCashFlowDto = service.find_by_id(id)
        return CashFlowReadDto(**s.model_dump())
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@category.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_category(id: int, service: ExpenseCategoryService = Depends(get_category_service)) -> None:
    try:
        service.delete_by_id(id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
