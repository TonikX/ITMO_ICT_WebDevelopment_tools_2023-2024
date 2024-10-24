import multiprocessing
from conn import get_session
from parsers import BlockchainComParser, BtcComParser, AbstractParser

def parse_and_save(parser: AbstractParser):
    parsed_data = parser.parse()
    session = next(get_session())
    for d in parsed_data:
        session.add(d)

def main():
    blockchain_parser = BlockchainComParser()
    btc_parser = BtcComParser()
    process1 = multiprocessing.Process(target=parse_and_save, args=(blockchain_parser,))
    process2 = multiprocessing.Process(target=parse_and_save, args=(btc_parser,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()

if __name__ == "__main__":
    main()
