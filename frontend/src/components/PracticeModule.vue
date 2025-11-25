<template>
  <div class="practice-module">
    <h2 class="module-title">生活应用</h2>
    
    <!-- 12时计时法与24时计时法转换 -->
    <div class="section">
      <h3>12时计时法与24时计时法</h3>
      <p class="section-desc">
        在生活中，我们有两种表示时间的方法：12时计时法（上午8时、晚上8时）和24时计时法（08:00、20:00）。
        让我们来学习它们的转换关系吧！
      </p>
      
      <!-- 时间尺 -->
      <div class="time-scale-container">
        <h4>时间尺 - 把钟面化曲为直</h4>
        <TimeScale @time-select="handleTimeSelect"/>
      </div>
      
      <!-- 转换规则 -->
      <div class="conversion-rules">
        <el-card>
          <h4>转换规则</h4>
          <div class="rules-content">
            <div class="rule-item">
              <div class="rule-title">上午/中午：</div>
              <div class="rule-desc">12时计时法 = 24时计时法（0:00-12:00）</div>
              <div class="rule-example">例如：上午8时 = 08:00</div>
            </div>
            <div class="rule-item">
              <div class="rule-title">下午/晚上：</div>
              <div class="rule-desc">24时计时法 = 12时计时法 + 12</div>
              <div class="rule-example">例如：晚上8时（8时+12）= 20:00</div>
            </div>
            <div class="rule-item">
              <div class="rule-title">反过来：</div>
              <div class="rule-desc">24时计时法 → 12时计时法：大于12就减12</div>
              <div class="rule-example">例如：20:00（20-12）= 晚上8时</div>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 生活场景练习 -->
    <div class="section">
      <h3>生活场景练习</h3>
      <p class="section-desc">让我们在实际生活场景中应用24时计时法！</p>
      
      <div v-if="questions.length > 0" class="questions-container">
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
            <p :class="answers[question.id]?.isCorrect ? 'correct' : 'wrong'">
              {{ answers[question.id]?.isCorrect ? '✓ 答对了！' : `✗ 答错了，正确答案是：${question.correct_answer}` }}
            </p>
          </div>
        </div>
      </div>
      
      <div v-else class="loading">
        <el-icon class="is-loading"><i class="el-icon-loading"></i></el-icon>
        <p>加载题目中...</p>
      </div>
    </div>
  </div>
</template>

<script>
import TimeScale from './TimeScale.vue'

export default {
  name: 'PracticeModule',
  components: {
    TimeScale
  },
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
      answers: {}
    }
  },
  mounted() {
    this.loadQuestions()
  },
  methods: {
    async loadQuestions() {
      try {
        const res = await this.$http.get('/questions/practice')
        this.questions = res.data.questions || []
      } catch (error) {
        this.$message.error('加载题目失败')
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
          module_type: 'practice'
        })
        
        this.answeredQuestions[question.id] = true
        this.answers[question.id] = {
          isCorrect: isCorrect,
          answer: answer
        }
        
        if (isCorrect) {
          this.$message.success('答对了！')
        } else {
          this.$message.error(`答错了，正确答案是：${question.correct_answer}`)
        }
      } catch (error) {
        this.$message.error('提交答案失败')
      }
    },
    handleTimeSelect(time) {
      this.$message.info(`你选择了：${time}`)
    }
  }
}
</script>

<style scoped>
.practice-module {
  padding: 20px;
}

.module-title {
  font-size: 28px;
  color: #667eea;
  margin-bottom: 30px;
  text-align: center;
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

.time-scale-container {
  margin: 30px 0;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.time-scale-container h4 {
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.conversion-rules {
  margin-top: 30px;
}

.conversion-rules h4 {
  font-size: 20px;
  color: #667eea;
  margin-bottom: 20px;
  text-align: center;
}

.rules-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.rule-item {
  padding: 20px;
  background: #f0f0f0;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.rule-title {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.rule-desc {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.6;
}

.rule-example {
  font-size: 14px;
  color: #666;
  font-style: italic;
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
</style>

