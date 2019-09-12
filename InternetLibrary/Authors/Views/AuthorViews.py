from flask import request, jsonify, Blueprint
from flask.views import MethodView
from InternetLibrary import db, app
from InternetLibrary.Authors.Models.AuthorModel import Author
from InternetLibrary.Book.Models.BookModel import AuthorBook
from InternetLibrary.Authors.Serializer.AuthorSerializer import AuthorSerializer

author = Blueprint('Author', __name__)
@author.route('/')
@author.route('/home')
def home():
    return "Welcome to the Author Home."


class AuthorView(MethodView):
    @author.route('/v1/author/<int:pk>/book/')
    def get_book_detail(pk):
        book = []
        for book_author in AuthorBook.query.filter_by(author_id=pk).all():
            book.append({
                'id': book_author.book_id,
                'name': book_author.book.name,
                'summary': book_author.book.summary
            })
        return jsonify(book)

    def get(self, id=None):

        if not id:
            if request.args.get('name') is not None:
                authors = Author.query.filter(Author.name.ilike("%"+request.args.get('name')+"%")).order_by(Author.name).all()
            else:
                authors = Author.query.order_by(Author.name).all()
            res = AuthorSerializer().get_not_id(authors)
        else:
            res = AuthorSerializer().get_by_id(Author.query.filter_by(id=id).first())
        return jsonify(res)

    def post(self):
        name = request.form.get('name')
        db.session.add(Author(name))
        db.session.commit(author)
        return jsonify({author.id: {
            'name': author.name
        }})

    def put(self, id):
        return

    def delete(self, id):
        return


author_view = AuthorView.as_view('author_view')
app.add_url_rule(
    '/v1/author/', view_func=author_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/v1/author/<int:id>/', view_func=author_view, methods=['GET']
)
