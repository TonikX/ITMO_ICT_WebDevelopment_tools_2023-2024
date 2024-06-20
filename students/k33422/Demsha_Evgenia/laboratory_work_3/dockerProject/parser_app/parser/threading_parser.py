import threading
from parser_app.parser.settings import URLS
from parser_app.parser.parse_utils import parse_and_save


def crypto_parse(num):

    threads = []
    result_list = [None] * num
    urls_slice = URLS[:num]

    for i in range(num):
        url = urls_slice[i]
        thread = threading.Thread(target=parse_and_save, args=(url, result_list, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_list
