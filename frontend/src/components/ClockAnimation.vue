<template>
  <div class="clock-animation">
    <!-- 视频背景容器 -->
    <div class="sky-container" style="background: none;">
      <video
        ref="bgVideo"
        class="bg-video"
        src="@/images/bg.mp4"
        muted
        loop
        playsinline
        :style="videoStyle"
      ></video>
      <!-- 太阳 - 东升西落 -->
      <div class="sun-orbit" :style="sunOrbitStyle">
        <div class="sun" :style="sunStyle">
          <div class="sun-rays"></div>
        </div>
      </div>
      
      <!-- 月亮 - 西升东落 -->
      <div class="moon-orbit" :style="moonOrbitStyle">
        <div class="moon" :style="moonStyle">
          <div class="moon-crater" v-for="i in 3" :key="i" :style="getCraterStyle(i)"></div>
        </div>
      </div>
      
      <!-- 星星 - 夜晚显示 -->
      <div v-if="showStars" class="stars">
        <div 
          v-for="i in 20" 
          :key="i" 
          class="star"
          :style="getStarStyle(i)"
        ></div>
      </div>
      
      <!-- 云朵装饰 -->
      <div class="clouds">
        <div class="cloud cloud-1" :style="cloud1Style"></div>
        <div class="cloud cloud-2" :style="cloud2Style"></div>
        <div class="cloud cloud-3" :style="cloud3Style"></div>
      </div>
      
      <!-- 钟表 -->
      <div class="earth-clock-container">
        <!-- 外围圆环 - 显示转圈进度 -->
        <div class="circle-ring-container">
          <svg class="circle-ring-svg" viewBox="0 0 360 360">
            <!-- 第一圈圆环 (0-12小时) - 红色 -->
            <circle
              class="circle-ring circle-ring-1"
              cx="180"
              cy="180"
              r="145"
              :style="circleRing1Style"
            ></circle>
            <!-- 第二圈圆环 (12-24小时) - 蓝色，在第一圈外侧 -->
            <circle
              class="circle-ring circle-ring-2"
              cx="180"
              cy="180"
              r="160"
              :style="circleRing2Style"
            ></circle>
          </svg>
        </div>
        <div class="clock-wrapper">
          <div class="clock-face" :style="clockFaceStyle">
            <!-- 钟表刻度线 -->
            <div 
              v-for="i in 60" 
              :key="`mark-${i}`"
              :class="['clock-mark', (i % 5 === 0) ? 'hour-mark' : 'minute-mark']"
              :style="getMarkStyle(i)"
            ></div>
            <!-- 钟表数字 -->
            <div 
              v-for="i in 12" 
              :key="`num-${i}`"
              class="clock-number"
              :style="getNumberStyle(i)"
            >
              {{ i }}
            </div>
            <!-- 时针 - 显示转了两圈 -->
            <div class="hour-hand" :style="hourHandStyle"></div>
            <!-- 分针 -->
            <div class="minute-hand" :style="minuteHandStyle"></div>
            <!-- 秒针 -->
            <div class="second-hand" :style="secondHandStyle" v-if="showSecondHand"></div>
            <!-- 中心点 -->
            <div class="center-dot"></div>
            <!-- 转圈标记 - 显示转了几圈 -->
            <div class="circle-indicator" v-if="circlesCompleted > 0">
              <span class="circle-text">已转 {{ circlesCompleted }} 圈</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 地平线 -->
      <div class="horizon" :style="horizonStyle"></div>
    </div>
    
    <!-- 时间显示和控制 -->
    <div class="time-display-panel">
      <div class="time-display">
        <div class="time-label">{{ currentTimeLabel }}</div>
        <div class="time-24">{{ currentTime24 }}</div>
      </div>
      
      <div class="time-control">
        <div class="control-row">
          <div class="speed-control">
            <span class="speed-label">倍速播放：</span>
            <el-radio-group v-model="playbackSpeed" size="mini" fill="#667eea">
              <el-radio-button :label="1">1x</el-radio-button>
              <el-radio-button :label="5">5x</el-radio-button>
              <el-radio-button :label="10">10x</el-radio-button>
            </el-radio-group>
          </div>
        </div>
        
        <el-slider 
          v-model="inputHour" 
          :min="0" 
          :max="24"
          :step="1"
          @input="jumpToTime"
          show-stops
          :show-tooltip="false"
          class="time-slider"
        ></el-slider>
        <div class="slider-labels">
          <span>0:00</span>
          <span>12:00</span>
          <span>24:00</span>
        </div>
        <div class="control-buttons">
          <el-button 
            @click="jumpToTime" 
            type="primary" 
            size="small"
            icon="el-icon-time"
          >
            跳转到 {{ String(inputHour).padStart(2, '0') }}:00
          </el-button>
          <el-button 
            @click="toggleAnimation" 
            :type="animationPlaying ? 'warning' : 'success'"
            size="small"
            :icon="animationPlaying ? 'el-icon-video-pause' : 'el-icon-video-play'"
          >
            {{ animationPlaying ? '暂停' : '播放' }}
          </el-button>
          <el-button 
            @click="resetAnimation" 
            size="small"
            icon="el-icon-refresh"
          >
            重置
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClockAnimation',
  props: {
    play: {
      type: Boolean,
      default: false
    },
    showSecondHand: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      currentHour: 8,
      currentMinute: 0,
      currentSecond: 0,
      inputHour: 8,
      animationInterval: null,
      animationPlaying: false,
      playbackSpeed: 1
    }
  },
  computed: {
    // 显示用的小时（0-23，动画结束时允许24）
    displayHour() {
      if (this.currentHour >= 24) return 24
      return this.currentHour % 24
    },

    // 时间显示
    currentTimeLabel() {
      const h = this.displayHour
      if (h === 24) {
        return '晚上12时'
      } else if (h === 0) {
        return '凌晨0时'
      } else if (h < 6) {
        return `凌晨${h}时`
      } else if (h < 12) {
        return `上午${h}时`
      } else if (h === 12) {
        return '中午12时'
      } else if (h < 18) {
        return `下午${h - 12}时`
      } else {
        return `晚上${h - 12}时`
      }
    },
    currentTime24() {
      const h = Math.floor(this.displayHour)
      const m = String(this.currentMinute).padStart(2, '0')
      const s = String(this.currentSecond).padStart(2, '0')
      
      if (h === 24) {
        return this.showSecondHand ? '24:00:00' : '24:00'
      }
      
      if (this.showSecondHand) {
        return `${String(h).padStart(2, '0')}:${m}:${s}`
      }
      return `${String(h).padStart(2, '0')}:${m}`
    },
    
    // 已转圈数
    circlesCompleted() {
      return Math.floor(this.currentHour / 12)
    },
    
    // 视频样式，确保全覆盖
    videoStyle() {
      return {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        zIndex: 0,
        pointerEvents: 'none'
      }
    },
    
    // 太阳轨道（东升西落：从左边-90度到右边90度）
    sunOrbitStyle() {
      const h = this.displayHour + (this.currentMinute / 60)
      // 太阳从6点（左侧）升起到18点（右侧）落下
      // 6点: -90度，12点: 0度，18点: 90度
      let angle = -90
      if (h >= 6 && h < 18) {
        const progress = (h - 6) / 12
        angle = -90 + (progress * 180)
      } else if (h >= 18) {
        angle = 90 // 太阳已落下
      } else {
        angle = -90 // 太阳未升起
      }
      
      return {
        transform: `rotate(${angle}deg)`,
        opacity: h >= 6 && h < 18 ? 1 : 0
      }
    },
    
    // 太阳位置
    sunStyle() {
      const h = this.displayHour + (this.currentMinute / 60)
      const distance = 280 // 轨道半径
      const scale = h >= 6 && h < 18 ? 
        (1 + Math.abs(Math.sin((h - 6) / 12 * Math.PI - Math.PI / 2)) * 0.3) : 0
      
      return {
        transform: `translateX(${distance}px) scale(${scale})`,
        opacity: h >= 6 && h < 18 ? 1 : 0
      }
    },
    
    // 月亮轨道（西升东落：从右边90度到左边-90度，与太阳相反）
    moonOrbitStyle() {
      const h = this.displayHour + (this.currentMinute / 60)
      
      // 统一计算角度，解决跨越午夜时的跳动问题
      // 将时间统一映射到从18点开始的轴上
      // 18点 -> 0小时 (90度)
      // 24点(0点) -> 6小时 (0度)
      // 6点 -> 12小时 (-90度)
      
      let effectiveH = h
      if (h < 6) {
        effectiveH = h + 24
      }
      
      // 计算相对于18点过去了多少小时
      const hoursSince18 = effectiveH - 18
      
      // 每小时转动 180/12 = 15度
      // 起始角度 90度 (右侧)
      // 角度 = 90 - (经过小时数 * 15)
      const angle = 90 - (hoursSince18 * 15)
      
      // 计算透明度：在18-19点之间淡入，5-6点之间淡出
      let opacity = 1
      if (h >= 18 && h < 19) {
        // 18-19点：从0渐变到1
        opacity = (h - 18)
      } else if (h >= 19 || h < 5) {
        // 19点到5点：完全显示
        opacity = 1
      } else if (h >= 5 && h < 6) {
        // 5-6点：从1渐变到0
        opacity = 1 - (h - 5)
      } else {
        // 其他时间：不显示
        opacity = 0
      }
      
      return {
        transform: `rotate(${angle}deg)`,
        opacity: opacity
      }
    },
    
    // 月亮位置
    moonStyle() {
      const h = this.displayHour + (this.currentMinute / 60)
      const distance = 280
      
      // 计算透明度：与轨道透明度保持一致
      let opacity = 1
      if (h >= 18 && h < 19) {
        opacity = (h - 18)
      } else if (h >= 19 || h < 5) {
        opacity = 1
      } else if (h >= 5 && h < 6) {
        opacity = 1 - (h - 5)
      } else {
        opacity = 0
      }
      
      return {
        transform: `translateX(${distance}px)`,
        opacity: opacity
      }
    },
    
    // 是否显示星星
    showStars() {
      const h = this.displayHour
      return h >= 19 || h < 5
    },
    
    // 云朵移动
    cloud1Style() {
      return {
        left: `${(this.displayHour / 24) * 200}%`
      }
    },
    cloud2Style() {
      return {
        left: `${((this.displayHour / 24) * 150 + 30)}%`
      }
    },
    cloud3Style() {
      return {
        left: `${((this.displayHour / 24) * 100 + 60)}%`
      }
    },
    
    // ...existing code...
    
    // 钟表时针
    hourHandStyle() {
      // 时针转两圈（0-24小时）
      const totalMinutes = this.currentHour * 60 + this.currentMinute
      const angle = (totalMinutes / 60) * 30 // 每12小时360度，每小时30度
      return {
        transform: `rotate(${angle}deg)`
      }
    },
    
    // 分针
    minuteHandStyle() {
      const totalMinutes = this.currentHour * 60 + this.currentMinute
      const angle = totalMinutes * 6
      return {
        transform: `rotate(${angle}deg)`
      }
    },
    
    // 秒针
    secondHandStyle() {
      const totalSeconds = this.currentHour * 3600 + this.currentMinute * 60 + this.currentSecond
      const angle = totalSeconds * 6
      return {
        transform: `rotate(${angle}deg)`
      }
    },
    
    // 钟表整体样式（保持静止，不随时间旋转）
    clockFaceStyle() {
      return {}
    },
    
    // 地平线颜色
    horizonStyle() {
      const h = this.displayHour + (this.currentMinute / 60)
      const brightness = h >= 6 && h < 18 ? 
        Math.sin((h - 6) / 12 * Math.PI) : 0.3
      return {
        background: `linear-gradient(to top, rgba(50, 50, 100, ${brightness}), transparent)`
      }
    },
    
    // 第一圈圆环样式 (0-12小时)
    circleRing1Style() {
      const h = this.currentHour + (this.currentMinute / 60) + (this.currentSecond / 3600)
      const radius1 = 145 // 第一圈半径
      const circumference = 2 * Math.PI * radius1 // 圆周长
      
      // 第一圈：0-12小时
      let progress = 0
      if (h >= 0 && h < 12) {
        progress = h / 12 // 0-1
      } else if (h >= 12) {
        progress = 1 // 第一圈已完成
      }
      
      const offset = circumference * (1 - progress)
      
      return {
        strokeDasharray: `${circumference}`,
        strokeDashoffset: `${offset}`,
        opacity: h < 24 ? 1 : 0 // 第一圈在24小时内完全显示，第二圈时也保持显示（红色始终可见）
      }
    },
    
    // 第二圈圆环样式 (12-24小时)
    circleRing2Style() {
      const h = this.currentHour + (this.currentMinute / 60) + (this.currentSecond / 3600)
      const radius2 = 160 // 第二圈半径（在第一圈外侧）
      const circumference = 2 * Math.PI * radius2 // 圆周长
      
      // 第二圈：12-24小时
      let progress = 0
      if (h >= 12 && h < 24) {
        progress = (h - 12) / 12 // 0-1
      } else if (h >= 24) {
        progress = 1 // 第二圈已完成
      }
      
      const offset = circumference * (1 - progress)
      
      return {
        strokeDasharray: `${circumference}`,
        strokeDashoffset: `${offset}`,
        opacity: h >= 12 ? 1 : 0 // 第二圈在12小时后显示
      }
    }
  },
  watch: {
    play(newVal) {
      this.animationPlaying = newVal
      if (newVal) {
        if (this.currentHour >= 24) {
          this.resetAnimation()
        }
        this.startAnimation()
      } else {
        this.stopAnimation()
      }
    }
  },
  mounted() {
    this.jumpToTime()
    // 确保视频加载完成后同步进度
    const video = this.$refs.bgVideo
    if (video) {
      video.addEventListener('loadedmetadata', () => {
        this.syncVideoToTime()
      })
    }
  },
  methods: {
    startAnimation() {
      if (this.animationInterval) return
      
      this.animationInterval = setInterval(() => {
        this.currentSecond += (this.playbackSpeed * 5)
        while (this.currentSecond >= 60) {
          this.currentSecond -= 60
          this.currentMinute += 1
          if (this.currentMinute >= 60) {
            this.currentMinute = 0
            this.currentHour += 1
            this.inputHour = this.currentHour
            if (this.currentHour >= 24) {
              this.stopAnimation()
              this.$emit('complete')
              return
            }
          }
        }
        // 同步视频进度
        this.syncVideoToTime()
      }, 20)
    },
    // 同步视频进度到当前时间
    syncVideoToTime() {
      const video = this.$refs.bgVideo
      if (video && video.duration) {
        // 24小时对应视频总时长
        const totalSeconds = this.currentHour * 3600 + this.currentMinute * 60 + this.currentSecond
        const percent = Math.min(totalSeconds / (24 * 3600), 1)
        const targetTime = percent * video.duration
        
        // 直接设置视频时间以保持同步
        video.currentTime = targetTime
        
        // 视频始终保持暂停状态，通过手动更新 currentTime 来实现"播放"效果
        // 这样可以确保视频进度与动画进度完全一致
        if (!video.paused) {
          video.pause()
        }
      }
    },
    stopAnimation() {
      if (this.animationInterval) {
        clearInterval(this.animationInterval)
        this.animationInterval = null
      }
      this.animationPlaying = false
    },
    async toggleAnimation() {
      // 如果已到24时或动画已完成，则先重置动画，等指针归零后再播放
      if (this.currentHour >= 24) {
        await this.resetAndWaitZero()
        this.animationPlaying = true
        this.startAnimation()
      } else {
        this.animationPlaying = !this.animationPlaying
        if (this.animationPlaying) {
          this.startAnimation()
        } else {
          this.stopAnimation()
        }
      }
      this.$emit('update:play', this.animationPlaying)
    },
    // 重置动画并等待指针归零
    resetAndWaitZero() {
      return new Promise(resolve => {
        this.stopAnimation()
        this.currentHour = 0
        this.currentMinute = 0
        this.currentSecond = 0
        this.inputHour = 0
        this.$nextTick(() => {
          // 等待一帧，确保UI已归零
          setTimeout(resolve, 50)
        })
      })
    },
    resetAnimation() {
      this.stopAnimation()
      this.currentHour = 0
      this.currentMinute = 0
      this.currentSecond = 0
      this.inputHour = 0
      
      // 重置视频到开始位置
      this.$nextTick(() => {
        this.syncVideoToTime()
      })
    },
    jumpToTime() {
      this.currentHour = this.inputHour
      this.currentMinute = 0
      this.currentSecond = 0
      this.$nextTick(() => {
        this.syncVideoToTime()
      })
    },
    getNumberStyle(num) {
      const angle = num * 30
      const radius = 120 // 稍微向内收一点，避开刻度
      const x = Math.sin(angle * Math.PI / 180) * radius
      const y = -Math.cos(angle * Math.PI / 180) * radius
      return {
        transform: `translate(${x}px, ${y}px)`
      }
    },
    getMarkStyle(index) {
      // 60 个刻度，每个 6 度
      const angle = index * 6
      return {
        transform: `rotate(${angle}deg)`
      }
    },
    getCraterStyle(index) {
      const positions = [
        { top: '20%', left: '30%', size: '12px' },
        { top: '50%', left: '50%', size: '10px' },
        { top: '70%', right: '25%', size: '8px' }
      ]
      return positions[index - 1]
    },
    getStarStyle(index) {
      const left = (index * 37) % 100 // 分散分布
      const top = (index * 23) % 100
      const size = 2 + (index % 3) // 不同大小
      const delay = index * 0.1 // 闪烁延迟
      
      return {
        left: `${left}%`,
        top: `${top}%`,
        width: `${size}px`,
        height: `${size}px`,
        animationDelay: `${delay}s`
      }
    }
  },
  beforeDestroy() {
    this.stopAnimation()
  }
}
</script>

<style scoped>
.clock-animation {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
}

.clock-animation * {
  box-sizing: border-box;
}

/* 天空容器 */
/* 天空容器 */
.sky-container {
  position: relative;
  width: 100%;
  max-width: 800px;
  height: 600px;
  margin: 20px auto;
  border-radius: 20px;
  overflow: hidden; /* 保持hidden以维持圆角效果 */
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  padding: 0;
  box-sizing: border-box;
}

.bg-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  pointer-events: none;
}

/* 太阳轨道 */
.sun-orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 560px;
  height: 560px;
  margin: -280px 0 0 -280px;
  transform-origin: center;
  transition: transform 0.5s ease, opacity 0.5s ease;
  pointer-events: none;
}

.sun {
  position: absolute;
  top: 0;
  left: 0;
  width: 80px;
  height: 80px;
  transform-origin: center;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.sun::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, #fff 10%, #fff700 30%, #ff8c00 60%, #ff4500 100%);
  border-radius: 50%;
  box-shadow: 
    0 0 40px #ffd700,
    0 0 80px #ff8c00,
    0 0 120px rgba(255, 215, 0, 0.5);
  animation: sunGlow 3s ease-in-out infinite;
}

.sun-rays {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
  z-index: -1;
}

.sun-rays::before,
.sun-rays::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background: repeating-conic-gradient(
    from 0deg,
    rgba(255, 215, 0, 0.1) 0deg 10deg,
    transparent 10deg 20deg
  );
  border-radius: 50%;
}

.sun-rays::after {
  transform: translate(-50%, -50%) rotate(15deg);
  opacity: 0.5;
}

@keyframes sunGlow {
  0%, 100% {
    box-shadow: 
      0 0 40px #ffd700,
      0 0 80px #ff8c00,
      0 0 120px rgba(255, 215, 0, 0.5);
    transform: scale(1);
  }
  50% {
    box-shadow: 
      0 0 60px #ffd700,
      0 0 100px #ff8c00,
      0 0 140px rgba(255, 215, 0, 0.7);
    transform: scale(1.05);
  }
}

/* 月亮轨道 */
.moon-orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 560px;
  height: 560px;
  margin: -280px 0 0 -280px;
  transform-origin: center;
  transition: transform 0.5s ease, opacity 0.5s ease;
  pointer-events: none;
}

.moon {
  position: absolute;
  top: 0;
  left: 0;
  width: 60px;
  height: 60px;
  transform-origin: center;
  transition: transform 0.5s ease, opacity 0.5s ease;
  background: radial-gradient(circle at 30% 30%, #f5f5f5, #ddd, #bbb);
  border-radius: 50%;
  box-shadow: 
    0 0 20px rgba(255, 255, 255, 0.5),
    inset -10px -10px 20px rgba(0, 0, 0, 0.2);
  position: relative;
}

.moon-crater {
  position: absolute;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  box-shadow: inset 2px 2px 3px rgba(0, 0, 0, 0.3), 1px 1px 1px rgba(255, 255, 255, 0.2);
}

/* 星星 */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.star {
  position: absolute;
  background: white;
  border-radius: 50%;
  box-shadow: 0 0 6px white, 0 0 12px rgba(255, 255, 255, 0.5);
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

/* 云朵 */
.clouds {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 40%;
  pointer-events: none;
  opacity: 0.9;
}

.cloud {
  position: absolute;
  background: linear-gradient(to bottom, #fff 0%, #f1f1f1 100%);
  border-radius: 50px;
  transition: left 1s linear;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.1));
}

.cloud::before,
.cloud::after {
  content: '';
  position: absolute;
  background: inherit;
  border-radius: 50%;
}

.cloud-1 {
  width: 100px;
  height: 40px;
  top: 50px;
}

.cloud-1::before {
  width: 50px;
  height: 50px;
  top: -25px;
  left: 15px;
}

.cloud-1::after {
  width: 40px;
  height: 40px;
  top: -15px;
  right: 15px;
}

.cloud-2 {
  width: 120px;
  height: 50px;
  top: 80px;
}

.cloud-2::before {
  width: 60px;
  height: 60px;
  top: -30px;
  left: 20px;
}

.cloud-2::after {
  width: 50px;
  height: 50px;
  top: -20px;
  right: 20px;
}

.cloud-3 {
  width: 110px;
  height: 45px;
  top: 120px;
}

.cloud-3::before {
  width: 55px;
  height: 55px;
  top: -28px;
  left: 18px;
}

.cloud-3::after {
  width: 45px;
  height: 45px;
  top: -18px;
  right: 18px;
}

/* 地球和钟表容器 */
.earth-clock-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 400px;
  overflow: visible; /* 确保圆环不会被裁剪 */
}

/* 已移除地球相关样式 */

/* 外围圆环容器 */
.circle-ring-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 360px;
  height: 360px;
  z-index: 15; /* 在钟表上方，确保圆环完全可见 */
  pointer-events: none;
  overflow: visible; /* 确保圆环不会被裁剪 */
}

.circle-ring-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg); /* 从顶部开始 */
}

.circle-ring {
  fill: none;
  stroke-width: 16;
  stroke-linecap: round;
  transform-origin: center;
  transition: stroke-dashoffset 0.3s ease, opacity 0.3s ease;
}

.circle-ring-1 {
  stroke: #e74c3c; /* 第一圈颜色 - 红色 */
  filter: drop-shadow(0 0 8px rgba(231, 76, 60, 0.8));
}

.circle-ring-2 {
  stroke: #3498db; /* 第二圈颜色 - 蓝色 */
  filter: drop-shadow(0 0 8px rgba(52, 152, 219, 0.8));
}

/* 钟表 */
.clock-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  z-index: 10; /* 降低z-index，确保不会遮挡其他重要元素，但高于earth */
}

.clock-face {
  position: relative;
  width: 100%;
  height: 100%;
  border: 10px solid #333;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
  box-shadow: 
    0 0 30px rgba(0, 0, 0, 0.3),
    inset 0 0 30px rgba(255, 255, 255, 0.8),
    inset -5px -5px 10px rgba(0, 0, 0, 0.1);
  /* 保持表盘静止，只让指针转动 */
}

.clock-mark {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: center bottom;
  z-index: 1; /* 确保刻度在表盘背景之上 */
}

.clock-number {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 30px;
  height: 30px;
  margin: -15px 0 0 -15px;
  font-size: 22px;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  z-index: 2; /* 确保数字在刻度之上 */
}

.hour-hand, .minute-hand, .second-hand {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: center bottom;
  border-radius: 4px;
  transition: transform 0.5s ease;
  z-index: 20; /* 确保指针在圆环上方 */
}

.hour-hand {
  width: 8px;
  height: 90px;
  margin: -90px 0 0 -4px;
  background: linear-gradient(to top, #333 0%, #666 100%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.minute-hand {
  width: 5px;
  height: 120px;
  margin: -120px 0 0 -2.5px;
  background: linear-gradient(to top, #666 0%, #999 100%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.second-hand {
  width: 2px;
  height: 130px;
  margin: -130px 0 0 -1px;
  background: #f56c6c;
  box-shadow: 0 0 4px rgba(245, 108, 108, 0.5);
}

.center-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 18px;
  height: 18px;
  margin: -9px 0 0 -9px;
  background: radial-gradient(circle, #333 0%, #666 100%);
  border-radius: 50%;
  z-index: 25; /* 确保中心点在指针和圆环上方 */
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}

.circle-indicator {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(102, 126, 234, 0.9);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 20;
}

/* 地平线 */
.horizon {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 150px;
  pointer-events: none;
  transition: background 0.5s ease;
}

/* 时间显示面板 */
.time-display-panel {
  width: 100%;
  max-width: 800px;
  margin-top: 30px;
  padding: 25px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 0 0 1px rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.control-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.speed-control {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.5);
  padding: 5px 10px;
  border-radius: 20px;
}

.speed-label {
  font-size: 14px;
  color: #666;
  font-weight: bold;
}

.time-display {
  text-align: center;
  margin-bottom: 20px;
}

.time-label {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.time-24 {
  font-size: 40px;
  font-weight: bold;
  color: #667eea;
  font-family: 'Courier New', monospace;
}

.time-control {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.time-slider {
  width: 100%;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
  padding: 0 12px;
}

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
