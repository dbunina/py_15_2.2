import os
import glob
import json
from chardet.universaldetector import UniversalDetector


def detect_encoding(filename):
    detector = UniversalDetector()
    with open(filename, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def get_top_words_for_file(filename, encoding):
    with open(filename, encoding=encoding) as f:
        if filename.endswith('.json'):
            text = parse_json(f)
        else:
            text = f.read()
        return get_top_ten_words(text)


def parse_json(file_descriptor):
    data = json.load(file_descriptor)
    text = ''
    for item in data['rss']['channel']['items']:
        text += (item['title'] + ' ' + item['description'] + '\n')
    return text


def get_top_ten_words(text):
    words = text.split()
    word_counter = {}
    for word in words:
        if len(word) > 6:
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1
    top_words = sorted(word_counter, key=word_counter.get, reverse=True)
    return top_words[:10]


def get_popular_words(extension):
    popular_words_by_article = dict()
    current_path = os.path.dirname(__file__)
    news_path = os.path.join(current_path, 'news')
    os.chdir(news_path)
    for filename in glob.glob('*.'+extension):
        encoding = detect_encoding(filename)
        popular_words_by_article[filename] = get_top_words_for_file(filename, encoding)
    return popular_words_by_article


def main():
    extension = input('Enter file type to count words in (txt or json):').lower()
    if extension not in ('txt', 'json'):
        print('Wrong extension type, please try again')
    else:
        print(get_popular_words(extension))


main()
