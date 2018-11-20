from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_text = db.Column(db.String(200), nullable=False)
    p_text = db.Column(db.Text, nullable=False)
    alternatives = db.Column(db.String(80), nullable=False)
    dataset = db.Column(db.String(20))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'q_text': self.q_text,
            'p_text': self.p_text,
            'alternatives': self.alternatives,
            'dataset': self.dataset
        }


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    query_time = db.Column(db.DateTime, default=datetime.now)
    question = db.relationship('Question', backref=db.backref('historys',
                                                               order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('historys'))
    answer = db.Column(db.String(100), nullable=False)

