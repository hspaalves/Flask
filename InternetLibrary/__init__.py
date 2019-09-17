from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ADMIN:PASS@db:5432/Borges'
db = SQLAlchemy(app)

from InternetLibrary.Authors.Views.AuthorViews import author
from InternetLibrary.Book.Views.BookViews import book
app.register_blueprint(author)
app.register_blueprint(book)

db.create_all()
lista = ['Links']


@app.route('/')
def home():
    return """
    <p>Author: <a href="http://0.0.0.0:8000/v1/author/">http://0.0.0.0:8000/v1/author/</a></p>
    <p>Book: <a href="http://0.0.0.0:8000/v1/book/">http://0.0.0.0:8000/v1/book/</a></p>
    """



