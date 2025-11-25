<template>
  <div class="time-scale">
    <div class="scale-wrapper">
      <div 
        v-for="hour in 24" 
        :key="hour"
        class="scale-item"
        :class="{ active: selectedHour === hour - 1 }"
        @click="selectHour(hour - 1)"
        :style="getItemStyle(hour - 1)"
      >
        <div class="hour-mark">{{ hour - 1 }}:00</div>
        <div class="hour-label">{{ getTimeLabel(hour - 1) }}</div>
      </div>
    </div>
    
    <div class="selected-time" v-if="selectedHour !== null">
      <el-card>
        <h4>选中时间</h4>
        <div class="time-info">
          <div class="time-24">{{ String(selectedHour).padStart(2, '0') }}:00</div>
          <div class="time-12">{{ getTimeLabel(selectedHour) }}</div>
          <div class="time-rule" v-if="selectedHour >= 12">
            转换规则：{{ selectedHour }} - 12 = {{ selectedHour - 12 }}（下午/晚上{{ selectedHour - 12 }}时）
          </div>
          <div class="time-rule" v-else>
            转换规则：上午/中午时间，12时计时法与24时计时法相同
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimeScale',
  data() {
    return {
      selectedHour: null
    }
  },
  methods: {
    selectHour(hour) {
      this.selectedHour = hour
      const timeLabel = this.getTimeLabel(hour)
      this.$emit('time-select', `${String(hour).padStart(2, '0')}:00 (${timeLabel})`)
    },
    getTimeLabel(hour) {
      if (hour === 0) {
        return '凌晨0时'
      } else if (hour < 6) {
        return `凌晨${hour}时`
      } else if (hour < 12) {
        return `上午${hour}时`
      } else if (hour === 12) {
        return '中午12时'
      } else if (hour < 18) {
        return `下午${hour - 12}时`
      } else {
        return `晚上${hour - 12}时`
      }
    },
    getItemStyle(hour) {
      const isNight = hour >= 18 || hour < 6
      const isDay = hour >= 6 && hour < 18
      return {
        background: isNight ? '#1a1a2e' : isDay ? '#87ceeb' : '#ffd700',
        color: isNight ? '#fff' : '#333'
      }
    }
  }
}
</script>

<style scoped>
.time-scale {
  width: 100%;
}

.scale-wrapper {
  display: flex;
  width: 100%;
  overflow-x: auto;
  padding: 20px 0;
  background: #f5f5f5;
  border-radius: 8px;
  position: relative;
  min-height: 150px;
}

.scale-item {
  flex: 0 0 80px;
  min-width: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 5px;
  margin: 0 5px;
  transition: all 0.3s;
  padding: 10px;
  border: 2px solid transparent;
  position: relative;
}

.scale-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.scale-item.active {
  border-color: #667eea;
  box-shadow: 0 0 15px rgba(102, 126, 234, 0.5);
  transform: scale(1.1);
}

.hour-mark {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
  font-family: 'Courier New', monospace;
}

.hour-label {
  font-size: 12px;
  text-align: center;
  line-height: 1.2;
}

.selected-time {
  margin-top: 30px;
}

.selected-time h4 {
  font-size: 18px;
  color: #667eea;
  margin-bottom: 15px;
  text-align: center;
}

.time-info {
  text-align: center;
}

.time-24 {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  font-family: 'Courier New', monospace;
  margin-bottom: 10px;
}

.time-12 {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
}

.time-rule {
  font-size: 14px;
  color: #666;
  padding: 10px;
  background: #f0f0f0;
  border-radius: 5px;
  margin-top: 10px;
}

/* 滚动条样式 */
.scale-wrapper::-webkit-scrollbar {
  height: 8px;
}

.scale-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.scale-wrapper::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 4px;
}

.scale-wrapper::-webkit-scrollbar-thumb:hover {
  background: #5568d3;
}
</style>

