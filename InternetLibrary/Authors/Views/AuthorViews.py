from flask import request, jsonify, Blueprint, Response
from flask.views import MethodView
from InternetLibrary import db, app
from InternetLibrary.Authors.Models.AuthorModel import Author
from InternetLibrary.Book.Models.BookModel import AuthorBook
from InternetLibrary.Authors.Serializer.AuthorSerializer import AuthorSerializer

author = Blueprint('Author', __name__)


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

    @author.route('/v1/author/<int:pk>/', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
    @author.route('/v1/author/<int:pk>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
    @author.route('/v1/author/', methods=['GET', 'POST'])
    def home(pk=None):
        if request.method == 'GET':
            if not pk:
                if request.args.get('name') is not None:
                    authors = Author.query.filter(Author.name.ilike("%"+request.args.get('name')+"%")).order_by(Author.name).all()
                else:
                    authors = Author.query.order_by(Author.name).all()
                res = AuthorSerializer().get_not_id(authors)
            else:
                res = AuthorSerializer().get_by_id(Author.query.filter_by(id=pk).first())
            return jsonify(res)
        elif request.method == 'POST':
            try:
                AuthorView().post()
                return Response('Author inserido com sucesso', 200)
            except Exception as exc:
                return Response(exc, 500)
        elif request.method == 'DELETE':
            try:
                AuthorView().delete(pk)
                return Response('Author deletado com sucesso', 200)
            except Exception as exc:
                return Response(exc, 500)
        elif request.method == 'PUT':
            try:
                AuthorView().update(pk)
                return Response('Atualizado com sucesso', 200)
            except Exception as exc:
                return Response(exc, 500)

    @staticmethod
    def post():
        author_insert = Author(name=request.form.get('name'))
        db.session.add(author_insert)
        db.session.commit()

    @staticmethod
    def delete(pk=None):
        for relationship in AuthorBook.query.filter(AuthorBook.author_id == pk).all():
            AuthorBook.query.filter(AuthorBook.id == relationship.id).delete()
        Author.query.filter(Author.id == pk).delete()
        db.session.commit()

    @staticmethod
    def update(pk):
        Author.query.filter(Author.id == pk).update({'name': request.form.get('name')})
        db.session.commit()
