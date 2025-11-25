<template>
  <div class="new-learning-page">
    <div class="page-header">
      <el-button 
        @click="goBack" 
        icon="el-icon-arrow-left" 
        circle
        class="back-button"
      ></el-button>
      <h1 class="page-title">新知学习</h1>
    </div>

    <!-- 钟表一天转两圈 -->
    <el-card class="section-card">
      <h2 class="section-title">🕐 钟表一天转两圈</h2>
      <p class="section-desc">
        同学们，你们知道吗？钟表的时针在一天中会转两圈！让我们通过下面的互动来感受一下时间的流转吧。
        你可以看到地球围绕太阳/月亮的变化，同时钟表也在转动。注意观察时针转了多少圈哦！
      </p>
      
      <div class="content-layout">
        <div class="interactive-clock">
          <!-- 传递 show-second-hand=false 属性隐藏秒针 -->
          <ClockAnimation :play="false" :show-second-hand="false"/>
        </div>
        
        <div class="learning-panel">
          <el-card class="learning-points" shadow="never">
            <div class="points-header">
              <i class="el-icon-aim"></i>
              <h3>学习要点</h3>
            </div>
            <ul class="points-list">
              <li>钟表的指针一天转了几圈？</li>
              <li>一天一共是多少小时？</li>
              <li>一天从什么时间开始？从什么时间结束？</li>
            </ul>
          </el-card>
        </div>
      </div>
    </el-card>
    
    <!-- 时间与天色 -->
    <el-card class="section-card">
      <h2 class="section-title">🌅 时间与天色</h2>
      <p class="section-desc">
        通过观察，我们可以发现：同样的钟表时间，在不同的时段（上午/下午），天色是不同的。
        早上8点时，天亮了；晚上8点时，天黑了。但钟表上时针的位置是一样的！
      </p>
      
      <div class="time-comparison">
        <div class="comparison-item">
          <h4>早上8点</h4>
          <div class="time-demo morning">
            <div class="sun-demo"></div>
            <div class="clock-demo">
              <span>08:00</span>
              <p>上午8时</p>
            </div>
          </div>
        </div>
        
        <div class="vs-divider">VS</div>
        
        <div class="comparison-item">
          <h4>晚上8点</h4>
          <div class="time-demo evening">
            <div class="moon-demo"></div>
            <div class="clock-demo">
              <span>20:00</span>
              <p>晚上8时</p>
            </div>
          </div>
        </div>
      </div>
      
      <el-alert
        title="发现了吗？"
        type="success"
        :closable="false"
        show-icon
      >
        <p>早上8点和晚上8点，时针都指向8，但是一个是白天（08:00），一个是晚上（20:00）！</p>
      </el-alert>
    </el-card>
    
    <!-- 时间转换学习入口 -->
    <el-card class="section-card conversion-entry">
      <h2 class="section-title">⏰ 12时计时法与24时计时法转换</h2>
      <p class="section-desc">
        想学习如何把早上8时转换为08:00，把晚上8时转换为20:00吗？
        让我们来看看时间尺是如何把钟面"化曲为直"的！
      </p>
      <div class="entry-button">
        <el-button 
          type="primary" 
          size="large" 
          icon="el-icon-arrow-right"
          @click="goToTimeConversion"
        >
          学习时间转换
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import ClockAnimation from '../components/ClockAnimation.vue'

export default {
  name: 'NewLearning',
  components: {
    ClockAnimation
  },
  methods: {
    goBack() {
      this.$router.push('/')
    },
    goToTimeConversion() {
      this.$router.push('/time-conversion')
    }
  }
}
</script>

<style scoped>
.new-learning-page {
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

.content-layout {
  display: flex;
  gap: 30px;
  margin: 40px 0;
}

.interactive-clock {
  flex: 2;
  display: flex;
  justify-content: center;
  padding: 30px;
  background: #fafafa;
  border-radius: 12px;
  min-width: 0; /* 防止flex子项溢出 */
}

.learning-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.learning-points {
  margin-top: 0; /* 重置之前的margin */
  height: 100%;
  background: #f0f7ff;
  border-left: 4px solid #667eea;
}

/* 移动端适配调整 */
@media (max-width: 992px) {
  .content-layout {
    flex-direction: column;
  }
  
  .learning-panel {
    width: 100%;
  }
}

.points-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.points-header i {
  font-size: 28px;
  color: #667eea;
}

.points-header h3 {
  font-size: 22px;
  color: #667eea;
  margin: 0;
}

.points-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.points-list li {
  padding: 12px 0;
  padding-left: 28px;
  position: relative;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
}

.points-list li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #67c23a;
  font-weight: bold;
  font-size: 18px;
}

.time-comparison {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  margin: 30px 0;
  flex-wrap: wrap;
}

.comparison-item {
  flex: 1;
  min-width: 250px;
  max-width: 350px;
}

.comparison-item h4 {
  text-align: center;
  font-size: 22px;
  color: #333;
  margin-bottom: 20px;
  font-weight: bold;
}

.time-demo {
  position: relative;
  width: 100%;
  height: 280px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.time-demo.morning {
  background: linear-gradient(180deg, #87ceeb 0%, #98d8e8 100%);
}

.time-demo.evening {
  background: linear-gradient(180deg, #191970 0%, #000033 100%);
}

.sun-demo {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 70px;
  height: 70px;
  background: radial-gradient(circle, #ffd700 0%, #ff8c00 100%);
  border-radius: 50%;
  box-shadow: 0 0 30px #ffd700;
  animation: pulse 2s infinite;
}

.moon-demo {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background: #e0e0e0;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.clock-demo {
  text-align: center;
  z-index: 10;
}

.clock-demo span {
  font-size: 52px;
  font-weight: bold;
  color: white;
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.5);
  display: block;
  margin-bottom: 12px;
  font-family: 'Courier New', monospace;
}

.clock-demo p {
  font-size: 26px;
  color: white;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
  margin: 0;
}

.vs-divider {
  font-size: 36px;
  font-weight: bold;
  color: #667eea;
  padding: 0 20px;
}

/* 转换入口卡片 */
.conversion-entry {
  background: linear-gradient(135deg, #f0f7ff 0%, #e8f5e9 100%);
  border: 2px solid #667eea;
}

.entry-button {
  text-align: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .time-comparison {
    flex-direction: column;
  }

  .vs-divider {
    transform: rotate(90deg);
    padding: 20px 0;
  }
}
</style>

