<template>
  <div class="pre-explore-page">
    <div class="page-header">
      <el-button 
        @click="goBack" 
        icon="el-icon-arrow-left" 
        circle
        class="back-button"
      ></el-button>
      <h1 class="page-title">课前探索</h1>
    </div>

    <!-- 旧知复习 -->
    <el-card class="section-card" v-if="!showScenarioIntro">
      <h2 class="section-title">📚 旧知复习</h2>
      <p class="section-desc">让我们先复习一下上学期学过的时间知识吧！</p>
      
      <div v-if="questions.length > 0" class="questions-container">
        <div class="progress-info">
          <span>进度: {{ answeredCount }} / {{ questions.length }}</span>
          <el-progress 
            :percentage="Math.round((answeredCount / questions.length) * 100)" 
            :stroke-width="8"
            color="#67c23a"
          ></el-progress>
        </div>

        <div 
          v-for="(question, index) in questions" 
          :key="question.id"
          class="question-card"
          :class="{ active: currentQuestionIndex === index }"
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
          
          <el-radio-group 
            v-model="userAnswers[question.id]" 
            @change="answerQuestion(question, $event)"
            :disabled="answeredQuestions[question.id]"
            class="options-group"
          >
            <el-radio 
              v-for="(option, optIndex) in question.options" 
              :key="optIndex" 
              :label="option"
              class="option-item"
            >
              <span class="option-text">{{ option }}</span>
            </el-radio>
          </el-radio-group>
          
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

        <div class="navigation-buttons">
          <el-button 
            @click="prevQuestion" 
            :disabled="currentQuestionIndex === 0"
            icon="el-icon-arrow-left"
          >
            上一题
          </el-button>
          <span class="question-indicator">
            {{ currentQuestionIndex + 1 }} / {{ questions.length }}
          </span>
          <el-button 
            @click="nextQuestion" 
            :disabled="currentQuestionIndex === questions.length - 1"
          >
            下一题
            <i class="el-icon-arrow-right"></i>
          </el-button>
        </div>
        
        <!-- 完成弹窗 - 当所有题目都回答后弹出 -->
        <el-dialog
          :visible.sync="showCompleteDialog"
          :modal="true"
          :close-on-click-modal="false"
          :close-on-press-escape="false"
          :show-close="false"
          width="500px"
          class="complete-dialog"
          center
        >
          <div class="complete-content">
            <div class="complete-icon">🎉</div>
            <div class="complete-text">
              <h3>恭喜完成旧知复习！</h3>
              <p>你已经回答了所有 {{ questions.length }} 道题目</p>
              <p class="score-info">正确: {{ correctCount }} 题 | 错误: {{ wrongCount }} 题</p>
            </div>
            <el-button 
              type="success" 
              size="large" 
              @click="enterScenarioIntro"
              icon="el-icon-right"
            >
              进入情景导入
            </el-button>
          </div>
        </el-dialog>
      </div>
      
      <div v-else class="loading">
        <i class="el-icon-loading"></i>
        <p>加载题目中...</p>
      </div>
    </el-card>

    <!-- 情景导入 - 只有当用户点击"进入情景导入"按钮后才显示 -->
    <div v-if="showScenarioIntro" class="section-video">
      <el-card class="section-card">
        <h2 class="section-title">🎬 情景导入</h2>
        <p class="section-desc">回答得真棒！让我们一起来看一个有趣的视频，了解一下今天的主题吧。</p>
        
        <div class="video-placeholder-container">
          <!-- 视频播放器占位 -->
          <div class="video-wrapper">
            <video 
              ref="introVideo"
              controls 
              width="100%" 
              height="100%"
              class="intro-video"
            >
              <source src="@/images/pre.mp4" type="video/mp4">
              您的浏览器不支持视频播放。
            </video>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
// import ClockAnimation from '../components/ClockAnimation.vue' // 移除旧的动画组件引用

export default {
  name: 'PreExplore',
  components: {
    // ClockAnimation
  },
  data() {
    return {
      studentId: null,
      questions: [],
      userAnswers: {},
      answeredQuestions: {},
      answers: {},
      currentQuestionIndex: 0,
      answeredCount: 0, // 已回答的题目数（不管对错）
      showScenarioIntro: false, // 是否显示情景导入
      isInitialLoad: true, // 标记是否为首次加载页面
      showCompleteDialog: false // 是否显示完成弹窗
    }
  },
  computed: {
    // 检查是否所有题目都已回答（不管对错）
    allQuestionsAnswered() {
      return this.questions.length > 0 && this.answeredCount === this.questions.length
    },
    // 正确题数
    correctCount() {
      return Object.values(this.answers).filter(a => a && a.isCorrect).length
    },
    // 错误题数
    wrongCount() {
      return this.answeredCount - this.correctCount
    }
  },
  watch: {
    // 监听是否所有题目都已答完
    allQuestionsAnswered(newVal, oldVal) {
      // 只有当从 false 变为 true 时才弹出弹窗（用户新答完所有题目）
      // 避免在页面首次加载时已经全部答完就弹出
      if (newVal && oldVal === false && !this.isInitialLoad) {
        // 延迟一点时间弹出，让最后一题的反馈显示完
        setTimeout(() => {
          this.showCompleteDialog = true
        }, 500)
      }
    }
  },
  mounted() {
    const savedStudentId = localStorage.getItem('studentId')
    if (savedStudentId) {
      this.studentId = parseInt(savedStudentId)
    }
    this.loadQuestions()
  },
  methods: {
    async loadQuestions() {
      try {
        const res = await this.$http.get('/questions/explore')
        this.questions = res.data.questions || []
        // 检查已答题
        this.checkAnsweredQuestions()
        
        // 等待所有初始化完成后再标记首次加载完成
        this.$nextTick(() => {
          this.isInitialLoad = false
        })
      } catch (error) {
        this.$message.error('加载题目失败')
        // 即使出错也要标记首次加载完成
        this.isInitialLoad = false
      }
    },
    checkAnsweredQuestions() {
      // 从本地存储或API检查已答题
      const saved = localStorage.getItem(`answers_explore_${this.studentId}`)
      if (saved) {
        try {
          const parsed = JSON.parse(saved)
          this.answeredQuestions = parsed.answeredQuestions || {}
          this.answers = parsed.answers || {}
          this.userAnswers = parsed.userAnswers || {}
          // 统计已回答的题目数（不管对错）
          this.answeredCount = Object.keys(this.answeredQuestions).length
          
          // 检查是否已经点击过"进入情景导入"按钮
          // 只在首次加载页面时才自动恢复状态，确保刷新页面后能保持状态
          // 但不会在答题时自动跳转，用户需要手动点击按钮
          const savedShowScenarioIntro = localStorage.getItem(`show_scenario_intro_${this.studentId}`)
          if (savedShowScenarioIntro === 'true' && this.isInitialLoad) {
            // 等待 questions 加载完成后再判断
            this.$nextTick(() => {
              // 只有首次加载页面且所有题目都已答完时，才自动恢复情景导入状态
              // 这样刷新页面后不会回到完成卡片，而是直接显示情景导入
              if (this.allQuestionsAnswered) {
                this.showScenarioIntro = true
              }
            })
          }
        } catch (error) {
          console.error('恢复答题状态失败:', error)
        }
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
          module_type: 'explore'
        })
        
        // 使用 $set 确保响应式
        this.$set(this.answeredQuestions, question.id, true)
        this.$set(this.answers, question.id, {
          isCorrect: isCorrect,
          answer: answer
        })
        this.$set(this.userAnswers, question.id, answer)
        
        // 更新已回答题目数（不管对错）
        this.answeredCount = Object.keys(this.answeredQuestions).length
        
        // 保存到本地存储
        localStorage.setItem(`answers_explore_${this.studentId}`, JSON.stringify({
          answeredQuestions: this.answeredQuestions,
          answers: this.answers,
          userAnswers: this.userAnswers
        }))
        
        if (isCorrect) {
          this.$message.success('答对了！')
        } else {
          this.$message.error(`答错了，正确答案是：${question.correct_answer}`)
        }
      } catch (error) {
        this.$message.error('提交答案失败')
        console.error('提交答案失败:', error)
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) {
        this.currentQuestionIndex++
      }
    },
    // toggleAnimation() {
    //   this.animationPlaying = !this.animationPlaying
    // },
    // resetAnimation() {
    //   this.animationPlaying = false
    //   this.$nextTick(() => {
    //     this.animationPlaying = true
    //   })
    // },
    // onAnimationComplete() {
    //   this.animationPlaying = false
    //   this.$message.success('动画播放完成！钟表一天转了两圈，你发现了吗？')
    // },
    enterScenarioIntro() {
      // 只有当所有题目都答完时才允许进入情景导入
      if (this.allQuestionsAnswered) {
        // 关闭完成弹窗
        this.showCompleteDialog = false
        // 保存状态到 localStorage，用于下次恢复
        localStorage.setItem(`show_scenario_intro_${this.studentId}`, 'true')
        // 延迟一点时间显示情景导入，让弹窗关闭动画完成
        setTimeout(() => {
          this.showScenarioIntro = true
        }, 300)
      } else {
        this.$message.warning('请先完成所有题目')
      }
    },
    goBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.pre-explore-page {
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

.progress-info {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.progress-info span {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #333;
}

.questions-container {
  position: relative;
  min-height: 400px;
}

.question-card {
  display: none;
  padding: 30px;
  background: #fafafa;
  border-radius: 12px;
  margin-bottom: 20px;
}

.question-card.active {
  display: block;
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
  font-size: 20px;
  color: #333;
  margin-bottom: 25px;
  line-height: 1.6;
  font-weight: 500;
}

.options-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.option-item {
  display: block;
  width: 100%;
  padding: 15px 20px;
  border-radius: 8px;
  background: white;
  border: 2px solid #e4e7ed;
  transition: all 0.3s;
  font-size: 16px;
  margin-bottom: 0;
  box-sizing: border-box;
}

.option-item ::v-deep .el-radio {
  display: block;
  width: 100%;
  margin-right: 0;
}

.option-item ::v-deep .el-radio__input {
  float: left;
  margin-right: 10px;
}

.option-item ::v-deep .el-radio__label {
  width: calc(100% - 30px);
  display: block;
  padding-left: 0;
}

.option-item .option-text {
  display: block;
  width: 100%;
  word-wrap: break-word;
  word-break: break-all;
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

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #e4e7ed;
}

.question-indicator {
  font-size: 16px;
  color: #666;
  font-weight: bold;
}

.animation-container {
  padding: 30px;
  background: #fafafa;
  border-radius: 12px;
}

.animation-controls {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
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

/* 视频容器样式 */
.video-placeholder-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  aspect-ratio: 16/9;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.video-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.intro-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.placeholder-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #2c3e50;
  color: white;
  z-index: 10;
}

.placeholder-overlay i {
  font-size: 48px;
  margin-bottom: 15px;
  color: #667eea;
}

.placeholder-overlay p {
  font-size: 18px;
  margin-bottom: 5px;
}

.placeholder-overlay .sub-text {
  font-size: 14px;
  color: #999;
}

/* 完成弹窗样式 */
.complete-dialog ::v-deep .el-dialog {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.complete-dialog ::v-deep .el-dialog__header {
  display: none;
}

.complete-dialog ::v-deep .el-dialog__body {
  padding: 40px;
}

.complete-content {
  text-align: center;
  padding: 20px 0;
}

.complete-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 0.6s ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}

.complete-text {
  margin-bottom: 30px;
}

.complete-text h3 {
  font-size: 28px;
  color: #333;
  margin-bottom: 15px;
  font-weight: bold;
}

.complete-text p {
  font-size: 18px;
  color: #666;
  margin-bottom: 10px;
  line-height: 1.6;
}

.complete-text .score-info {
  font-size: 20px;
  color: #667eea;
  font-weight: bold;
  margin-top: 15px;
}
</style>

