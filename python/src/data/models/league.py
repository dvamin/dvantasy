from python.src.data.database import db

class League(db.Model):
    __tablename__ = "league"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    commissioner_id = db.Column(db.Integer())

    def __init__(self, name, commissioner_id):
        self.name = name
        self.commissioner_id = commissioner_id

    def __repr__(self):
        return "<id {}>".format(self.id)