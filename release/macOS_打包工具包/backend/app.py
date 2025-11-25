from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Student, Question, StudentAnswer, Teacher
from seed_data import seed_questions
from datetime import datetime
import json
import os
import sys

# Determine paths for static files (frontend build)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_dir = sys._MEIPASS
    static_dir = os.path.join(base_dir, 'web')
else:
    # Running as python script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, '../frontend/dist')

# Ensure the static directory exists to avoid errors if frontend isn't built yet
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app = Flask(__name__, static_folder=static_dir, static_url_path='')

# Configure Database Path
if getattr(sys, 'frozen', False):
    # When frozen, put DB in the same folder as the executable
    db_path = os.path.join(os.path.dirname(sys.executable), 'time24_teaching.db')
else:
    # When dev, put DB in the instance folder
    db_path = os.path.join(app.instance_path, 'time24_teaching.db')
    os.makedirs(app.instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

CORS(app)
db.init_app(app)

# Serve Frontend
@app.route('/')
def serve_frontend():
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return "Frontend not built. Please run 'npm run build' in frontend directory."

# Handle Vue Router history mode (catch-all)
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    # Try to serve static file if it exists
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # Otherwise serve index.html for client-side routing
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    return "Not found", 404

# 初始化数据库
with app.app_context():
    db.create_all()
    # 创建默认教师账号
    teacher = Teacher.query.filter_by(username='teacher').first()
    if not teacher:
        default_teacher = Teacher(username='teacher', password='teacher123')
        db.session.add(default_teacher)
        db.session.commit()
    
    # 自动初始化题目数据
    seed_questions(db)


# ==================== 学生相关API ====================

@app.route('/api/student/register', methods=['POST'])
def register_student():
    data = request.json
    student = Student(
        name=data.get('name'),
        class_name=data.get('class_name', '三年级一班')
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({
        'success': True,
        'student_id': student.id,
        'message': '注册成功'
    })


@app.route('/api/student/<int:student_id>/answers', methods=['POST'])
def submit_answer(student_id):
    data = request.json
    answer = StudentAnswer(
        student_id=student_id,
        question_id=data.get('question_id'),
        answer=data.get('answer'),
        is_correct=data.get('is_correct'),
        module_type=data.get('module_type')  # 'explore', 'learn', 'practice', 'challenge'
    )
    db.session.add(answer)
    db.session.commit()
    return jsonify({'success': True, 'message': '答案已提交'})


@app.route('/api/student/<int:student_id>/score', methods=['GET'])
def get_student_score(student_id):
    student = Student.query.get_or_404(student_id)
    answers = StudentAnswer.query.filter_by(student_id=student_id).all()
    
    # 统计各模块完成情况（按唯一题目统计）
    modules = {}
    total_unique_questions = 0
    total_correct_questions = 0
    
    for module_type in ['explore', 'practice', 'challenge']:
        module_answers = [a for a in answers if a.module_type == module_type]
        # 去重，按question_id统计（同一题只算一次）
        unique_questions = list(set([a.question_id for a in module_answers]))
        
        # 对于每个唯一题目，检查是否有正确答案
        correct_questions = []
        for qid in unique_questions:
            # 该题的所有答案记录
            q_answers = [a for a in module_answers if a.question_id == qid]
            # 只要有一次答对就算对
            if any(a.is_correct for a in q_answers):
                correct_questions.append(qid)
        
        modules[module_type] = {
            'completed': len(unique_questions),
            'correct': len(correct_questions)
        }
        
        total_unique_questions += len(unique_questions)
        total_correct_questions += len(correct_questions)
    
    # 总统计也按唯一题目数计算
    score = int((total_correct_questions / total_unique_questions * 100)) if total_unique_questions > 0 else 0
    
    return jsonify({
        'student_id': student_id,
        'total': total_unique_questions,
        'correct': total_correct_questions,
        'score': score,
        'modules': modules
    })


# ==================== 题目相关API ====================

@app.route('/api/questions/explore', methods=['GET'])
def get_explore_questions():
    """获取课前探索题目（旧知复习）"""
    questions = Question.query.filter_by(module_type='explore').all()
    return jsonify({
        'questions': [{
            'id': q.id,
            'question': q.question,
            'options': json.loads(q.options) if isinstance(q.options, str) else q.options,
            'correct_answer': q.correct_answer,
            'module_type': q.module_type
        } for q in questions]
    })


@app.route('/api/questions/practice', methods=['GET'])
def get_practice_questions():
    """获取生活应用题目"""
    questions = Question.query.filter_by(module_type='practice').all()
    return jsonify({
        'questions': [{
            'id': q.id,
            'question': q.question,
            'options': json.loads(q.options) if isinstance(q.options, str) else q.options,
            'correct_answer': q.correct_answer,
            'module_type': q.module_type
        } for q in questions]
    })


@app.route('/api/questions/challenge', methods=['GET'])
def get_challenge_questions():
    """获取成就挑战题目"""
    questions = Question.query.filter_by(module_type='challenge').all()
    return jsonify({
        'questions': [{
            'id': q.id,
            'question': q.question,
            'options': json.loads(q.options) if isinstance(q.options, str) else q.options,
            'correct_answer': q.correct_answer,
            'module_type': q.module_type
        } for q in questions]
    })


# ==================== 排行榜API ====================

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取排行榜"""
    students = Student.query.all()
    leaderboard = []
    for student in students:
        answers = StudentAnswer.query.filter_by(student_id=student.id).all()
        total = len(answers)
        correct = sum(1 for a in answers if a.is_correct)
        score = int((correct / total * 100)) if total > 0 else 0
        leaderboard.append({
            'student_id': student.id,
            'name': student.name,
            'class_name': student.class_name,
            'score': score,
            'total': total,
            'correct': correct
        })
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({'leaderboard': leaderboard[:20]})


# ==================== 教师后台API ====================

@app.route('/api/teacher/login', methods=['POST'])
def teacher_login():
    data = request.json
    teacher = Teacher.query.filter_by(
        username=data.get('username'),
        password=data.get('password')
    ).first()
    if teacher:
        return jsonify({
            'success': True,
            'teacher_id': teacher.id,
            'message': '登录成功'
        })
    return jsonify({
        'success': False,
        'message': '用户名或密码错误'
    }), 401


@app.route('/api/teacher/statistics', methods=['GET'])
def get_statistics():
    """获取整体统计数据"""
    students = Student.query.all()
    total_students = len(students)
    answers = StudentAnswer.query.all()
    total_answers = len(answers)
    correct_answers = sum(1 for a in answers if a.is_correct)
    avg_score = int((correct_answers / total_answers * 100)) if total_answers > 0 else 0
    
    # 按模块统计
    module_stats = {}
    for module in ['explore', 'learn', 'practice', 'challenge']:
        module_answers = [a for a in answers if a.module_type == module]
        module_total = len(module_answers)
        module_correct = sum(1 for a in module_answers if a.is_correct)
        module_stats[module] = {
            'total': module_total,
            'correct': module_correct,
            'accuracy': int((module_correct / module_total * 100)) if module_total > 0 else 0
        }
    
    return jsonify({
        'total_students': total_students,
        'total_answers': total_answers,
        'correct_answers': correct_answers,
        'avg_score': avg_score,
        'module_stats': module_stats
    })


@app.route('/api/teacher/wrong-questions', methods=['GET'])
def get_wrong_questions():
    """获取错题分析"""
    wrong_answers = StudentAnswer.query.filter_by(is_correct=False).all()
    
    # 按题目分组统计错误率
    question_stats = {}
    for answer in wrong_answers:
        qid = answer.question_id
        if qid not in question_stats:
            question = Question.query.get(qid)
            question_stats[qid] = {
                'question_id': qid,
                'question': question.question if question else '题目已删除',
                'total_attempts': 0,
                'wrong_count': 0,
                'wrong_students': []
            }
        question_stats[qid]['wrong_count'] += 1
        question_stats[qid]['wrong_students'].append(answer.student_id)
    
    # 计算总尝试次数
    all_answers = StudentAnswer.query.all()
    for answer in all_answers:
        qid = answer.question_id
        if qid in question_stats:
            question_stats[qid]['total_attempts'] += 1
    
    # 计算错误率并排序
    result = []
    for qid, stats in question_stats.items():
        error_rate = int((stats['wrong_count'] / stats['total_attempts'] * 100)) if stats['total_attempts'] > 0 else 0
        result.append({
            **stats,
            'error_rate': error_rate,
            'wrong_students': list(set(stats['wrong_students']))
        })
    
    result.sort(key=lambda x: x['error_rate'], reverse=True)
    return jsonify({'wrong_questions': result})


@app.route('/api/teacher/students', methods=['GET'])
def get_all_students():
    """获取所有学生列表及成绩"""
    students = Student.query.all()
    result = []
    for student in students:
        answers = StudentAnswer.query.filter_by(student_id=student.id).all()
        total = len(answers)
        correct = sum(1 for a in answers if a.is_correct)
        score = int((correct / total * 100)) if total > 0 else 0
        result.append({
            'id': student.id,
            'name': student.name,
            'class_name': student.class_name,
            'total': total,
            'correct': correct,
            'score': score
        })
    return jsonify({'students': result})


if __name__ == '__main__':
    # 生产环境关闭调试模式
    # 打包后的程序由启动脚本负责打开浏览器
    app.run(debug=False, port=5000, host='127.0.0.1')
