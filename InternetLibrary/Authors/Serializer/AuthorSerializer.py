from flask import abort


class AuthorSerializer:

    def __init__(self):
        pass

    @staticmethod
    def get_by_id(authors):
        if not authors:
            abort(404)
        return {
            'id': authors.id,
            'name': authors.name
        }
