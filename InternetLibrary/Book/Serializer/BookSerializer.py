from flask import abort


class BookSerializer:
    def __init__(self):
        pass

    @staticmethod
    def get_by_id(books, AuthorBook):
        for detail_book in books:
            res = {'name': detail_book.name, 'summary': detail_book.summary, 'id': detail_book.id}
            author = []
            for authorbook in AuthorBook.query.filter_by(book_id=detail_book.id).all():
                author.append(authorbook.author_id)
                res['author'] = author
            return res
