from InternetLibrary.Book.Models.BookModel import Book, AuthorBook
from flask.views import MethodView
from flask import request, jsonify, Blueprint
from InternetLibrary import db, app
from InternetLibrary.Book.Serializer.BookSerializer import BookSerializer

book = Blueprint('Book', __name__)
@book.route('/v1/book/')
@book.route('/v1/book/<int:id>')
def home():
    return 'Books'


class BookView(MethodView):
    @book.route('/v1/book/<int:pk>/author/')
    def get_author_detail(pk):
        author = []
        for author_book in AuthorBook.query.filter_by(book_id=pk).all():
            author.append({'id': author_book.author_id, 'name': author_book.author.name})
        res = author
        return jsonify(res)

    def get(self, pk=None):
        if not pk:
            if request.args.get('name') is not None:
                books = Book.query.filter(Book.name.ilike("%"+request.args.get('name')+"%")).order_by(Book.name).all()
            else:
                books = Book.query.order_by(Book.name).all()
            res = BookSerializer.get_not_id(books, AuthorBook)
        else:
            res = BookSerializer.get_by_id(Book.query.filter_by(id=pk).all(), AuthorBook)

        return jsonify(res)

    def post(self):
        name = request.form.get('name')
        author = Book(name)
        db.session.add(author)
        db.session.commit(author)
        return jsonify({author.id: {
            'name': author.name
        }})


book_view = BookView.as_view('book_view')
app.add_url_rule(
    '/v1/book/', view_func=book_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/v1/book/<int:pk>/', view_func=book_view, methods=['GET']
)
