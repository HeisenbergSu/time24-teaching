<template>
  <div class="explore-module">
    <h2 class="module-title">课前探索</h2>
    
    <!-- 旧知复习 -->
    <div class="section">
      <h3>旧知复习</h3>
      <p class="section-desc">让我们先复习一下上学期学过的时间知识吧！</p>
      
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

    <!-- 情景导入 -->
    <div class="section">
      <h3>情景导入</h3>
      <p class="section-desc">让我们一起来观看时间流转的动画，看看钟表一天会转几圈呢？</p>
      
      <div class="video-container">
        <div class="animation-area">
          <ClockAnimation :play="animationPlaying" @complete="onAnimationComplete"/>
          <div class="controls">
            <el-button 
              type="primary" 
              @click="toggleAnimation"
              :icon="animationPlaying ? 'el-icon-video-pause' : 'el-icon-video-play'"
            >
              {{ animationPlaying ? '暂停' : '播放' }}
            </el-button>
            <el-button @click="resetAnimation">重置</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ClockAnimation from './ClockAnimation.vue'

export default {
  name: 'ExploreModule',
  components: {
    ClockAnimation
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
      answers: {},
      animationPlaying: false
    }
  },
  mounted() {
    this.loadQuestions()
  },
  methods: {
    async loadQuestions() {
      try {
        const res = await this.$http.get('/questions/explore')
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
          module_type: 'explore'
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
    toggleAnimation() {
      this.animationPlaying = !this.animationPlaying
    },
    resetAnimation() {
      this.animationPlaying = false
      this.$nextTick(() => {
        this.animationPlaying = true
      })
    },
    onAnimationComplete() {
      this.animationPlaying = false
      this.$message.success('动画播放完成！钟表一天转了两圈，你发现了吗？')
    }
  }
}
</script>

<style scoped>
.explore-module {
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

.video-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.animation-area {
  width: 100%;
  max-width: 600px;
}

.controls {
  margin-top: 20px;
  text-align: center;
}

.controls .el-button {
  margin: 0 10px;
}
</style>

