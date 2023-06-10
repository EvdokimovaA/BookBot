import re
import requests
from Book import Book
from random import choice


class BookSearch:
    def __init__(self, book_name):
        name = book_name
        self.__book_name = name[0].upper() + name[1:]
        self.__URL = f"https://libgen.li/index.php?req={self.__book_name}&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&columns%5B%5D=y&columns%5B%5D=p&columns%5B%5D=i&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&objects%5B%5D=w&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=r&topics%5B%5D=s&res=25&filesuns=all&curtab=f"
        self.__list_books = []

    # Делает запрос на сайт с названием книги
    # Находит json файл на странице, формирует ссылку на него
    # Вызывает функцию сбора информации по файлу
    # Возвращает список найденных книг
    def get_request(self):
        book_listing_page = requests.get(self.__URL, headers=self.__choice_user_agent()).text
        try:
            main_json_url_part = re.findall(r'"\Wjson\Wphp\Wobject=f&ids=.+?"', book_listing_page)[0]
            main_json_url = self.__do_norm_urls(main_json_url_part)
            main_json = requests.get(main_json_url, headers=self.__choice_user_agent()).json()
            self.__collect_information(main_json)
            amount = 3
            if len(self.__list_books) < 3:
                amount = len(self.__list_books)
            for i in range(amount):
                self.__work_with_book_personal_page(self.__list_books[i], self.__list_books[i].url_personal_page)
            final_list = []
            for i in range(amount):
                if len(self.__list_books[i].url_download) > 0:
                    final_list.append(self.__list_books[i])
            return final_list
        except:
            return []

    # Собирает нужную информацию из json, формирует список из объектов Book, включающих эту информацию
    def __collect_information(self, main_json):
        for i in main_json:
            pages = int(main_json[i]["pages"])
            if pages == 0:
                continue
            else:
                name = self.__book_name
                md5 = main_json[i]["md5"]
                extension = main_json[i]["extension"]
                for j in main_json[i]["editions"]:
                    e_id = int(main_json[i]["editions"][j]["e_id"])
                    url_personal_page = self.__do_norm_urls("edition.php?id=", str(e_id))
                    k = Book(name, md5, pages, extension, e_id, url_personal_page)
                    if k not in self.__list_books and k:
                        self.__list_books.append(k)

    # Собирает все ссылки для скачивания книги
    def __work_with_book_personal_page(self, book, link):
        ipfs_cloudflare = r'href="https:\W\Wcloudflare.+?>'
        ipfs_io = r'href="https:\W\Wipfs\Wio.+?>'
        libgen_rs = r'href="http:\W\Wlibrary\Wlol.+?>'
        book_personal_page = requests.get(link, headers=self.__choice_user_agent()).text
        book.url_download = book.url_download + self.__collect_links(book_personal_page, ipfs_cloudflare)
        book.url_download = book.url_download + self.__collect_links(book_personal_page, ipfs_io)
        for i in self.__collect_links(book_personal_page, libgen_rs):
            lst = self.__collect_libgen_links(book, i)
            if len(lst) > 0:
                book.url_download.append(lst)
        temporary_short_links = []
        for i in book.url_download:
            temporary_short_links.append(self.__make_short_links(i))
        book.url_download = temporary_short_links.copy()

    @staticmethod
    def __make_short_links(link):
        endpoint = 'https://clck.ru/--'
        url = (link, '?utm_source=sender')
        response = requests.get(endpoint, params={'url': url})
        return response.text

    # Находит ссылки разных типов, собирает в 1 список
    def __collect_links(self, page_text, regular_expression):
        lst = re.findall(regular_expression, page_text)
        links_list = []
        for i in lst:
            box = i.split('"')
            link = box[1].replace(" ", "%20")
            links_list.append(link)
        return links_list

    # Поиск ссылки на отдельных страницах для скачивания
    def __collect_libgen_links(self, book, element):
        book_download_page = requests.get(element, headers=self.__choice_user_agent()).text
        try:
            link = re.findall('href=".+?' + book.md5 + '.+?">GET', book_download_page)[0].split('"')
            return link[1]
        except:
            return []

    # Формирует ссылки из результатов поиска по регулярным выражениям
    @staticmethod
    def __do_norm_urls(link, addition=""):
        norm_part = link.strip('"')
        norm_link = f"https://libgen.li/{norm_part}{addition}"
        return norm_link

    @staticmethod
    def __choice_user_agent():
        with open("user_agent.txt", "r") as file:
            lines = file.read().splitlines()
            user_agent = {"user_agent": choice(lines)}
            return user_agent
