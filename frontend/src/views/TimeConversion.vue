<template>
  <div class="time-conversion-page">
    <div class="page-header">
      <el-button 
        @click="goBack" 
        icon="el-icon-arrow-left" 
        circle
        class="back-button"
      ></el-button>
      <h1 class="page-title">时间转换学习</h1>
    </div>

    <!-- 12时计时法与24时计时法对比 -->
    <el-card class="section-card">
      <h2 class="section-title">⏰ 12时计时法与24时计时法对比</h2>
      <p class="section-desc">
        在生活中，我们有两种表示时间的方法：12时计时法（上午8时、晚上8时）和24时计时法（08:00、20:00）。
        让我们来学习它们的转换关系吧！
      </p>
      
      <!-- 对比展示 -->
      <div class="comparison-section">
        <div class="comparison-cards">
          <!-- 早上8点 -->
          <el-card class="comparison-card morning-card" shadow="hover">
            <div class="card-header">
              <i class="el-icon-sunny morning-icon"></i>
              <h3>早上8点</h3>
            </div>
            <div class="time-display-row">
              <div class="time-item">
                <div class="time-label">12时计时法</div>
                <div class="time-value">上午8时</div>
              </div>
              <div class="arrow">→</div>
              <div class="time-item">
                <div class="time-label">24时计时法</div>
                <div class="time-value time-24-value">08:00</div>
              </div>
            </div>
            <div class="conversion-rule">
              <i class="el-icon-info"></i>
              <span>规则：上午时间，两种计时法相同（0:00-12:00）</span>
            </div>
          </el-card>
          
          <!-- 晚上8点 -->
          <el-card class="comparison-card evening-card" shadow="hover">
            <div class="card-header">
              <i class="el-icon-moon evening-icon"></i>
              <h3>晚上8点</h3>
            </div>
            <div class="time-display-row">
              <div class="time-item">
                <div class="time-label">12时计时法</div>
                <div class="time-value">晚上8时</div>
              </div>
              <div class="arrow">→</div>
              <div class="time-item">
                <div class="time-label">24时计时法</div>
                <div class="time-value time-24-value">20:00</div>
              </div>
            </div>
            <div class="conversion-rule highlight">
              <i class="el-icon-star-on"></i>
              <span>规则：晚上时间，24时 = 12时 + 12（8 + 12 = 20）</span>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 转换公式卡片 -->
      <el-card class="formula-card" shadow="always">
        <div class="formula-content">
          <h3 class="formula-title">📐 转换公式</h3>
          <div class="formula-grid">
            <div class="formula-item">
              <div class="formula-label">12时 → 24时（下午/晚上）</div>
              <div class="formula-expression">
                <span class="formula-highlight">24时 = 12时 + 12</span>
              </div>
              <div class="formula-example">
                例：晚上8时 → 8 + 12 = 20:00
              </div>
            </div>
            <div class="formula-item">
              <div class="formula-label">24时 → 12时（下午/晚上）</div>
              <div class="formula-expression">
                <span class="formula-highlight">12时 = 24时 - 12</span>
              </div>
              <div class="formula-example">
                例：20:00 → 20 - 12 = 晚上8时
              </div>
            </div>
            <div class="formula-item">
              <div class="formula-label">12时 → 24时（上午/中午）</div>
              <div class="formula-expression">
                <span class="formula-highlight">24时 = 12时（相同）</span>
              </div>
              <div class="formula-example">
                例：上午8时 → 08:00（相同）
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </el-card>
    
    <!-- 时间尺 - 化曲为直 -->
    <el-card class="section-card">
      <h2 class="section-title">📏 时间尺 - 把钟面化曲为直</h2>
      <p class="section-desc">
        让我们把圆形的钟面展开成一条直线的时间尺，观察12时和24时计时法的对应关系。
      </p>
      
      <div class="interaction-container">
        <!-- 左侧：钟面或时间尺 -->
        <div class="display-wrapper">
          <!-- 展开/收起按钮 - 移到面板外部上方 -->
          <div class="panel-header">
            <div class="panel-title">{{ showExpanded ? '📏 展开的时间尺' : '⏰ 钟面视图' }}</div>
            <el-button 
              @click="showExpandAnimation" 
              type="primary" 
              size="small"
              round
              :icon="showExpanded ? 'el-icon-refresh-left' : 'el-icon-full-screen'"
            >
              {{ showExpanded ? '返回钟面' : '展开为时间尺' }}
            </el-button>
          </div>

          <div class="display-panel" :class="{ 'is-expanded': showExpanded }">
            <!-- 钟面显示 (收起状态) -->
            <div v-if="!showExpanded" class="clock-view">
              <div class="clock-circle">
                <div 
                  v-for="i in 12" 
                  :key="i"
                  class="clock-hour-mark"
                  :style="getClockMarkStyle(i)"
                >
                  {{ i }}
                </div>
                <div class="clock-center">
                  <!-- 时针 -->
                  <div class="clock-hand hour-hand" :style="{ transform: `rotate(${getHourRotation}deg)` }"></div>
                  <!-- 分针 -->
                  <div class="clock-hand minute-hand" :style="{ transform: `rotate(${getMinuteRotation}deg)` }"></div>
                  <div class="center-dot"></div>
                </div>
              </div>
              <div class="clock-label">
                {{ formatTimeDisplay }}
              </div>
            </div>

            <!-- 时间尺显示 (展开状态) -->
            <div v-else class="ruler-view">
              <TimeScaleExpanded 
                :selected-hour="selectedHour"
                :conversion-direction="conversionDirection"
                @hour-select="handleHourSelect"
              />
            </div>
          </div>
        </div>

        <!-- 右侧：控制面板 -->
        <div class="control-panel">
          <el-card class="control-card" shadow="hover">
            <div slot="header" class="clearfix">
              <span class="control-title">⏱️ 转换练习设置</span>
            </div>
            
            <div class="control-item">
              <div class="label">选择转换方向：</div>
              <el-radio-group v-model="conversionDirection" size="small">
                <el-radio-button label="12to24">12时 转 24时</el-radio-button>
                <el-radio-button label="24to12">24时 转 12时</el-radio-button>
              </el-radio-group>
            </div>

            <div class="control-item">
              <div class="label">选择时间：</div>
              <div class="time-selector">
                <el-slider
                  v-model="selectedHour"
                  :min="0"
                  :max="23"
                  :step="1"
                  show-stops
                  :marks="sliderMarks"
                  @input="handleTimeChange"
                >
                </el-slider>
              </div>
              <div class="current-time-display">
                当前选择：<span class="highlight">{{ formatTimeDisplay }}</span>
              </div>
            </div>

            <div class="instruction-text">
              <i class="el-icon-info"></i>
              <span v-if="conversionDirection === '12to24'">
                观察左侧{{ showExpanded ? '时间尺' : '钟面' }}，看12时计时法如何对应到24时计时法。
              </span>
              <span v-else>
                观察左侧{{ showExpanded ? '时间尺' : '钟面' }}，看24时计时法如何对应到12时计时法。
              </span>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 快速转换练习 -->
      <div class="quick-practice">
        <h3 class="practice-title">⚡ 快速转换练习</h3>
        <div class="practice-grid">
          <div 
            v-for="practice in practiceItems" 
            :key="practice.id"
            class="practice-item"
            :class="{ active: practice.active }"
            @click="selectPractice(practice)"
          >
            <div class="practice-question">
              <span class="practice-label">{{ practice.label }}</span>
              <span class="practice-value">{{ practice.value }}</span>
            </div>
            <div class="practice-answer">
              <i class="el-icon-arrow-right"></i>
              <span class="answer-text">{{ practice.answer }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import TimeScaleExpanded from '../components/TimeScaleExpanded.vue'

export default {
  name: 'TimeConversion',
  components: {
    TimeScaleExpanded
  },
  data() {
    return {
      showExpanded: false,
      selectedHour: 8,
      conversionDirection: '12to24',
      sliderMarks: {
        0: '0',
        6: '6',
        12: '12',
        18: '18',
        23: '23'
      },
      practiceItems: [
        { id: 1, label: '上午9时', value: '上午9时', answer: '09:00', active: false, hour: 9 },
        { id: 2, label: '晚上9时', value: '晚上9时', answer: '21:00', active: false, hour: 21 },
        { id: 3, label: '15:00', value: '15:00', answer: '下午3时', active: false, hour: 15 },
        { id: 4, label: '22:00', value: '22:00', answer: '晚上10时', active: false, hour: 22 },
        { id: 5, label: '中午12时', value: '中午12时', answer: '12:00', active: false, hour: 12 },
        { id: 6, label: '00:00', value: '00:00', answer: '凌晨0时', active: false, hour: 0 }
      ]
    }
  },
  computed: {
    getHourRotation() {
      return (this.selectedHour % 12) * 30
    },
    getMinuteRotation() {
      return 0
    },
    formatTimeDisplay() {
      const h = this.selectedHour
      if (this.conversionDirection === '24to12') {
        // 展示24时
        return `${String(h).padStart(2, '0')}:00`
      } else {
        // 展示12时
        if (h === 0) return '凌晨0时'
        if (h < 6) return `凌晨${h}时`
        if (h < 12) return `上午${h}时`
        if (h === 12) return '中午12时'
        if (h < 18) return `下午${h-12}时`
        return `晚上${h-12}时`
      }
    }
  },
  methods: {
    showExpandAnimation() {
      this.showExpanded = !this.showExpanded
    },
    handleHourSelect(hour) {
      this.selectedHour = hour
    },
    handleTimeChange(val) {
      this.selectedHour = val
    },
    selectHour(hour) {
      this.selectedHour = hour
    },
    selectPractice(practice) {
      // 更新选中的时间
      this.selectedHour = practice.hour;
      
      // 滚动到钟面视图
      const clockSection = this.$el.querySelector('.interaction-container');
      if (clockSection) {
        clockSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      // 高亮显示选中的练习项
      this.practiceItems.forEach(item => {
        item.active = item.id === practice.id
      })
      
      // 2秒后取消高亮
      setTimeout(() => {
        practice.active = false
      }, 2000)
    },
    getClockMarkStyle(num) {
      const angle = (num) * 30
      const radius = 115 // 缩小半径，让数字在圆圈内 (原140 -> 115)
      const x = Math.sin(angle * Math.PI / 180) * radius
      const y = -Math.cos(angle * Math.PI / 180) * radius
      return {
        transform: `translate(${x}px, ${y}px)`
      }
    },
    goBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.time-conversion-page {
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
  line-height: 1.8;
}

/* 对比卡片 */
.comparison-section {
  margin: 40px 0;
}

.comparison-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.comparison-card {
  padding: 30px;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.morning-card {
  background: linear-gradient(135deg, #fff9e6 0%, #ffe0b2 100%);
  border: 2px solid #ffd54f;
}

.evening-card {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border: 2px solid #2196f3;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.card-header h3 {
  font-size: 24px;
  margin: 0;
  color: #333;
}

.morning-icon {
  font-size: 36px;
  color: #ff9800;
}

.evening-icon {
  font-size: 36px;
  color: #2196f3;
}

.time-display-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.time-item {
  flex: 1;
  text-align: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
}

.time-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.time-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.time-24-value {
  color: #667eea;
  font-family: 'Courier New', monospace;
}

.arrow {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
}

.conversion-rule {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  font-size: 16px;
  color: #333;
}

.conversion-rule.highlight {
  background: rgba(102, 126, 234, 0.1);
  border: 2px solid #667eea;
  color: #667eea;
  font-weight: bold;
}

.conversion-rule i {
  font-size: 20px;
}

/* 公式卡片 */
.formula-card {
  margin-top: 40px;
  background: linear-gradient(135deg, #f0f7ff 0%, #e8f5e9 100%);
  border: 2px solid #667eea;
}

.formula-content {
  padding: 20px;
}

.formula-title {
  font-size: 24px;
  color: #667eea;
  margin-bottom: 25px;
  text-align: center;
}

.formula-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
}

.formula-item {
  padding: 20px;
  background: white;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.formula-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.formula-expression {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
}

.formula-highlight {
  color: #667eea;
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  display: inline-block;
}

.formula-example {
  font-size: 14px;
  color: #666;
  font-style: italic;
}

/* 交互区域布局 */
.interaction-container {
  display: flex;
  gap: 30px;
  margin: 30px 0;
  min-height: 450px;
}

.display-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.5s ease;
  min-width: 0; /* 关键：防止flex子项被内容撑大，确保内部滚动生效 */
}

.display-wrapper:has(.is-expanded) {
  flex: 2;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0 10px;
}

.panel-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.display-panel {
  flex: 1;
  background: #fafafa;
  border-radius: 12px;
  position: relative;
  transition: all 0.5s ease;
  display: flex;
  flex-direction: column;
  padding: 20px;
  min-height: 400px;
  border: 1px solid #e4e7ed;
  overflow: hidden; /* 确保内容不会溢出面板 */
}

/* 钟面视图 */
.clock-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.clock-circle {
  position: relative;
  width: 280px;
  height: 280px;
  border: 8px solid #333;
  border-radius: 50%;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

.clock-hour-mark {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 30px;
  height: 30px;
  margin: -15px 0 0 -15px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clock-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 16px;
  height: 16px;
  background: #333;
  border-radius: 50%;
  z-index: 10;
}

.clock-hand {
  position: absolute;
  bottom: 50%;
  left: 50%;
  transform-origin: center bottom;
  background: #333;
  border-radius: 4px;
  transition: transform 0.3s cubic-bezier(0.4, 2.08, 0.55, 0.44);
}

.hour-hand {
  width: 6px;
  height: 70px;
  margin-left: -3px;
  z-index: 5;
}

.minute-hand {
  width: 4px;
  height: 100px;
  margin-left: -2px;
  background: #666;
  z-index: 4;
}

.clock-label {
  font-size: 24px;
  font-weight: bold;
  color: #667eea;
  margin-top: 10px;
}

/* 时间尺视图 */
.ruler-view {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  padding-top: 40px; /* 留出按钮空间 */
}

/* 右侧控制面板 */
.control-panel {
  width: 320px;
  flex-shrink: 0;
}

.control-card {
  height: 100%;
  border-radius: 12px;
}

.control-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.control-item {
  margin-bottom: 25px;
}

.label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.time-selector {
  padding: 0 10px;
}

.current-time-display {
  margin-top: 15px;
  text-align: center;
  font-size: 16px;
  color: #666;
}

.highlight {
  font-weight: bold;
  color: #667eea;
  font-size: 20px;
  margin-left: 5px;
}

.instruction-text {
  display: flex;
  gap: 10px;
  background: #f0f9ff;
  padding: 15px;
  border-radius: 8px;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.instruction-text i {
  color: #409EFF;
  font-size: 16px;
  margin-top: 2px;
}

@media (max-width: 900px) {
  .interaction-container {
    flex-direction: column;
  }
  
  .control-panel {
    width: 100%;
  }
}

/* 快速练习 */
.quick-practice {
  margin-top: 40px;
  padding: 30px;
  background: #fafafa;
  border-radius: 12px;
}

.practice-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 25px;
  text-align: center;
}

.practice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.practice-item {
  padding: 20px;
  background: white;
  border-radius: 12px;
  border: 2px solid #e4e7ed;
  cursor: pointer;
  transition: all 0.3s ease;
}

.practice-item:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  transform: translateY(-4px);
}

.practice-item.active {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e8f5e9 100%);
  box-shadow: 0 6px 16px rgba(103, 194, 58, 0.3);
}

.practice-question {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.practice-label {
  font-size: 14px;
  color: #666;
}

.practice-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.practice-answer {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-top: 15px;
  border-top: 1px solid #e4e7ed;
}

.practice-answer i {
  color: #667eea;
  font-size: 18px;
}

.answer-text {
  font-size: 20px;
  font-weight: bold;
  color: #667eea;
  font-family: 'Courier New', monospace;
}

@media (max-width: 768px) {
  .comparison-cards {
    grid-template-columns: 1fr;
  }

  .formula-grid {
    grid-template-columns: 1fr;
  }

  .practice-grid {
    grid-template-columns: 1fr;
  }
}
</style>

