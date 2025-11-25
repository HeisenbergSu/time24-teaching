"""初始化题目数据"""
import json
from app import app
from models import db, Question

# 课前探索题目（旧知复习）
explore_questions = [
    {
        'question': '一小时有多少分钟？',
        'options': json.dumps(['30分钟', '100分钟', '60分钟', '45分钟']),
        'correct_answer': '60分钟',
        'module_type': 'explore'  
    },
    {
        'question': '钟表上最短的指针是什么针？',
        'options': json.dumps(['时针', '分针', '秒针', '指针一样长']),
        'correct_answer': '时针',
        'module_type': 'explore'
    },
    {
        'question': '夏天午睡大约用1（）。',
        'options': json.dumps(['小时', '天', '分钟', '秒']),
        'correct_answer': '小时',
        'module_type': 'explore'
    },
    {
        'question': '现在是上午9点，再过3小时是几点？',
        'options': json.dumps(['上午10点', '上午11点', '中午12点', '下午1点']),
        'correct_answer': '中午12点',
        'module_type': 'explore'
    }
]

# 生活应用题目
practice_questions = [
    {
        'question': '这是某公交车的站牌，我们平时几点到公交站可以坐公交车？',
        'options': json.dumps(['早上5点', '晚上10点', '晚上11点半', '上午8点']),
        'correct_answer': '上午8点',
        'module_type': 'practice'
    },
    {
        'question': '这是一张电影票。我们应该几点到电影院比较合适呢？',
        'options': json.dumps(['上午10点', '下午1点', '晚上7点', '晚上9点']),
        'correct_answer': '晚上7点',
        'module_type': 'practice'
    },
    {
        'question': '早上9点用24时计时法表示是？',
        'options': json.dumps(['09:00', '21:00', '19:00', '29:00']),
        'correct_answer': '09:00',
        'module_type': 'practice'
    },
    {
        'question': '晚上9点用24时计时法表示是？',
        'options': json.dumps(['09:00', '21:00', '19:00', '29:00']),
        'correct_answer': '21:00',
        'module_type': 'practice'
    },
    {
        'question': '咖啡店17:30关门，我们需要至少几点到？',
        'options': json.dumps(['早上5点半', '下午5点半之前', '晚上7点半', '中午12点']),
        'correct_answer': '下午5点半之前',
        'module_type': 'practice'
    },
    {
        'question': '14:00对应的是12时计时法的什么时候？',
        'options': json.dumps(['早上2点', '中午12点', '下午2点', '晚上8点']),
        'correct_answer': '下午2点',
        'module_type': 'practice'
    }
]

# 成就挑战题目
challenge_questions = [
    {
        'question': '钟表一天转几圈？',
        'options': json.dumps(['1圈', '2圈', '3圈', '4圈']),
        'correct_answer': '2圈',
        'module_type': 'challenge'
    },
    {
        'question': '早上8点和晚上8点，时针的位置相同吗？',
        'options': json.dumps(['相同', '不同', '有时相同', '无法确定']),
        'correct_answer': '相同',
        'module_type': 'challenge'
    },
    {
        'question': '23:00用12时计时法表示是？',
        'options': json.dumps(['早上11点', '中午11点', '晚上11点', '下午3点']),
        'correct_answer': '晚上11点',
        'module_type': 'challenge'
    },
    {
        'question': '下午3点用24时计时法表示是？',
        'options': json.dumps(['03:00', '13:00', '15:00', '23:00']),
        'correct_answer': '15:00',
        'module_type': 'challenge'
    },
    {
        'question': '从早上8点到晚上8点，时针转了多少圈？',
        'options': json.dumps(['0圈', '1圈', '2圈', '3圈']),
        'correct_answer': '1圈',
        'module_type': 'challenge'
    }
]

def init_questions():
    with app.app_context():
        # 清空现有题目（可选）
        # Question.query.delete()
        # db.session.commit()
        
        # 添加题目
        all_questions = explore_questions + practice_questions + challenge_questions
        for q_data in all_questions:
            existing = Question.query.filter_by(question=q_data['question']).first()
            if not existing:
                question = Question(**q_data)
                db.session.add(question)
        
        db.session.commit()
        print(f'已添加 {len(all_questions)} 道题目')

if __name__ == '__main__':
    init_questions()
