from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from personal_finance.application.accounts.dto import ReadAccountDto, WriteAccountDto
from personal_finance.application.accounts.service import UserAccountService
from personal_finance.application.auth.service import get_current_user
from personal_finance.application.exceptions import NotFoundException
from personal_finance.application.users.dto import ReadUserDto
from personal_finance.domain.account.account import UserAccount
from personal_finance.infrastructure.persistance.postgres.account.model import TagModel, AccountTagModel
from personal_finance.infrastructure.persistance.postgres.account.repository import UserAccountRepository
from personal_finance.infrastructure.persistance.postgres.database import get_session
from personal_finance.presentation.http.accounts.dto import AccountCreateDto, AccountReadDto, TagCreateDto, TagReadDto, \
    AccountTagCreateDto, AccountTagReadDto

account_router = APIRouter()


def get_service(session: Session = Depends(get_session)) -> UserAccountService:
    return UserAccountService(UserAccountRepository(session))


@account_router.post('/', status_code=status.HTTP_201_CREATED)
def create_account(dto: AccountCreateDto, user: ReadUserDto = Depends(get_current_user),
                   service: UserAccountService = Depends(get_service)) -> AccountReadDto:
    dto = AccountCreateDto.validate(dto)

    write_dto: WriteAccountDto = WriteAccountDto(user=user, name=dto.name, balance=dto.balance, currency=dto.currency)
    account: ReadAccountDto = service.save(write_dto)
    return AccountReadDto(**account.model_dump())


@account_router.get('/{id}', status_code=status.HTTP_200_OK)
def get_account(id: int, service: UserAccountService = Depends(get_service)) -> AccountReadDto:
    try:
        account: ReadAccountDto = service.find_by_id(id)
        return AccountReadDto(**account.model_dump())
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@account_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(id: int, service: UserAccountService = Depends(get_service)) -> None:
    try:
        service.delete_by_id(id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@account_router.post("/tags", status_code=status.HTTP_201_CREATED)
def add_tag(dto: AccountTagCreateDto, session: Session = Depends(get_session)) -> AccountTagReadDto:
    dto = AccountTagCreateDto.validate(dto)
    model: AccountTagModel = AccountTagModel(account_id=dto.account_id, tag_id=dto.tag_id, order=dto.order)
    session.add(model)
    session.commit()
    session.refresh(model)

    tag_dto: TagReadDto = TagReadDto(id=model.tag.id, name=model.tag.name)
    return AccountTagReadDto(id=model.id, tag=tag_dto, order=model.order)


tag_router = APIRouter()


@tag_router.post("", status_code=status.HTTP_201_CREATED)
def create_tag(dto: TagCreateDto, session: Session = Depends(get_session)) -> TagReadDto:
    dto = TagCreateDto.validate(dto)
    tag_model: TagModel = TagModel(name=dto.name)
    session.add(tag_model)
    session.commit()
    session.refresh(tag_model)
    return TagReadDto(id=tag_model.id, name=tag_model.name)


@tag_router.get("/{id}", status_code=status.HTTP_200_OK)
def get_tag(id: int, session: Session = Depends(get_session)) -> TagReadDto:
    tag_model: TagModel = session.exec(select(TagModel).where(TagModel.id == id)).first()
    if tag_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return TagReadDto(id=tag_model.id, name=tag_model.name)


