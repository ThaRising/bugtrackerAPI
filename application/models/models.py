from application import db
from datetime import datetime
from application.config import TOO_SHORT, TYPE_NOT_COLOR, OUT_OF_RANGE
import application.models.data_models as data_models

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
        db.CheckConstraint("length(background) < 7",
                           name="background_max_length"),
        db.CheckConstraint("length(color) > 5",
                           name="color_min_length"),
        db.CheckConstraint("length(color) < 7",
                           name="color_max_length"),
    )

    @db.validates("name")
    def validate_background(self, key, name: str) -> str:
        if len(name) < 1:
            raise ValueError(TOO_SHORT)
        return name

    @db.validates("background")
    def validate_background(self, key, background: str) -> str:
        if len(background) <= 5 or len(background) >= 7:
            raise ValueError(TYPE_NOT_COLOR)
        return background

    @db.validates("color")
    def validate_background(self, key, color: str) -> str:
        if len(color) <= 5 or len(color) >= 7:
            raise ValueError(TYPE_NOT_COLOR)
        return color

    def __repr__(self) -> str:
        """
        :return: Returns a string representation of the object
        """
        return f"{self.__class__.__name__}" \
               f"('name': '{self.name}', 'background': '{self.background}', 'color': '{self.color}')"

    def __iter__(self) -> None:
        """
        :return: Yields the items attributes as a dictionary
        """
        yield "id", self.id
        yield "name", self.name
        yield "background", self.background
        yield "color", self.color

    def __len__(self) -> int:
        """
        :return: Returns the total number of the tables SQL columns
        """
        return 4


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
            raise ValueError(TOO_SHORT)
        return name

    def __repr__(self) -> str:
        """
        :return: Returns a string representation of the object
        """
        return f"{self.__class__.__name__}('name': '{self.name}')"

    def __iter__(self) -> None:
        """
        :return: Yields the items attributes as a dictionary
        """
        yield "id", self.id
        yield "name", self.name

    def __len__(self) -> int:
        """
        :return: Returns the total number of the tables SQL columns
        """
        return 2


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
            raise ValueError(TOO_SHORT)
        return name

    def __repr__(self) -> str:
        """
        :return: Returns a string representation of the object
        """
        return f"{self.__class__.__name__}('name': '{self.name}', 'created_on': '{self.created_on}')"

    def __iter__(self) -> None:
        """
        :return: Yields the items attributes as a dictionary
        """
        yield "id", self.id
        yield "name", self.name
        yield "created_on", self.created_on

    def __len__(self) -> int:
        """
        :return: Returns the total number of the tables SQL columns
        """
        return 3


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
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
            raise ValueError(TOO_SHORT)
        return content

    def __repr__(self) -> str:
        """
        :return: Returns a string representation of the object
        """
        return f"{self.__class__.__name__}" \
               f"('id': '{self.id}', 'parent_id': '{self.parent_id}', 'author': '{self.author}'," \
               f" 'content': '{self.content}', 'edited': '{self.edited}', 'created_on': '{self.created_on}')"

    def __iter__(self) -> None:
        """
        :return: Yields the items attributes as a dictionary
        """
        yield "id", self.id
        yield "parent_id", self.parent_id
        yield "author", self.author
        yield "content", self.content
        yield "edited", self.edited
        yield "created_on", str(self.created_on)

    def __len__(self) -> int:
        """
        :return: Returns the total number of the tables SQL columns
        """
        return 6


class Issue(db.Model):
    __tablename__ = "issue"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    description = db.Column(db.Text)
    type = db.Column(db.Integer, db.ForeignKey("type.id"), default=None)
    tags = db.relationship("Tag", secondary=tags_association, back_populates="issues")
    status = db.Column(db.Integer, default=1)
    priority = db.Column(db.Integer, default=1)
    comments = db.relationship("Comment", backref="parent")
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    __table_args__ = (
        db.CheckConstraint("length(title) > 0",
                           name="title_min_length"),
        db.CheckConstraint(f"priority < {len(data_models.PRIORITY)}",
                           name="priority_max_length"),
        db.CheckConstraint(f"status < {len(data_models.STATUS)}",
                           name="status_max_length"),
    )

    @db.validates("title")
    def validate_background(self, key, title: str) -> str:
        if len(title) < 1:
            raise ValueError(TOO_SHORT)
        return title

    @db.validates("priority")
    def validate_background(self, key, priority: int) -> int:
        if not data_models.validate_priority(priority):
            raise ValueError(OUT_OF_RANGE)
        return priority

    @db.validates("status")
    def validate_background(self, key, status: int) -> int:
        if not data_models.validate_status(status):
            raise ValueError(OUT_OF_RANGE)
        return status

    def __repr__(self) -> str:
        """
        :return: Returns a string representation of the object.
        """
        return f"{self.__class__.__name__}" \
               f"('title': '{self.title}', 'reporter': '{self.reporter}', 'assignee': '{self.assignee}'," \
               f"'description': '{self.description}', 'type': '{self.type}', 'status': '{self.status}'," \
               f"'priority': '{self.priority}')"

    def __iter__(self) -> None:
        """
        :return: Yields the items attributes as a dictionary.
        """
        yield "id", self.id
        yield "title", self.title
        yield "reporter", self.reporter
        yield "assignee", self.assignee
        yield "description", self.description
        yield "type", self.type
        yield "tags", self.tags
        yield "status", self.status
        yield "priority", self.priority
        yield "comments", self.comments
        yield "created_on", str(self.created_on)

    def __len__(self) -> int:
        """
        :return: Returns the total number of the tables SQL columns
        """
        return 9
