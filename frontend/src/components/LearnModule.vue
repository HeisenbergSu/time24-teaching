<template>
  <div class="learn-module">
    <h2 class="module-title">新知学习</h2>
    
    <div class="section">
      <h3>钟表一天转两圈</h3>
      <p class="section-desc">
        同学们，你们知道吗？钟表的时针在一天中会转两圈！让我们通过下面的互动来感受一下时间的流转吧。
        你可以看到地球围绕太阳/月亮的变化，同时钟表也在转动。注意观察时针转了多少圈哦！
      </p>
      
      <!-- 互动时钟展示 -->
      <div class="interactive-clock">
        <ClockAnimation :play="false"/>
      </div>
      
      <div class="learning-points">
        <el-card class="point-card">
          <div class="point-icon">🎯</div>
          <h4>学习要点</h4>
          <ul>
            <li>钟表的指针一天转了几圈？</li>
            <li>一天一共是多少小时？</li>
            <li>一天从什么时间开始？从什么时间结束？</li>
        
          </ul>
        </el-card>
      </div>
    </div>
    
    <div class="section">
      <h3>时间与天色</h3>
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
        style="margin-top: 20px;"
      >
        <p>早上8点和晚上8点，时针都指向8，但是一个是白天（08:00），一个是晚上（20:00）！</p>
      </el-alert>
    </div>
  </div>
</template>

<script>
import ClockAnimation from './ClockAnimation.vue'

export default {
  name: 'LearnModule',
  components: {
    ClockAnimation
  },
  props: {
    studentId: {
      type: Number,
      required: true
    }
  }
}
</script>

<style scoped>
.learn-module {
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
  line-height: 1.8;
}

.interactive-clock {
  display: flex;
  justify-content: center;
  margin: 40px 0;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.learning-points {
  margin-top: 30px;
}

.point-card {
  text-align: center;
}

.point-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.point-card h4 {
  font-size: 20px;
  color: #667eea;
  margin-bottom: 15px;
}

.point-card ul {
  text-align: left;
  list-style: none;
  padding: 0;
}

.point-card li {
  padding: 10px;
  margin-bottom: 8px;
  background: #f0f0f0;
  border-radius: 5px;
  font-size: 16px;
  line-height: 1.6;
}

.point-card li:before {
  content: "✓ ";
  color: #67c23a;
  font-weight: bold;
  margin-right: 8px;
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
  font-size: 20px;
  color: #333;
  margin-bottom: 20px;
}

.time-demo {
  position: relative;
  width: 100%;
  height: 250px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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
  width: 60px;
  height: 60px;
  background: radial-gradient(circle, #ffd700 0%, #ff8c00 100%);
  border-radius: 50%;
  box-shadow: 0 0 20px #ffd700;
}

.moon-demo {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background: #e0e0e0;
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
}

.clock-demo {
  text-align: center;
  z-index: 10;
}

.clock-demo span {
  font-size: 48px;
  font-weight: bold;
  color: white;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  display: block;
  margin-bottom: 10px;
  font-family: 'Courier New', monospace;
}

.clock-demo p {
  font-size: 24px;
  color: white;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
}

.vs-divider {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  padding: 0 20px;
}
</style>

