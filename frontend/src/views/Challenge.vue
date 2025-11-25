<template>
  <div class="challenge-page">
    <div class="page-header">
      <el-button 
        @click="goBack" 
        icon="el-icon-arrow-left" 
        circle
        class="back-button"
      ></el-button>
      <h1 class="page-title">成就挑战</h1>
    </div>
    
    <!-- 综合测验 -->
    <el-card class="section-card">
      <h2 class="section-title">🎯 综合测验</h2>
      <p class="section-desc">
        让我们来检验一下学习成果吧！完成以下所有题目，看看你能得多少分！
      </p>
      
      <div v-if="questions.length > 0" class="questions-container">
        <div 
          v-for="(question, index) in questions" 
          :key="question.id" 
          class="question-card"
        >
          <div class="question-header">
            <span class="question-number">第 {{ index + 1 }} 题</span>
            <el-tag 
              v-if="answeredQuestions[question.id]"
              :type="answers[question.id]?.isCorrect ? 'success' : 'danger'"
            >
              {{ answers[question.id]?.isCorrect ? '答对了' : '答错了' }}
            </el-tag>
          </div>
          <p class="question-text">{{ question.question }}</p>
          <div class="options">
            <el-radio-group 
              v-model="userAnswers[question.id]" 
              @change="answerQuestion(question, $event)"
              :disabled="answeredQuestions[question.id]"
            >
              <el-radio 
                v-for="(option, optIndex) in question.options" 
                :key="optIndex" 
                :label="option"
                class="option-item"
              >
                {{ option }}
              </el-radio>
            </el-radio-group>
          </div>
          <div v-if="answeredQuestions[question.id]" class="answer-feedback">
            <div :class="answers[question.id]?.isCorrect ? 'correct' : 'wrong'">
              <i :class="answers[question.id]?.isCorrect ? 'el-icon-success' : 'el-icon-error'"></i>
              <span v-if="answers[question.id]?.isCorrect">
                答对了！
              </span>
              <span v-else>
                答错了，正确答案是：{{ question.correct_answer }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="loading">
        <i class="el-icon-loading"></i>
        <p>加载题目中...</p>
      </div>
      
      <!-- 提交按钮和成绩显示 -->
      <div class="submit-section">
        <el-button 
          type="primary" 
          size="large" 
          @click="submitTest"
          :disabled="!allAnswered"
          class="submit-button"
        >
          {{ allAnswered ? '查看成绩' : `还有 ${unansweredCount} 题未完成` }}
        </el-button>
        
        <el-card v-if="showScore" class="score-card" shadow="always">
          <div class="score-content">
            <div class="score-icon">🎉</div>
            <div class="score-number">{{ score }}分</div>
            <div class="score-desc">
              答对了 {{ correctCount }} 题，共 {{ totalCount }} 题
            </div>
            <div class="score-badge" v-if="score === 100">
              <el-tag type="success" size="large">🏆 满分！太棒了！</el-tag>
            </div>
            <div class="score-badge" v-else-if="score >= 80">
              <el-tag type="success" size="large">✨ 优秀！</el-tag>
            </div>
            <div class="score-badge" v-else-if="score >= 60">
              <el-tag type="warning" size="large">👍 良好！</el-tag>
            </div>
            <div class="score-badge" v-else>
              <el-tag type="info" size="large">💪 继续加油！</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>
    
    <!-- 排行榜 -->
    <el-card class="section-card">
      <h2 class="section-title">🏆 排行榜</h2>
      <p class="section-desc">看看你的成绩在全班排名第几吧！</p>
      
      <div class="leaderboard-container">
        <el-table :data="leaderboard" style="width: 100%">
          <el-table-column type="index" label="排名" width="100" align="center">
            <template slot-scope="scope">
              <span class="rank-badge" :class="getRankClass(scope.$index)">
                {{ scope.$index + 1 }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="150"></el-table-column>
          <el-table-column prop="class_name" label="班级" width="150"></el-table-column>
          <el-table-column prop="score" label="得分" width="150" align="center">
            <template slot-scope="scope">
              <span class="score-text">{{ scope.row.score }}分</span>
            </template>
          </el-table-column>
          <el-table-column prop="correct" label="正确题数" width="150" align="center">
            <template slot-scope="scope">
              {{ scope.row.correct }} / {{ scope.row.total }}
            </template>
          </el-table-column>
        </el-table>
        
        <div class="refresh-section">
          <el-button @click="loadLeaderboard" type="primary" icon="el-icon-refresh">
            刷新排行榜
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Challenge',
  data() {
    return {
      studentId: null,
      questions: [],
      userAnswers: {},
      answeredQuestions: {},
      answers: {},
      showScore: false,
      score: 0,
      correctCount: 0,
      totalCount: 0,
      leaderboard: []
    }
  },
  computed: {
    allAnswered() {
      return this.questions.length > 0 && 
             this.questions.every(q => this.answeredQuestions[q.id])
    },
    unansweredCount() {
      return this.questions.length - Object.keys(this.answeredQuestions).length
    }
  },
  mounted() {
    const savedStudentId = localStorage.getItem('studentId')
    if (savedStudentId) {
      this.studentId = parseInt(savedStudentId)
    }
    this.loadQuestions()
    this.loadLeaderboard()
    this.checkAnsweredQuestions()
  },
  methods: {
    async loadQuestions() {
      try {
        const res = await this.$http.get('/questions/challenge')
        this.questions = res.data.questions || []
        this.totalCount = this.questions.length
      } catch (error) {
        this.$message.error('加载题目失败')
      }
    },
    checkAnsweredQuestions() {
      const saved = localStorage.getItem(`answers_challenge_${this.studentId}`)
      if (saved) {
        const parsed = JSON.parse(saved)
        // 使用 $set 逐个恢复，确保响应式
        const answeredQuestions = parsed.answeredQuestions || {}
        const answers = parsed.answers || {}
        
        Object.keys(answeredQuestions).forEach(qid => {
          this.$set(this.answeredQuestions, qid, answeredQuestions[qid])
        })
        
        Object.keys(answers).forEach(qid => {
          this.$set(this.answers, qid, answers[qid])
          // 恢复用户选择的答案
          if (answers[qid] && answers[qid].answer) {
            this.$set(this.userAnswers, qid, answers[qid].answer)
          }
        })
      }
    },
    async answerQuestion(question, answer) {
      if (this.answeredQuestions[question.id]) return
      
      const isCorrect = answer === question.correct_answer
      
      try {
        await this.$http.post(`/student/${this.studentId}/answers`, {
          question_id: question.id,
          answer: answer,
          is_correct: isCorrect,
          module_type: 'challenge'
        })
        
        // 使用 $set 确保响应式更新
        this.$set(this.answeredQuestions, question.id, true)
        this.$set(this.answers, question.id, {
          isCorrect: isCorrect,
          answer: answer
        })
        this.$set(this.userAnswers, question.id, answer)
        
        localStorage.setItem(`answers_challenge_${this.studentId}`, JSON.stringify({
          answeredQuestions: this.answeredQuestions,
          answers: this.answers
        }))
        
        if (isCorrect) {
          this.$message.success('答对了！')
        } else {
          this.$message.error(`答错了，正确答案是：${question.correct_answer}`)
        }
      } catch (error) {
        this.$message.error('提交答案失败')
      }
    },
    submitTest() {
      if (!this.allAnswered) {
        this.$message.warning('请完成所有题目后再提交')
        return
      }
      
      // 计算成绩
      this.correctCount = Object.values(this.answers).filter(a => a.isCorrect).length
      this.score = Math.round((this.correctCount / this.totalCount) * 100)
      this.showScore = true
      
      // 刷新排行榜
      this.loadLeaderboard()
      
      this.$message.success('提交成功！')
    },
    async loadLeaderboard() {
      try {
        const res = await this.$http.get('/leaderboard')
        this.leaderboard = res.data.leaderboard || []
      } catch (error) {
        this.$message.error('加载排行榜失败')
      }
    },
    getRankClass(index) {
      if (index === 0) return 'rank-gold'
      if (index === 1) return 'rank-silver'
      if (index === 2) return 'rank-bronze'
      return ''
    },
    goBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.challenge-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 50%, #fff3e0 100%);
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.back-button {
  font-size: 20px;
}

.page-title {
  font-size: 36px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.section-card {
  max-width: 1200px;
  margin: 0 auto 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 28px;
  color: #333;
  margin-bottom: 12px;
}

.section-desc {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.6;
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.question-card {
  background: #fafafa;
  padding: 30px;
  border-radius: 12px;
  border: 2px solid #e4e7ed;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-number {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.question-text {
  font-size: 18px;
  color: #333;
  margin-bottom: 25px;
  line-height: 1.6;
  font-weight: 500;
}

.options {
  margin-bottom: 20px;
}

.option-item {
  display: flex;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 12px;
  font-size: 16px;
  padding: 12px 16px;
  border-radius: 8px;
  background: white;
  border: 2px solid #e4e7ed;
  transition: all 0.3s;
  white-space: normal;
  height: auto;
  line-height: 1.5;
}

.option-item:last-child {
  margin-bottom: 0;
}

.option-item >>> .el-radio__label {
  white-space: normal;
  display: inline-block;
  vertical-align: middle;
  text-align: left;
  width: 100%;
}

.option-item:hover {
  border-color: #667eea;
  background: #f0f2ff;
}

.answer-feedback {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
}

.answer-feedback .correct {
  color: #67c23a;
  font-weight: bold;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.answer-feedback .wrong {
  color: #f56c6c;
  font-weight: bold;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}

.loading i {
  font-size: 32px;
  margin-bottom: 15px;
}

.submit-section {
  margin-top: 40px;
  text-align: center;
}

.submit-button {
  font-size: 18px;
  height: 50px;
  padding: 0 40px;
}

.score-card {
  margin-top: 30px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.score-content {
  text-align: center;
  padding: 30px;
  color: white;
}

.score-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.score-number {
  font-size: 56px;
  font-weight: bold;
  margin-bottom: 12px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.score-desc {
  font-size: 20px;
  margin-bottom: 20px;
  opacity: 0.9;
}

.score-badge {
  margin-top: 20px;
}

.leaderboard-container {
  padding: 20px;
  background: #fafafa;
  border-radius: 12px;
}

.rank-badge {
  display: inline-block;
  width: 36px;
  height: 36px;
  line-height: 36px;
  text-align: center;
  border-radius: 50%;
  font-weight: bold;
  background: #f0f0f0;
  color: #333;
  font-size: 16px;
}

.rank-badge.rank-gold {
  background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
  color: white;
}

.rank-badge.rank-silver {
  background: linear-gradient(135deg, #c0c0c0 0%, #a8a8a8 100%);
  color: white;
}

.rank-badge.rank-bronze {
  background: linear-gradient(135deg, #cd7f32 0%, #b87333 100%);
  color: white;
}

.score-text {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.refresh-section {
  margin-top: 20px;
  text-align: center;
}
</style>

