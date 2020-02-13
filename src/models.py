from src import db
from datetime import datetime


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    background = db.Column(db.String(7), nullable=False, default="#000000")
    color = db.Column(db.String(7), nullable=False, default="#ffffff")

    def __repr__(self):
        return str({"name": self.name, "background": self.background, "color": self.color})


class Comment(db.Model):
    parent_id = db.Column(db.Integer, db.ForeignKey('issue.id'), primary_key=True)
    comment_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return str(
            {"author": self.author, "content": self.content, "edited": self.edited, "created_on": self.created_on})


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"User('{self.id}', '{self.name}')"


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return f"Type('{self.id}', '{self.name}')"


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    type = db.Column(db.Integer, db.ForeignKey('type.id'))
    status = db.Column(db.Integer, nullable=False, default=0)
    priority = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Issue('{self.title}', '{self.reporter}', '{self.assignee}', '{self.content}', '{self.type}'," \
               f"'{self.status}', '{self.priority}', '{self.comments}')"
