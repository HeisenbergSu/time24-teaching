<template>
  <div class="challenge-module">
    <h2 class="module-title">成就挑战</h2>
    
    <!-- 烟花容器 -->
    <div class="fireworks-container" v-show="showFireworks">
      <div class="firework" v-for="i in 20" :key="i" :style="getFireworkStyle(i)"></div>
    </div>
    
    <!-- 综合测验 -->
    <div class="section">
      <h3>综合测验</h3>
      <p class="section-desc">
        让我们来检验一下学习成果吧！完成以下所有题目，看看你能得多少分！
      </p>
      
      <div v-if="!loading && questions.length > 0" class="questions-container">
        <div v-for="(question, index) in questions" :key="question.id" class="question-card">
          <div class="question-header">
            <span class="question-number">第{{ index + 1 }}题</span>
            <el-tag :type="answeredQuestions[question.id] ? (answers[question.id]?.isCorrect ? 'success' : 'danger') : ''">
              {{ answeredQuestions[question.id] ? (answers[question.id]?.isCorrect ? '答对了' : '答错了') : '未作答' }}
            </el-tag>
          </div>
          <p class="question-text">{{ question.question }}</p>
          <div class="options">
            <el-radio-group 
              v-model="userAnswers[question.id]" 
              @change="(val) => handleAnswerChange(question, val)"
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
            <p :class="answers[question.id]?.isCorrect ? 'correct' : 'wrong'">
              {{ answers[question.id]?.isCorrect ? '✓ 答对了！' : `✗ 答错了，正确答案是：${question.correct_answer}` }}
            </p>
          </div>
        </div>
        
        <!-- 提交按钮和成绩显示 - 移到题目列表下方 -->
        <div class="submit-section">
          <el-button 
            v-if="!showScore"
            type="primary" 
            size="large" 
            @click="submitTest"
            :disabled="!allAnswered"
          >
            <template v-if="allAnswered">
              查看成绩
            </template>
            <template v-else>
              还有 {{ unansweredCount }} 题未完成
            </template>
          </el-button>
          
          <div v-if="showScore" class="score-display">
            <el-card class="score-card">
              <div class="score-content">
                <div class="score-icon">{{ score === 100 ? '🏆' : score >= 80 ? '✨' : score >= 60 ? '👍' : '💪' }}</div>
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
        </div>
      </div>
      
      <div v-else-if="loading" class="loading">
        <el-icon class="is-loading"><i class="el-icon-loading"></i></el-icon>
        <p>加载题目中...</p>
      </div>
    </div>
    
    <!-- 排行榜 -->
    <div class="section">
      <h3>排行榜</h3>
      <p class="section-desc">看看你的成绩在全班排名第几吧！</p>
      
      <div class="leaderboard-container">
        <el-table :data="leaderboard" style="width: 100%">
          <el-table-column type="index" label="排名" width="80" align="center">
            <template slot-scope="scope">
              <span class="rank-badge" :class="getRankClass(scope.$index)">
                {{ scope.$index + 1 }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="150"></el-table-column>
          <el-table-column prop="class_name" label="班级" width="150"></el-table-column>
          <el-table-column prop="score" label="得分" width="120" align="center">
            <template slot-scope="scope">
              <span class="score-text">{{ scope.row.score }}分</span>
            </template>
          </el-table-column>
          <el-table-column prop="correct" label="正确题数" width="120" align="center">
            <template slot-scope="scope">
              {{ scope.row.correct }} / {{ scope.row.total }}
            </template>
          </el-table-column>
        </el-table>
        
        <el-button @click="loadLeaderboard" style="margin-top: 20px;" type="primary">
          刷新排行榜
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChallengeModule',
  props: {
    studentId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      questions: [],
      userAnswers: {},
      answeredQuestions: {},
      answers: {},
      showScore: false,
      score: 0,
      correctCount: 0,
      totalCount: 0,
      leaderboard: [],
      loading: true,
      showFireworks: false,
      answeredCount: 0
    }
  },
  computed: {
    allAnswered() {
      if (this.questions.length === 0) return false
      // 同时检查 answeredCount 和实际 answeredQuestions 的长度
      const actualAnsweredCount = Object.keys(this.answeredQuestions).length
      return actualAnsweredCount === this.questions.length && this.answeredCount === this.questions.length
    },
    unansweredCount() {
      // 计算实际未答题数
      const actualAnsweredCount = Object.keys(this.answeredQuestions).length
      const count = Math.max(0, this.questions.length - actualAnsweredCount)
      return count
    }
  },
  watch: {
    // 监听 answeredQuestions 的变化，自动更新 answeredCount
    answeredQuestions: {
      handler(newVal) {
        const count = Object.keys(newVal).length
        if (count !== this.answeredCount) {
          this.answeredCount = count
          console.log('已回答数量更新:', count, '/', this.questions.length)
        }
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.loadQuestions()
    this.loadLeaderboard()
  },
  methods: {
    async loadQuestions() {
      this.loading = true
      try {
        const res = await this.$http.get('/questions/challenge')
        this.questions = res.data.questions || []
        this.totalCount = this.questions.length
        
        // 从 localStorage 恢复答题状态
        this.loadAnswersFromStorage()
      } catch (error) {
        this.$message.error('加载题目失败')
      } finally {
        this.loading = false
      }
    },
    loadAnswersFromStorage() {
      const saved = localStorage.getItem(`answers_challenge_${this.studentId}`)
      if (saved) {
        try {
          const parsed = JSON.parse(saved)
          const savedAnsweredQuestions = parsed.answeredQuestions || {}
          const savedAnswers = parsed.answers || {}
          const savedUserAnswers = parsed.userAnswers || {}
          
          // 确保只恢复当前题目列表中存在的题目
          const validAnsweredQuestions = {}
          const validAnswers = {}
          const validUserAnswers = {}
          
          this.questions.forEach(q => {
            if (savedAnsweredQuestions[q.id]) {
              validAnsweredQuestions[q.id] = savedAnsweredQuestions[q.id]
              validAnswers[q.id] = savedAnswers[q.id]
              validUserAnswers[q.id] = savedUserAnswers[q.id]
            }
          })
          
          // 使用 $set 逐个设置，确保响应式
          this.answeredQuestions = {}
          this.answers = {}
          this.userAnswers = {}
          
          Object.keys(validAnsweredQuestions).forEach(qid => {
            this.$set(this.answeredQuestions, qid, validAnsweredQuestions[qid])
            if (validAnswers[qid]) {
              this.$set(this.answers, qid, validAnswers[qid])
            }
            if (validUserAnswers[qid]) {
              this.$set(this.userAnswers, qid, validUserAnswers[qid])
            }
          })
          
          // 更新已答题计数
          this.answeredCount = Object.keys(this.answeredQuestions).length
          
          console.log('恢复答题状态:', this.answeredCount, '/', this.questions.length, '已回答的题目:', Object.keys(this.answeredQuestions))
        } catch (error) {
          console.error('恢复答题状态失败:', error)
        }
      } else {
        // 如果没有保存的数据，重置计数
        this.answeredCount = 0
      }
    },
    saveAnswersToStorage() {
      localStorage.setItem(`answers_challenge_${this.studentId}`, JSON.stringify({
        answeredQuestions: this.answeredQuestions,
        answers: this.answers,
        userAnswers: this.userAnswers
      }))
    },
    handleAnswerChange(question, answer) {
      // 如果已经回答过，不重复处理
      if (this.answeredQuestions[question.id] || !answer) {
        return
      }
      
      const isCorrect = answer === question.correct_answer
      
      // 使用 $set 确保响应式更新
      this.$set(this.answeredQuestions, question.id, true)
      this.$set(this.answers, question.id, {
        isCorrect: isCorrect,
        answer: answer
      })
      
      // answeredCount 会通过 watch 自动更新，但我们也手动更新一下确保同步
      this.answeredCount = Object.keys(this.answeredQuestions).length
      
      // 保存到 localStorage
      this.saveAnswersToStorage()
      
      console.log('已答题:', this.answeredCount, '/', this.questions.length, '题目ID:', question.id)
      
      // 立即显示反馈
      if (isCorrect) {
        this.$message.success('答对了！')
      } else {
        this.$message.error(`答错了，正确答案是：${question.correct_answer}`)
      }
      
      // 异步提交到服务器（不阻塞界面）
      this.submitAnswerToServer(question, answer, isCorrect)
      
      // 检查是否全部答完
      this.$nextTick(() => {
        const actualCount = Object.keys(this.answeredQuestions).length
        const allDone = actualCount === this.questions.length && this.questions.length > 0
        console.log('检查是否全部答完:', allDone, '已答:', actualCount, '总数:', this.questions.length)
        
        if (allDone) {
          setTimeout(() => {
            this.submitTest()
          }, 500)
        }
      })
    },
    async submitAnswerToServer(question, answer, isCorrect) {
      try {
        await this.$http.post(`/student/${this.studentId}/answers`, {
          question_id: question.id,
          answer: answer,
          is_correct: isCorrect,
          module_type: 'challenge'
        })
      } catch (error) {
        console.error('提交答案到服务器失败:', error)
        // 不影响本地显示，只在后台记录错误
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
      
      // 如果全对，显示烟花
      if (this.score === 100) {
        this.showFireworks = true
        setTimeout(() => {
          this.showFireworks = false
        }, 5000)
      }
      
      // 刷新排行榜
      this.loadLeaderboard()
      
      // 滚动到成绩显示区域
      this.$nextTick(() => {
        const scoreDisplay = document.querySelector('.score-display')
        if (scoreDisplay) {
          scoreDisplay.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      })
      
      this.$message.success('提交成功！')
    },
    getFireworkStyle(index) {
      // 生成烟花样式：从两侧弹出
      const isLeft = index % 2 === 0
      const startX = isLeft ? '0%' : '100%'
      const endX = Math.random() * 30 + (isLeft ? 10 : 60) + '%'
      const endY = Math.random() * 50 + 10 + '%'
      const delay = Math.random() * 2
      const duration = Math.random() * 2 + 2
      const size = Math.random() * 100 + 50
      const hue = Math.random() * 360
      
      return {
        '--start-x': startX,
        '--end-x': endX,
        '--end-y': endY,
        '--size': size + 'px',
        '--hue': hue,
        'animation-delay': delay + 's',
        'animation-duration': duration + 's'
      }
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
    }
  }
}
</script>

<style scoped>
.challenge-module {
  padding: 20px;
  position: relative;
}

.module-title {
  font-size: 28px;
  color: #667eea;
  margin-bottom: 30px;
  text-align: center;
}

/* 烟花效果 */
.fireworks-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
  overflow: hidden;
}

.firework {
  position: absolute;
  width: var(--size);
  height: var(--size);
  border-radius: 50%;
  background: radial-gradient(circle, 
    hsla(var(--hue), 100%, 70%, 1) 0%, 
    hsla(var(--hue), 100%, 60%, 0.8) 30%,
    hsla(var(--hue), 100%, 50%, 0) 70%);
  box-shadow: 
    0 0 20px hsla(var(--hue), 100%, 60%, 0.8),
    0 0 40px hsla(var(--hue), 100%, 50%, 0.5);
  animation: firework-fly 3s ease-out forwards, firework-burst 1s 2.5s ease-out forwards;
  opacity: 0;
}

@keyframes firework-fly {
  0% {
    left: var(--start-x);
    bottom: -100px;
    opacity: 1;
    transform: scale(0.3);
  }
  70% {
    left: var(--end-x);
    bottom: var(--end-y);
    opacity: 1;
    transform: scale(0.8);
  }
  100% {
    left: var(--end-x);
    bottom: var(--end-y);
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes firework-burst {
  0% {
    opacity: 1;
    transform: scale(1);
    filter: brightness(2);
  }
  50% {
    opacity: 1;
    transform: scale(1.5);
    filter: brightness(1.5);
  }
  100% {
    opacity: 0;
    transform: scale(2);
    filter: brightness(0.5);
  }
}

.section {
  margin-bottom: 50px;
  padding: 30px;
  background: #f5f7fa;
  border-radius: 10px;
}

.section h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 15px;
}

.section-desc {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-number {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.question-text {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.6;
}

.options {
  margin-bottom: 15px;
}

.option-item {
  display: block;
  margin-bottom: 10px;
  font-size: 16px;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s;
}

.option-item:hover {
  background: #f0f0f0;
}

.answer-feedback {
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
}

.answer-feedback .correct {
  color: #67c23a;
  font-weight: bold;
}

.answer-feedback .wrong {
  color: #f56c6c;
  font-weight: bold;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.submit-section {
  margin-top: 30px;
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.score-display {
  margin-top: 30px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.score-card {
  max-width: 500px;
  margin: 0 auto;
  border: 3px solid #667eea;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.score-content {
  text-align: center;
  padding: 30px;
}

.score-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

.score-number {
  font-size: 56px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 15px;
  animation: pulse 1s ease-in-out infinite alternate;
}

@keyframes pulse {
  from {
    text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
  }
  to {
    text-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
  }
}

.score-desc {
  font-size: 20px;
  color: #666;
  margin-bottom: 20px;
}

.score-badge {
  margin-top: 20px;
}

.score-badge .el-tag {
  font-size: 18px;
  padding: 12px 24px;
}

.leaderboard-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.rank-badge {
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  border-radius: 50%;
  font-weight: bold;
  background: #f0f0f0;
  color: #333;
}

.rank-badge.rank-gold {
  background: #ffd700;
  color: #fff;
}

.rank-badge.rank-silver {
  background: #c0c0c0;
  color: #fff;
}

.rank-badge.rank-bronze {
  background: #cd7f32;
  color: #fff;
}

.score-text {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}
</style>

