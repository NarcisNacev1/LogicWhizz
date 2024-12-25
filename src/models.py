from .extensions import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)  # Use Text for longer strings

    def __repr__(self):
        return f"<Question {self.question}>"
