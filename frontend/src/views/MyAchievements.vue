<template>
  <div class="achievements-page">
    <div class="page-header">
      <el-button 
        @click="goBack" 
        icon="el-icon-arrow-left" 
        circle
        class="back-button"
      ></el-button>
      <h1 class="page-title">我的成就</h1>
    </div>

    <div class="achievements-container">
      <!-- 成绩统计 -->
      <el-card class="stats-card">
        <h2 class="card-title">📊 成绩统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">📝</div>
            <div class="stat-value">{{ totalAnswers }}</div>
            <div class="stat-label">总答题数</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">✅</div>
            <div class="stat-value">{{ correctAnswers }}</div>
            <div class="stat-label">正确题数</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{{ overallScore }}%</div>
            <div class="stat-label">总得分</div>
          </div>
        </div>
      </el-card>

      <!-- 模块完成情况 -->
      <el-card class="modules-card">
        <h2 class="card-title">🎯 模块完成情况</h2>
        <div class="modules-list">
          <div 
            v-for="module in modules" 
            :key="module.id"
            class="module-item"
          >
            <div class="module-info">
              <div :class="['module-icon', module.color]">
                <i :class="module.icon"></i>
              </div>
              <div class="module-details">
                <h3>{{ module.title }}</h3>
                <p>{{ module.description }}</p>
              </div>
            </div>
            <div class="module-status">
              <el-progress 
                :percentage="module.progress" 
                :color="module.progress === 100 ? '#67c23a' : '#409eff'"
                :stroke-width="12"
              ></el-progress>
              <span class="progress-text">{{ module.completed }}/{{ module.total }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 徽章展示 -->
      <el-card class="badges-card">
        <h2 class="card-title">🏅 获得的徽章</h2>
        <div class="badges-grid">
          <div 
            v-for="badge in badges" 
            :key="badge.id"
            class="badge-item"
            :class="{ earned: badge.earned }"
          >
            <div class="badge-icon">{{ badge.icon }}</div>
            <div class="badge-name">{{ badge.name }}</div>
            <div class="badge-desc">{{ badge.description }}</div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyAchievements',
  data() {
    return {
      studentId: null,
      totalAnswers: 0,
      correctAnswers: 0,
      overallScore: 0,
      modules: [
        {
          id: 'explore',
          title: '课前探索',
          description: '完成旧知复习和情景导入',
          icon: 'el-icon-light-rain',
          color: 'icon-yellow',
          completed: 0,
          total: 6,
          progress: 0
        },
        {
          id: 'practice',
          title: '生活应用',
          description: '完成时间转换练习',
          icon: 'el-icon-time',
          color: 'icon-green',
          completed: 0,
          total: 4,
          progress: 0
        },
        {
          id: 'challenge',
          title: '成就挑战',
          description: '完成综合测验',
          icon: 'el-icon-trophy',
          color: 'icon-purple',
          completed: 0,
          total: 5,
          progress: 0
        }
      ],
      badges: [
        {
          id: 'explorer',
          icon: '🔍',
          name: '探索者',
          description: '完成课前探索',
          earned: false
        },
        {
          id: 'learner',
          icon: '📚',
          name: '学习者',
          description: '完成新知学习',
          earned: false
        },
        {
          id: 'practitioner',
          icon: '⚡',
          name: '实践者',
          description: '完成生活应用',
          earned: false
        },
        {
          id: 'champion',
          icon: '🏆',
          name: '挑战者',
          description: '完成成就挑战',
          earned: false
        },
        {
          id: 'perfect',
          icon: '⭐',
          name: '完美主义',
          description: '所有题目全对',
          earned: false
        }
      ]
    }
  },
  mounted() {
    const savedStudentId = localStorage.getItem('studentId')
    if (savedStudentId) {
      this.studentId = parseInt(savedStudentId)
    }
    this.loadAchievements()
  },
  methods: {
    async loadAchievements() {
      try {
        // 加载学生成绩
        const res = await this.$http.get(`/student/${this.studentId}/score`)
        if (res.data) {
          this.totalAnswers = res.data.total || 0
          this.correctAnswers = res.data.correct || 0
          this.overallScore = res.data.score || 0
          
          // 使用后端返回的模块数据更新模块完成情况
          if (res.data.modules) {
            this.updateModuleProgress(res.data.modules)
          }
        }
        
        // 检查徽章
        this.checkBadges()
      } catch (error) {
        console.error('加载成就失败:', error)
        this.$message.error('加载成就失败')
      }
    },
    updateModuleProgress(modulesData) {
      // 更新课前探索
      if (modulesData.explore) {
        this.modules[0].completed = modulesData.explore.completed || 0
      }

      // 更新生活应用
      if (modulesData.practice) {
        this.modules[1].completed = modulesData.practice.completed || 0
      }

      // 更新成就挑战
      if (modulesData.challenge) {
        this.modules[2].completed = modulesData.challenge.completed || 0
      }

      // 计算进度
      this.modules.forEach(module => {
        module.progress = Math.round((module.completed / module.total) * 100)
      })
    },
    checkBadges() {
      // 检查探索者徽章
      if (this.modules[0].progress === 100) {
        this.badges[0].earned = true
      }

      // 检查学习者徽章（新知学习模块默认完成）
      this.badges[1].earned = true

      // 检查实践者徽章
      if (this.modules[1].progress === 100) {
        this.badges[2].earned = true
      }

      // 检查挑战者徽章
      if (this.modules[2].progress === 100) {
        this.badges[3].earned = true
      }

      // 检查完美主义徽章
      if (this.overallScore === 100 && this.totalAnswers > 0) {
        this.badges[4].earned = true
      }
    },
    goBack() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.achievements-page {
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

.achievements-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.stats-card,
.modules-card,
.badges-card {
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}

.stat-item {
  text-align: center;
  padding: 24px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  border-radius: 12px;
  transition: transform 0.3s;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: #666;
}

.modules-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.module-item {
  padding: 20px;
  background: #fafafa;
  border-radius: 12px;
  border: 2px solid #e4e7ed;
}

.module-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

.module-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.module-icon i {
  font-size: 28px;
  color: white;
}

.icon-yellow {
  background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%);
}

.icon-green {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.icon-purple {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.module-details h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 4px;
}

.module-details p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.module-status {
  display: flex;
  align-items: center;
  gap: 16px;
}

.module-status ::v-deep .el-progress {
  flex: 1;
}

.progress-text {
  font-size: 14px;
  color: #666;
  font-weight: bold;
  min-width: 80px;
  text-align: right;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.badge-item {
  text-align: center;
  padding: 24px;
  background: #f5f5f5;
  border-radius: 12px;
  border: 2px solid #e0e0e0;
  opacity: 0.5;
  transition: all 0.3s;
}

.badge-item.earned {
  background: linear-gradient(135deg, #fff9e6 0%, #ffe0b2 100%);
  border-color: #ffd54f;
  opacity: 1;
  box-shadow: 0 4px 12px rgba(255, 213, 79, 0.3);
}

.badge-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.badge-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.badge-desc {
  font-size: 14px;
  color: #666;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .badges-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>

