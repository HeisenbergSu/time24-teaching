<template>
  <div class="time-scale-expanded">
    <div class="scale-wrapper">
      <div class="scale-header">
        <div class="scale-legend top">12时计时法</div>
        <div class="scale-legend bottom">24时计时法</div>
      </div>
      
      <div class="ruler-container" ref="rulerContainer">
        <!-- 24个时间切片 -->
        <div 
          v-for="hour in 24" 
          :key="hour"
          class="hour-slice"
          :class="{ 
            active: selectedHour === hour - 1,
            'is-day': hour - 1 >= 6 && hour - 1 < 18
          }"
          @click="selectHour(hour - 1)"
        >
          <!-- 上部分：12时 -->
          <div class="scale-part top-scale">
            <div class="tick-label">{{ get12HourLabel(hour - 1) }}</div>
            <div class="tick-mark"></div>
          </div>
          
          <!-- 中间部分：动画区域 -->
          <div class="animation-zone">
            <div class="connector-line"></div>
            <transition name="fade">
              <div v-if="selectedHour === hour - 1" class="active-indicator">
                <!-- 12转24：向下箭头 -->
                <div v-if="conversionDirection === '12to24'" class="arrow-anim down">
                  <i class="el-icon-bottom"></i>
                </div>
                <!-- 24转12：向上箭头 -->
                <div v-else class="arrow-anim up">
                  <i class="el-icon-top"></i>
                </div>
              </div>
            </transition>
          </div>
          
          <!-- 下部分：24时 -->
          <div class="scale-part bottom-scale">
            <div class="tick-mark"></div>
            <div class="tick-label number-font">{{ String(hour - 1).padStart(2, '0') }}:00</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimeScaleExpanded',
  props: {
    selectedHour: {
      type: Number,
      default: 0
    },
    conversionDirection: {
      type: String,
      default: '12to24'
    }
  },
  watch: {
    selectedHour(val) {
      this.scrollToHour(val)
    }
  },
  mounted() {
    if (this.selectedHour !== null) {
      this.scrollToHour(this.selectedHour)
    }
  },
  methods: {
    selectHour(hour) {
      this.$emit('hour-select', hour)
    },
    scrollToHour(hour) {
      // 简单滚动到可视区域
      this.$nextTick(() => {
        const container = this.$refs.rulerContainer
        const items = container.getElementsByClassName('hour-slice')
        if (items[hour]) {
          const item = items[hour]
          const scrollLeft = item.offsetLeft - container.clientWidth / 2 + item.clientWidth / 2
          container.scrollTo({
            left: scrollLeft,
            behavior: 'smooth'
          })
        }
      })
    },
    get12HourLabel(hour) {
      if (hour === 0) return '凌晨0时'
      if (hour < 6) return `凌晨${hour}时`
      if (hour < 12) return `上午${hour}时`
      if (hour === 12) return '中午12时'
      return `下午/晚${hour - 12}时`
    }
  }
}
</script>

<style scoped>
.time-scale-expanded {
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  /* Removed overflow: hidden to allow scrollbars to be potentially visible on container if needed, 
     but mainly ruler-container handles it */
}

.scale-wrapper {
  position: relative;
  padding: 20px 0;
  width: 100%; /* Ensure full width */
}

/* ... existing styles ... */

.ruler-container {
  display: flex;
  overflow-x: auto; /* Enables horizontal scrolling */
  padding-left: 80px; /* Header width */
  padding-right: 20px;
  scrollbar-width: thin; /* Firefox */
  /* Ensure it takes space */
  width: 100%;
  box-sizing: border-box;
}

.ruler-container::-webkit-scrollbar {
  height: 12px; /* Make scrollbar larger and easier to click */
}

.ruler-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 6px;
}

.ruler-container::-webkit-scrollbar-thumb {
  background: #c0c4cc;
  border-radius: 6px;
  border: 2px solid #f1f1f1; /* Add border to thumb for better contrast */
}

.ruler-container::-webkit-scrollbar-thumb:hover {
  background: #909399;
}

.hour-slice {
  flex: 0 0 60px; /* 缩小宽度，让更多时间显示在屏幕内 (原80px) */
  display: flex;
  flex-direction: column;
  height: 300px;
  cursor: pointer;
  transition: background 0.3s;
  border-right: 1px dashed #eee;
  position: relative;
}

.hour-slice:hover {
  background: #f5f7fa;
}

.hour-slice.active {
  background: #ecf5ff;
}

.scale-part {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding: 10px 0;
}

.scale-part.top-scale {
  border-bottom: 2px solid #e6a23c;
  color: #606266;
}

.scale-part.bottom-scale {
  justify-content: flex-start;
  border-top: 2px solid #409EFF;
  color: #606266;
}

.tick-mark {
  width: 2px;
  height: 10px;
  background: #333;
  margin: 5px 0;
}

.tick-label {
  font-size: 14px;
  text-align: center;
  padding: 0 5px;
}

.number-font {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  font-size: 16px;
}

.animation-zone {
  height: 80px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.connector-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background: #eee;
  z-index: 0;
}

.active-indicator {
  z-index: 1;
}

.arrow-anim {
  font-size: 24px;
  font-weight: bold;
  color: #67C23A;
  animation-duration: 1.5s;
  animation-iteration-count: infinite;
}

.arrow-anim.down {
  color: #e6a23c;
  animation-name: moveDown;
}

.arrow-anim.up {
  color: #409EFF;
  animation-name: moveUp;
}

@keyframes moveDown {
  0% { transform: translateY(-20px); opacity: 0; }
  20% { opacity: 1; }
  80% { transform: translateY(20px); opacity: 1; }
  100% { transform: translateY(25px); opacity: 0; }
}

@keyframes moveUp {
  0% { transform: translateY(20px); opacity: 0; }
  20% { opacity: 1; }
  80% { transform: translateY(-20px); opacity: 1; }
  100% { transform: translateY(-25px); opacity: 0; }
}
</style>