from src import db
from datetime import datetime


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    background = db.Column(db.String(6), nullable=False, default="000000")
    color = db.Column(db.String(6), nullable=False, default="ffffff")
    __table_args__ = (
        db.CheckConstraint("char_length(name) > 0",
                           name="name_min_length"),
        db.CheckConstraint("char_length(background) > 5",
                           name="background_min_length"),
        db.CheckConstraint("char_length(color) > 5",
                           name="color_min_length"),
    )

    @db.validates("name")
    def validate_background(self, key, name: str) -> str:
        if len(name) < 1:
            raise ValueError("attr name must be at least 1 character long.")
        return name

    @db.validates("background")
    def validate_background(self, key, background: str) -> str:
        if len(background) <= 5:
            raise ValueError("attr background must be a 6 digit hex value.")
        return background

    @db.validates("color")
    def validate_background(self, key, color: str) -> str:
        if len(color) <= 5:
            raise ValueError("attr color must be a 6 digit hex value.")
        return color

    def __repr__(self):
        return str({"name": self.name, "background": self.background, "color": self.color})


class Type(db.Model):
    __tablename__ = "type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    __table_args__ = (
        db.CheckConstraint("char_length(name) > 0",
                           name="name_min_length"),
    )

    @db.validates("name")
    def validate_background(self, key, name: str) -> str:
        if len(name) < 1:
            raise ValueError("attr name must be at least 1 character long.")
        return name

    def __repr__(self):
        return str({"name": self.name})


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    __table_args__ = (
        db.CheckConstraint("char_length(name) > 0",
                           name="name_min_length"),
    )

    @db.validates("name")
    def validate_background(self, key, name: str) -> str:
        if len(name) < 1:
            raise ValueError("attr name must be at least 1 character long.")
        return name

    def __repr__(self):
        return str({"id": self.id, "name": self.name})


class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    __table_args__ = (
        db.CheckConstraint("char_length(content) > 0",
                           name="content_min_length"),
    )

    @db.validates("name")
    def validate_background(self, key, content: str) -> str:
        if len(content) < 1:
            raise ValueError("attr content must be at least 1 character long.")
        return content

    def __repr__(self):
        return str(
            {"author": self.author, "content": self.content, "edited": self.edited, "created_on": self.created_on})


class Issue(db.Model):
    __tablename__ = "issue"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # automatically set by frontend
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'))  # none or one
    description = db.Column(db.Text)
    type = db.Column(db.Integer, db.ForeignKey('type.id'))  # many to many, may also be none
    tags = db.Column(db.Integer, db.ForeignKey('tags.id'))  # many to many, may also be none
    status = db.Column(db.Integer, default=0)
    priority = db.Column(db.Integer, default=0)
    comments = db.relationship("Comment")  # may require additional backref markers

    def __repr__(self):
        return str(
            {"id": self.id, "title": self.title, "reporter": self.reporter, "assignee": self.assignee,
             "content": self.description, "type": self.type, "status": self.status, "priority": self.priority,
             "comments": self.comments})

    comments_association = db.Table("comments_association",
                                    db.Column("comment_id", db.Integer, db.ForeignKey("comment.id")))
