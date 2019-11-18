from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(20), unique=True, nullable=False)
    images = db.relationship('Image', backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "images": list(map(lambda x: x.serialize(), self.images))
        }

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)
    def serialize(self):
        return{
          "image_name": self.image_name,
          "user_id": self.user_id,
          "created_date": self.created_date
        }