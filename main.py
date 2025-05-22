"""
Доработать декоратор logger в коде ниже.
Должен получиться декоратор, который записывает в файл 'main.log' дату и время вызова функции,
имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.
Функция test_1 в коде ниже также должна отработать без ошибок.

"""
from pprint import pprint
import re
import bs4
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import os
from datetime import datetime
from functools import wraps
def logger(old_function):
    @wraps(old_function)

    def new_function(*args, **kwargs):
        arguments = f''
        if args:
            arguments += f'{args=} '
        if kwargs:
            arguments += f'{kwargs} '
        date = datetime.now()
        name = old_function.__name__
        result = old_function(*args, **kwargs)

        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(str(date) + '\n')
            f.write(name + '\n')
            f.write(arguments + '\n')
            f.write(str(result) + '\n')

        return result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


"""
Доработать параметризованный декоратор logger в коде ниже.
Должен получиться декоратор, который записывает в файл дату и время вызова функции,
имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.
Путь к файлу должен передаваться в аргументах декоратора.
Функция test_2 в коде ниже также должна отработать без ошибок.

"""


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            arguments = ''
            if args:
                arguments += f'{args=} '
            if kwargs:
                arguments += f'{kwargs} '
            date = datetime.now()
            name = old_function.__name__
            result = old_function(*args, **kwargs)

            with open(path, 'a', encoding='utf-8') as f:
                f.write(str(date) + '\n')
                f.write(name + '\n')
                f.write(arguments + '\n')
                f.write(str(result) + '\n')
            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            arguments = ''
            if args:
                arguments += f'{args=} '
            if kwargs:
                arguments += f'{kwargs} '
            date = datetime.now()
            name = old_function.__name__
            result = old_function(*args, **kwargs)

            with open(path, 'a', encoding='utf-8') as f:
                f.write(str(date) + '\n')
                f.write(name + '\n')
                f.write(arguments + '\n')
                f.write(str(result) + '\n')

            return result

        return new_function

    return __logger



@logger('download.log')
def download_page():
    # эта функция будет сохранять HTML в файл
    def generate_headers():

        headers = Headers(browser='chrome', os='win').generate()

        return headers

    link = 'https://habr.com/ru/articles/'

    try:
        response = requests.get("https://habr.com/ru/articles/", headers=generate_headers())
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе Хабр: {e}")
        exit()

    return response.text

@logger('parse.log')
def find_articles(keywords):
    # здесь код для поиска статей по ключевым словам и возврата списка статей
    main_html = download_page()

    main_page_soup = bs4.BeautifulSoup(main_html, features='lxml')

    tm_articles_list_tag = main_page_soup.find("div", class_="tm-articles-list")

    article_tags = tm_articles_list_tag.find_all("article")

    parsed_articles_list = []

    for article_tag in article_tags:

        h2_tag = article_tag.find("h2")
        a_tag = h2_tag.find("a")
        time_tag = article_tag.find("time")

        header = h2_tag.text
        pattern = r"[.,:;!?—–\-–«»\"\'\[\]\(\)]"
        pre_final_header = re.sub(pattern, "", header)
        pattern2 = r"…"
        final_header = re.sub(pattern2, "", pre_final_header)

        link = a_tag["href"]
        full_link = f"https://habr.com{link}"
        published_time = time_tag["datetime"]

        for word in final_header.split():
            if word.lower() in keywords:
                parsed_article = {
                    "дата": published_time,
                    "заголовок": header,
                    "ссылка": full_link
                }

                parsed_articles_list.append(parsed_article)
                break

    return parsed_articles_list


if __name__ == '__main__':
    keywords = [
        "интеллект",
        "история",
        "Код",
        "Хабр",
        "GPT",
        "баг",
        "linux"
    ]
    keywords = [i.lower() for i in keywords]

    articles = find_articles(keywords)
    pprint(articles)
