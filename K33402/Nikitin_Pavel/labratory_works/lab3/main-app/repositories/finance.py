from sqlmodel import select
from database import engine, Session
from models.finance import Balance, Target, Transactions, Subscription
from sqlalchemy.orm import selectinload

def select_all_balances():
    with Session(engine) as session:
        statement = select(Balance)
        res = session.exec(statement).all()
        return res

def find_balance(balance_id):
    with Session(bind=engine) as session:
      return session.get(Balance, balance_id)

def select_all_targets(balance_id: int):
    with Session(engine) as session:
        statement = select(Target).where(Target.balance_id == balance_id)
        res = session.exec(statement).all()
        return res

def find_target(balance_id, target_id):
    with Session(engine) as session:
        statement = select(Target).where((Target.id == target_id) & (Target.balance_id == balance_id))
        return session.exec(statement).first()
    
def select_all_transactions(balance_id):
    with Session(engine) as session:
        statement = select(Transactions).where(Transactions.balance_id == balance_id)
        res = session.exec(statement).all()
        return res

def find_transaction(balance_id, transaction_id):
    with Session(engine) as session:
        statement = select(Transactions).where((Transactions.id == transaction_id) & (Transactions.balance_id == balance_id))
        return session.exec(statement).first()

def select_all_subscriptions():
    with Session(engine) as session:
        statement = select(Subscription)
        res = session.exec(statement).all()
        return res

def find_subscription(balance_id, subscription_id):
    with Session(engine) as session:
        statement = select(Subscription).where((Subscription.id == subscription_id) & (Subscription.balance_id == balance_id))
        return session.exec(statement).first()
