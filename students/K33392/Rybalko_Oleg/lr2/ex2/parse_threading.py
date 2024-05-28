import threading
from conn import get_session
from sqlmodel import Session
from parsers import BlockchainComParser, BtcComParser, AbstractParser

def parse_and_save(parser: AbstractParser, session: Session):
    parsed_data = parser.parse()
    for d in parsed_data:
        session.add(d)
    # session.commit()

def main():
    blockchain_parser = BlockchainComParser()
    btc_parser = BtcComParser()
    session = next(get_session())
    thread1 = threading.Thread(target=parse_and_save, args=(blockchain_parser, session))
    thread2 = threading.Thread(target=parse_and_save, args=(btc_parser, session))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
