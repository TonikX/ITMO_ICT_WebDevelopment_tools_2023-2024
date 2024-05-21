import multiprocessing
import requests
import psycopg2
from time import time


def save_to_db(data):
    conn = psycopg2.connect("dbname=openalex_db user=postgres password=Aliya2103 host=localhost")
    cur = conn.cursor()
    for record in data:
        cur.execute(
            "INSERT INTO openalex_data (id, title, abstract, domain) VALUES (%s, %s, %s, %s)",
            (record['id'], record['title'], record['abstract'], record['domain'])
        )
    conn.commit()
    cur.close()
    conn.close()

def dict_to_sentence(dictionary):
    sentence_words = [''] * (max(max(indices) for indices in dictionary.values()) + 1)
    for word, indices in dictionary.items():
        for index in indices:
            sentence_words[index] = word
    return ' '.join(sentence_words)

def parse_and_save(url):
    response = requests.get(url)
    page_with_results = response.json()
    all_data = []
    if 'results' in page_with_results:
        for result in page_with_results['results']:
            primary_topic = result.get('primary_topic')
            if primary_topic:
                domain_display_name = primary_topic.get('domain', {}).get('display_name', '')
            else:
                domain_display_name = ''
            if domain_display_name:
                title = result.get('title')
                if title:
                    record = {'id': result['id'].replace("https://openalex.org/", ""), 'domain': domain_display_name}
                    for key, value in result.items():
                        if key != 'id':
                            record[key] = value
                    if 'abstract_inverted_index' in record and record['abstract_inverted_index']:
                        record['abstract'] = dict_to_sentence(record['abstract_inverted_index'])
                        all_data.append(record)
    save_to_db(all_data)

def main_multiprocessing():
    start_time = time()
    urls = [f'https://api.openalex.org/works?page={i}&per-page=200' for i in range(7, 13)]
    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    print(f"Time taken (multiprocessing): {time() - start_time} seconds")

if __name__ == "__main__":
    main_multiprocessing()
