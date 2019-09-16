from InternetLibrary.Book.Models.BookModel import Book, AuthorBook
from flask.views import MethodView
from flask import request, jsonify, Blueprint, Response
from InternetLibrary import db, app
from InternetLibrary.Book.Serializer.BookSerializer import BookSerializer

book = Blueprint('Book', __name__)


class BookView(MethodView):
    @book.route('/v1/book/<int:pk>/author/')
    def get_author_detail(pk):
        author = []
        for author_book in AuthorBook.query.filter_by(book_id=pk).all():
            author.append({'id': author_book.author_id, 'name': author_book.author.name})
        res = author
        return jsonify(res)

    @book.route('/v1/book/<int:pk>/',  methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
    @book.route('/v1/book/<int:pk>',  methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
    @book.route('/v1/book/', methods=['GET', 'POST'])
    def home(pk=None):
        if request.method == 'GET':
            if not pk:
                if request.args.get('name') is not None:
                    books = Book.query.filter(Book.name.ilike("%"+request.args.get('name')+"%")).order_by(Book.name).all()
                else:
                    books = Book.query.order_by(Book.name).all()
                res = BookSerializer.get_not_id(books, AuthorBook)
            else:
                res = BookSerializer.get_by_id(Book.query.filter_by(id=pk).all(), AuthorBook)

            return jsonify(res)
        elif request.method == 'POST':
            try:
                BookView().post()
                return Response('Book inserido com sucesso', 200)
            except Exception as exc:
                return Response(exc, 500)

        elif request.method == 'DELETE':
            try:
                BookView().delete(pk)
                return Response('Deletado com sucesso', 200)
            except Exception as exc:
                return Response(exc, 500)

        elif request.method == 'PUT':
            try:
                BookView.update(pk)
                return Response('Atualizado com sucesso', 200)
            except Exception as exc:
                return Response(exc, 500)

    @staticmethod
    def post():
        db.session.add(Book(name=request.form.get('name'), summary=request.form.get('summary')))
        db.session.commit()
        if request.form.get('author') not in '':
            details = Book.query.order_by(Book.id.desc()).first()
            db.session.add(AuthorBook(author_id=request.form.get('author'), book_id=details.id))
            db.session.commit()

    @staticmethod
    def delete(pk):
        for relationship in AuthorBook.query.filter(AuthorBook.book_id == pk).all():
            AuthorBook.query.filter(AuthorBook.id == relationship.id).delete()
        Book.query.filter(Book.id == pk).delete()
        db.session.commit()

    @staticmethod
    def update(pk):
        if request.form.get('name') not in '':
            Book.query.filter(Book.id == pk).update({'name': request.form.get('name')})
        if request.form.get('summary') not in '':
            Book.query.filter(Book.id == pk).update({'summary': request.form.get('summary')})
        db.session.commit()

