from src import db
from datetime import datetime

tags_association = db.Table("tags_association",
                            db.Column("issue_id", db.Integer, db.ForeignKey("issue.id")),
                            db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")))


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    background = db.Column(db.String(6), nullable=False, default="000000")
    color = db.Column(db.String(6), nullable=False, default="ffffff")
    issues = db.relationship("Issue", secondary=tags_association, back_populates="tags")
    __table_args__ = (
        db.CheckConstraint("length(name) > 0",
                           name="name_min_length"),
        db.CheckConstraint("length(background) > 5",
                           name="background_min_length"),
        db.CheckConstraint("length(color) > 5",
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
        db.CheckConstraint("length(name) > 0",
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
        db.CheckConstraint("length(name) > 0",
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
    parent_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    comment_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    edited = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    __table_args__ = (
        db.CheckConstraint("length(content) > 0",
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
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    description = db.Column(db.Text)
    type = db.Column(db.Integer, db.ForeignKey("type.id"), default=None)
    tags = db.relationship("Tag", secondary=tags_association, back_populates="issues")
    status = db.Column(db.Integer, default=0)
    priority = db.Column(db.Integer, default=0)
    comments = db.relationship("Comment", backref="parent")
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    __table_args__ = (
        db.CheckConstraint("length(title) > 0",
                           name="title_min_length"),
        db.CheckConstraint("priority < 3",
                           name="priority_max_length"),
        db.CheckConstraint("status < 5",
                           name="status_max_length"),
    )

    @db.validates("title")
    def validate_background(self, key, title: str) -> str:
        if len(title) < 1:
            raise ValueError("attr title must be at least 1 character long.")
        return title

    @db.validates("priority")
    def validate_background(self, key, priority: int) -> int:
        if priority > 2:
            raise ValueError("attr priority may not be larger than 2.")
        return priority

    @db.validates("status")
    def validate_background(self, key, status: int) -> int:
        if status > 5:
            raise ValueError("attr status may not be larger than 2.")
        return status

    def __repr__(self):
        return str(
            {"id": self.id, "title": self.title, "reporter": self.reporter, "assignee": self.assignee,
             "description": self.description, "type": self.type, "status": self.status, "priority": self.priority,
             "comments": self.comments})
