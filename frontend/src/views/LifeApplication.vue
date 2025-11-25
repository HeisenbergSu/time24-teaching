<template>
  <div class="life-application-page">
    <div class="page-header">
      <el-button 
        @click="goBack" 
        icon="el-icon-arrow-left" 
        circle
        class="back-button"
      ></el-button>
      <h1 class="page-title">生活应用</h1>
    </div>
    
    <!-- 主内容区 -->
    <div class="main-content" :class="{ 'mode-quiz': quizStarted }">
      
      <!-- 12时计时法与24时计时法转换 (规则区) -->
      <!-- 规则放在这里，flex-order调整位置或者放在DOM前面? -->
      <!-- 用户要求：卡片在右侧。 -->
      <!-- 答题区在左侧，规则区在右侧。 -->
      
      <!-- 生活场景练习 (答题区) -->
      <div class="quiz-section" v-if="quizStarted">
        <el-card class="section-card quiz-card">
          <div class="quiz-header">
            <h2 class="section-title">🎯 生活场景练习</h2>
            <div class="quiz-progress">
              进度：{{ currentQuestionIndex + 1 }} / {{ questions.length }}
            </div>
          </div>
          
          <div v-if="questions.length > 0" class="questions-container">
            <div 
              v-if="currentQuestion"
              :key="currentQuestion.id" 
              class="question-card active-question"
            >
              <div class="question-header">
                <span class="question-number">第 {{ currentQuestionIndex + 1 }} 题</span>
                <el-tag 
                  v-if="answeredQuestions[currentQuestion.id]"
                  :type="answers[currentQuestion.id]?.isCorrect ? 'success' : 'danger'"
                >
                  {{ answers[currentQuestion.id]?.isCorrect ? '答对了' : '答错了' }}
                </el-tag>
              </div>
              
              <div class="question-content">
                <div class="question-image-container" v-if="currentQuestion.image">
                  <img :src="currentQuestion.image" class="question-image" alt="场景图片">
                </div>
                <div class="question-main">
                  <p class="question-text">{{ currentQuestion.question }}</p>
                  <div class="options">
                    <el-radio-group 
                      v-model="userAnswers[currentQuestion.id]" 
                      @change="answerQuestion(currentQuestion, $event)"
                      :disabled="answeredQuestions[currentQuestion.id]"
                      class="options-group"
                    >
                      <el-radio 
                        v-for="(option, optIndex) in currentQuestion.options" 
                        :key="optIndex" 
                        :label="option"
                        class="option-item"
                      >
                        {{ option }}
                      </el-radio>
                    </el-radio-group>
                  </div>
                </div>
              </div>

              <div v-if="answeredQuestions[currentQuestion.id]" class="answer-feedback">
                <div :class="answers[currentQuestion.id]?.isCorrect ? 'correct' : 'wrong'">
                  <i :class="answers[currentQuestion.id]?.isCorrect ? 'el-icon-success' : 'el-icon-error'"></i>
                  <span v-if="answers[currentQuestion.id]?.isCorrect">
                    答对了！
                  </span>
                  <span v-else>
                    答错了，正确答案是：{{ currentQuestion.correct_answer }}
                  </span>
                </div>
              </div>
              
              <!-- 导航按钮 -->
              <div class="navigation-btns">
                 <el-button @click="prevQuestion" :disabled="currentQuestionIndex === 0" icon="el-icon-arrow-left">上一题</el-button>
                 <el-button 
                   type="primary" 
                   @click="nextQuestion" 
                   v-if="currentQuestionIndex < questions.length - 1"
                   :disabled="!answeredQuestions[currentQuestion.id]"
                 >
                   下一题 <i class="el-icon-arrow-right el-icon--right"></i>
                 </el-button>
                 <el-button 
                   type="success" 
                   @click="finishQuiz" 
                   v-if="currentQuestionIndex === questions.length - 1"
                   :disabled="!answeredQuestions[currentQuestion.id]"
                 >
                   完成练习
                 </el-button>
              </div>
            </div>
          </div>
          
          <div v-else class="loading">
            <i class="el-icon-loading"></i>
            <p>加载题目中...</p>
          </div>
        </el-card>
      </div>

      <!-- 12时计时法与24时计时法转换 (规则区) -->
      <div class="rules-section">
        <el-card class="section-card rules-card">
          <h2 class="section-title">⏰ 12时计时法与24时计时法</h2>
          <p class="section-desc" v-if="!quizStarted">
            在生活中，我们有两种表示时间的方法：12时计时法（上午8时、晚上8时）和24时计时法（08:00、20:00）。
            让我们来学习它们的转换关系吧！
          </p>
          
          <!-- 转换规则 -->
          <el-card class="conversion-rules" shadow="never">
            <h3 class="rules-title">📖 转换规则</h3>
            <div class="rules-content">
              <div class="rule-item">
                <div class="rule-header">
                  <i class="el-icon-sunny"></i>
                  <div class="rule-title">上午/中午：</div>
                </div>
                <div class="rule-desc">12时计时法 = 24时计时法（0:00-12:00）</div>
                <div class="rule-example" v-if="!quizStarted">例如：上午8时 = 08:00</div>
              </div>
              <div class="rule-item">
                <div class="rule-header">
                  <i class="el-icon-moon"></i>
                  <div class="rule-title">下午/晚上：</div>
                </div>
                <div class="rule-desc">24时计时法 = 12时计时法 + 12</div>
                <div class="rule-example" v-if="!quizStarted">例如：晚上8时（8时+12）= 20:00</div>
              </div>
              <div class="rule-item">
                <div class="rule-header">
                  <i class="el-icon-refresh"></i>
                  <div class="rule-title">反过来：</div>
                </div>
                <div class="rule-desc">24时 → 12时：大于12减12</div>
                <div class="rule-example" v-if="!quizStarted">例如：20:00（20-12）= 晚上8时</div>
              </div>
            </div>
          </el-card>

          <!-- 开始按钮 (未开始时显示在这里) -->
          <div class="start-action" v-if="!quizStarted">
             <el-button type="primary" size="large" round @click="startQuiz" class="start-btn">
               开始回答 <i class="el-icon-arrow-right"></i>
             </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
// 导入图片
import img1 from '../images/1.jpg'
import img2 from '../images/2.jpg'
import img3 from '../images/3.jpg'
import img4 from '../images/4.jpg'

export default {
  name: 'LifeApplication',
  data() {
    return {
      studentId: null,
      questions: [],
      userAnswers: {},
      answeredQuestions: {},
      answers: {},
      quizStarted: false,
      currentQuestionIndex: 0
    }
  },
  computed: {
    currentQuestion() {
      if (this.questions.length === 0) return null;
      return this.questions[this.currentQuestionIndex];
    }
  },
  mounted() {
    const savedStudentId = localStorage.getItem('studentId')
    if (savedStudentId) {
      this.studentId = parseInt(savedStudentId)
    }
    this.loadQuestions()
    this.checkAnsweredQuestions()
  },
  methods: {
    loadQuestions() {
      // 使用硬编码的题目，替换原来的API调用
      this.questions = [
        {
          id: 101,
          question: '这是某公交车的站牌，我们平时几点到公交站可以坐公交车？',
          options: ['早上5点', '晚上10点', '晚上11点半', '上午8点'],
          correct_answer: '上午8点', 
          image: img1
        },
        {
          id: 102,
          question: '这是一张电影票。我们应该几点到电影院比较合适呢？',
          options: ['上午10点', '下午1点', '晚上7点', '晚上9点'],
          correct_answer: '晚上7点',
          image: img2
        },
        {
          id: 103,
          question: '如果今天是1月1日，那么超市今天营业多少小时呢？',
          options: ['8小时', '14小时', '10小时', '15小时'],
          correct_answer: '14小时',
          image: img3
        },
        {
          id: 104,
          question: '吉林卫视春晚是几点播出呢？',
          options: ['晚上9点半', '晚上7点半', '晚上6点18分', '上午10点半'],
          correct_answer: '晚上7点半',
          image: img4
        }
      ]
    },
    checkAnsweredQuestions() {
      const saved = localStorage.getItem(`answers_practice_${this.studentId}`)
      if (saved) {
        const parsed = JSON.parse(saved)
        this.answeredQuestions = parsed.answeredQuestions || {}
        this.answers = parsed.answers || {}
      }
    },
    async answerQuestion(question, answer) {
      if (this.answeredQuestions[question.id]) return
      
      const isCorrect = answer === question.correct_answer
      
      try {
        // 提交答案到后端
        await this.$http.post(`/student/${this.studentId}/answers`, {
          question_id: question.id,
          answer: answer,
          is_correct: isCorrect,
          module_type: 'practice'
        })
        
        this.answeredQuestions[question.id] = true
        this.answeredQuestions = { ...this.answeredQuestions } // 触发响应式更新
        
        this.answers[question.id] = {
          isCorrect: isCorrect,
          answer: answer
        }
        
        // 同时保存到本地存储，用于离线查看
        localStorage.setItem(`answers_practice_${this.studentId}`, JSON.stringify({
          answeredQuestions: this.answeredQuestions,
          answers: this.answers
        }))
        
        if (isCorrect) {
          this.$message.success('答对了！')
        } else {
          this.$message.error(`答错了，正确答案是：${question.correct_answer}`)
        }
      } catch (error) {
        console.error('提交答案失败:', error)
        // 即使API调用失败，也保存到本地，以便离线使用
        this.answeredQuestions[question.id] = true
        this.answeredQuestions = { ...this.answeredQuestions }
        this.answers[question.id] = {
          isCorrect: isCorrect,
          answer: answer
        }
        localStorage.setItem(`answers_practice_${this.studentId}`, JSON.stringify({
          answeredQuestions: this.answeredQuestions,
          answers: this.answers
        }))
        this.$message.warning('提交答案失败，已保存到本地')
      }
    },
    goBack() {
      this.$router.push('/')
    },
    startQuiz() {
      this.quizStarted = true;
      this.currentQuestionIndex = 0;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++;
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
    },
    finishQuiz() {
      this.$message.success('恭喜你完成了所有练习！');
      // 可选：这里可以重置或跳转，但用户要求不要弹窗。
      // 我们就停留在最后一道题的状态，或者显示一个简单的完成状态。
    }
  }
}
</script>

<style scoped>
.life-application-page {
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

.main-content.mode-quiz {
  display: flex;
  gap: 20px;
  align-items: stretch;
}

.rules-section {
  transition: all 0.5s ease;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.main-content.mode-quiz .rules-section {
  width: 320px;
  flex-shrink: 0;
}

.quiz-section {
  flex: 1;
  min-width: 0; /* 防止flex子项溢出 */
  animation: fadeIn 0.5s ease;
  display: flex;
  flex-direction: column;
}

.section-card {
  max-width: 1200px;
  margin: 0 auto 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  height: 100%;
}

/* .rules-card and .quiz-card placeholders removed */

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

/* 新布局样式 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  transition: all 0.5s ease;
  /* 尝试整体向左微调，通过减少左侧边距或设置相对定位 */
  transform: translateX(-20px); 
}


@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 规则卡片在侧边栏模式下的样式调整 */
.main-content.mode-quiz .rules-card {
  padding: 15px;
}

.main-content.mode-quiz .section-title {
  font-size: 20px;
  margin-bottom: 10px;
}

.main-content.mode-quiz .conversion-rules {
  margin-top: 10px;
  border-left-width: 3px;
}

.main-content.mode-quiz .rules-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.main-content.mode-quiz .rules-content {
  gap: 12px;
}

.main-content.mode-quiz .rule-item {
  padding: 12px;
}

.main-content.mode-quiz .rule-header {
  margin-bottom: 5px;
}

.main-content.mode-quiz .rule-header i {
  font-size: 18px;
}

.main-content.mode-quiz .rule-title {
  font-size: 16px;
}

.main-content.mode-quiz .rule-desc {
  font-size: 14px;
}

/* 开始按钮 */
.start-action {
  text-align: center;
  padding: 40px 0;
  border-top: 1px solid #eee;
  margin-top: 20px;
}

.start-btn {
  font-size: 20px;
  padding: 15px 40px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

/* 答题区样式 */
.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.quiz-progress {
  font-size: 16px;
  color: #667eea;
  font-weight: bold;
}

.active-question {
  border: none;
  padding: 0;
  background: transparent;
}

.navigation-btns {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.conversion-rules {
  margin-top: 30px;
  background: #f0f7ff;
  border-left: 4px solid #667eea;
}

.rules-title {
  font-size: 22px;
  color: #667eea;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
}

.rules-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.rule-item {
  padding: 20px;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.rule-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.rule-header i {
  font-size: 24px;
  color: #667eea;
}

.rule-title {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
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
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 4px;
}

/* questions-container removed empty rule */

/* question-card removed empty rule */

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

.question-content {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.question-image-container {
  flex: 0 0 45%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-image {
  width: 100%;
  height: auto;
  display: block;
}

.question-main {
  flex: 1;
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
  width: 100%;
}

.options-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex; /* Change from block to flex for better internal alignment */
  margin-bottom: 0; /* Handled by gap in parent */
  margin-right: 0 !important; /* Override Element UI default */
  margin-left: 0 !important; /* Override Element UI default for + label */
  font-size: 16px;
  padding: 12px 16px;
  border-radius: 8px;
  background: white;
  border: 2px solid #e4e7ed;
  transition: all 0.3s;
  width: 100%;
  box-sizing: border-box;
  white-space: normal;
  height: auto;
}

::v-deep .el-radio.option-item {
  /* Redundant if option-item selector works, but kept for specificity */
  display: flex;
  align-items: center;
  height: auto;
  margin-right: 0;
  width: 100%;
  padding: 12px 16px; /* Ensure padding is here if Element UI overrides it */
}

::v-deep .el-radio__input {
  flex-shrink: 0; /* 防止单选框图标被压缩 */
}

::v-deep .el-radio__label {
  display: inline-block;
  word-break: break-word;
  white-space: normal;
  line-height: 1.4;
  width: 100%; /* 让文字区域占满剩余空间 */
  text-align: left; /* 确保文字左对齐 */
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

@media (max-width: 992px) {
  .main-content.mode-quiz {
    flex-direction: column;
  }
  
  .main-content.mode-quiz .rules-section {
    width: 100%;
  }
  
  .main-content.mode-quiz .rules-content {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .main-content.mode-quiz .rule-item {
    flex: 1 1 300px;
  }
}

@media (max-width: 768px) {
  .question-content {
    flex-direction: column;
  }
  
  .question-image-container {
    flex: none;
    width: 100%;
    max-width: 100%;
  }
}
</style>