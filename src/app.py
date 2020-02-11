from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    background = db.Column(db.String(7), nullable=False, default="#000000")
    color = db.Column(db.String(7), nullable=False, default="#ffffff")

    def __repr__(self):
        return f"Tag('{self.name}', '{self.background}', '{self.color}')"




db.create_all()
db.session.commit()

tag = Tag(name="Backend", background="#123456", color="#fgfgfg")
db.session.add(tag)
db.session.commit()
users = Tag.query.all()
print(users)
