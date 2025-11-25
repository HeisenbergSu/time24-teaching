from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Student(db.Model):
    """学生表"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    class_name = db.Column(db.String(50), default='三年级一班')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_name': self.class_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Teacher(db.Model):
    """教师表"""
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Question(db.Model):
    """题目表"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)  # JSON字符串存储选项
    correct_answer = db.Column(db.String(10), nullable=False)
    module_type = db.Column(db.String(20))  # 'explore', 'learn', 'practice', 'challenge'
    created_at = db.Column(db.DateTime, default=datetime.now)


class StudentAnswer(db.Model):
    """学生答题记录表"""
    __tablename__ = 'student_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer = db.Column(db.String(10), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    module_type = db.Column(db.String(20))  # 'explore', 'learn', 'practice', 'challenge'
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    student = db.relationship('Student', backref=db.backref('answers', lazy=True))
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

