from flask import abort


class AuthorSerializer:

    def __init__(self):
        pass

    @staticmethod
    def get_not_id(authors):
        res = {'count': len(authors), 'next': None, 'previous': None}
        results = []
        for detail_author in authors:
            results.append({
                'id': detail_author.id,
                'name': detail_author.name
            })
            res['results'] = results
        return res

    @staticmethod
    def get_by_id(authors):
        if not authors:
            abort(404)
        return {
            'id': authors.id,
            'name': authors.name
        }
