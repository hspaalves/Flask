from InternetLibrary import db
from sqlalchemy.orm import relationship


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __str__(self):
        return "%s | %s" % (
            self.name,
            self.id,
        )

    def __repr__(self):
        return " %r" % (
            self.name
        )
