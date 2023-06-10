class Book:
    def __init__(self, name, md5, pages, extension, e_id, url_personal_page):
        self.name = name
        self.md5 = md5
        self.pages = pages
        self.extension = extension
        self.e_id = e_id
        self.url_personal_page = url_personal_page
        self.url_download = []

    def __bool__(self):
        return self.pages > 0

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.e_id == other.e_id

    def __str__(self):
        return f"Книга: {self.name}\nРасширение: {self.extension}\nСтраницы: {self.pages}\nСкачать: {self.url_download}"
