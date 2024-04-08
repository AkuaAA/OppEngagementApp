from website import bcrypt, db
from flask_login import UserMixin
from datetime import datetime
from .extension import db

class Employee(UserMixin, db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False, name='uq_employee_email')
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    posts = db.relationship('Post', back_populates='post_author', lazy=True)
    opportunities = db.relationship('Opportunity', backref='employee_opportunity', lazy=True)
    comments = db.relationship('Comments', back_populates='comment_author', lazy=True)
    
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_lockout_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Employee {self.email}>"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('employees.id', name='fk_posts_author_id'), nullable=False)

    post_author = db.relationship('Employee', back_populates='posts')

    def __repr__(self):
        return f"<Post {self.title}>"

class Opportunity(db.Model):
    __tablename__ = "opportunity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __repr__(self):
        return f"<Opportunity {self.name}>"

class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    body = db.Column(db.Text, nullable=False)

    comment_author = db.relationship('Employee', back_populates='comments')

    def __repr__(self):
        return f"<Comments {self.body}>"