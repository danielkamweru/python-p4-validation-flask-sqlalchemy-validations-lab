from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Author must have a name.")

        existing_author = Author.query.filter(Author.name == name).first()
        if existing_author:
            raise ValueError("Author name must be unique.")

        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not re.fullmatch(r'\d{10}', phone_number):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    CLICKBAIT_PHRASES = ["Won't Believe", "Secret", "Top", "Guess"]

    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be 250 characters or fewer.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be Fiction or Non-Fiction.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        if not any(phrase in title for phrase in self.CLICKBAIT_PHRASES):
            raise ValueError("Post title must contain a clickbait phrase.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title})'
