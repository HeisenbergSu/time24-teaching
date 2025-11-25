<template>
  <div class="teacher-dashboard">
    <!-- 登录页面 -->
    <div v-if="!isLoggedIn" class="login-section">
      <el-card class="login-card">
        <h2>教师后台登录</h2>
        <el-form :model="loginForm" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-button type="primary" @click="login" style="width: 100%">登录</el-button>
        </el-form>
      </el-card>
    </div>
    
    <!-- 后台管理页面 -->
    <div v-else class="dashboard-content">
      <div class="header">
        <h1>教师后台管理系统</h1>
        <el-button @click="logout" type="text">退出登录</el-button>
      </div>
      
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <!-- 数据统计 -->
        <el-tab-pane label="数据统计" name="statistics">
          <div class="statistics-section">
            <h2>整体数据统计</h2>
            
            <el-row :gutter="20" class="stats-row">
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-icon">👥</div>
                  <div class="stat-value">{{ statistics.total_students }}</div>
                  <div class="stat-label">总学生数</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-icon">📝</div>
                  <div class="stat-value">{{ statistics.total_answers }}</div>
                  <div class="stat-label">总答题数</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-icon">✅</div>
                  <div class="stat-value">{{ statistics.correct_answers }}</div>
                  <div class="stat-label">正确答题数</div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-icon">📊</div>
                  <div class="stat-value">{{ statistics.avg_score }}%</div>
                  <div class="stat-label">平均得分</div>
                </el-card>
              </el-col>
            </el-row>
            
            <h3>模块统计</h3>
            <el-row :gutter="20" class="module-stats-row">
              <el-col :span="6" v-for="(stats, module) in statistics.module_stats" :key="module">
                <el-card>
                  <h4>{{ getModuleName(module) }}</h4>
                  <div class="module-stat-item">
                    <span>总题数：</span>
                    <strong>{{ stats.total }}</strong>
                  </div>
                  <div class="module-stat-item">
                    <span>正确数：</span>
                    <strong style="color: #67c23a">{{ stats.correct }}</strong>
                  </div>
                  <div class="module-stat-item">
                    <span>正确率：</span>
                    <strong style="color: #667eea">{{ stats.accuracy }}%</strong>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            
            <div class="refresh-section">
              <el-button @click="loadStatistics" type="primary" icon="el-icon-refresh">刷新数据</el-button>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 学生成绩 -->
        <el-tab-pane label="学生成绩" name="students">
          <div class="students-section">
            <h2>学生成绩列表</h2>
            
            <el-table :data="students" style="width: 100%">
              <el-table-column prop="name" label="姓名" width="150"></el-table-column>
              <el-table-column prop="class_name" label="班级" width="150"></el-table-column>
              <el-table-column prop="total" label="总题数" width="120" align="center"></el-table-column>
              <el-table-column prop="correct" label="正确数" width="120" align="center"></el-table-column>
              <el-table-column prop="score" label="得分" width="150" align="center">
                <template slot-scope="scope">
                  <el-progress 
                    :percentage="scope.row.score" 
                    :color="getScoreColor(scope.row.score)"
                    :stroke-width="20"
                  ></el-progress>
                  <span style="margin-left: 10px;">{{ scope.row.score }}%</span>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="refresh-section">
              <el-button @click="loadStudents" type="primary" icon="el-icon-refresh">刷新列表</el-button>
            </div>
          </div>
        </el-tab-pane>
        
        <!-- 错题分析 -->
        <el-tab-pane label="错题分析" name="wrong-questions">
          <div class="wrong-questions-section">
            <h2>错题分析</h2>
            <p class="section-desc">按错误率排序，帮助您精准定位教学难点</p>
            
            <el-table :data="wrongQuestions" style="width: 100%">
              <el-table-column type="index" label="序号" width="80" align="center"></el-table-column>
              <el-table-column prop="question" label="题目" min-width="300"></el-table-column>
              <el-table-column prop="total_attempts" label="总答题数" width="120" align="center"></el-table-column>
              <el-table-column prop="wrong_count" label="错误数" width="120" align="center">
                <template slot-scope="scope">
                  <span style="color: #f56c6c; font-weight: bold;">{{ scope.row.wrong_count }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="error_rate" label="错误率" width="150" align="center">
                <template slot-scope="scope">
                  <el-progress 
                    :percentage="scope.row.error_rate" 
                    color="#f56c6c"
                    :stroke-width="20"
                  ></el-progress>
                  <span style="margin-left: 10px;">{{ scope.row.error_rate }}%</span>
                </template>
              </el-table-column>
              <el-table-column prop="wrong_students" label="错误学生数" width="150" align="center">
                <template slot-scope="scope">
                  {{ scope.row.wrong_students.length }}人
                </template>
              </el-table-column>
            </el-table>
            
            <div class="refresh-section">
              <el-button @click="loadWrongQuestions" type="primary" icon="el-icon-refresh">刷新分析</el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TeacherDashboard',
  data() {
    return {
      isLoggedIn: false,
      loginForm: {
        username: '',
        password: ''
      },
      activeTab: 'statistics',
      statistics: {
        total_students: 0,
        total_answers: 0,
        correct_answers: 0,
        avg_score: 0,
        module_stats: {}
      },
      students: [],
      wrongQuestions: []
    }
  },
  mounted() {
    // 检查是否已登录
    const savedLogin = localStorage.getItem('teacherLoggedIn')
    if (savedLogin === 'true') {
      this.isLoggedIn = true
      this.loadData()
    }
  },
  methods: {
    async login() {
      if (!this.loginForm.username || !this.loginForm.password) {
        this.$message.error('请输入用户名和密码')
        return
      }
      
      try {
        const res = await this.$http.post('/teacher/login', {
          username: this.loginForm.username,
          password: this.loginForm.password
        })
        
        if (res.data.success) {
          this.isLoggedIn = true
          localStorage.setItem('teacherLoggedIn', 'true')
          this.$message.success('登录成功')
          this.loadData()
        } else {
          this.$message.error(res.data.message || '登录失败')
        }
      } catch (error) {
        this.$message.error('登录失败，请检查用户名和密码')
      }
    },
    logout() {
      this.isLoggedIn = false
      localStorage.removeItem('teacherLoggedIn')
      this.$message.success('已退出登录')
    },
    async loadData() {
      await Promise.all([
        this.loadStatistics(),
        this.loadStudents(),
        this.loadWrongQuestions()
      ])
    },
    async loadStatistics() {
      try {
        const res = await this.$http.get('/teacher/statistics')
        this.statistics = res.data
      } catch (error) {
        this.$message.error('加载统计数据失败')
      }
    },
    async loadStudents() {
      try {
        const res = await this.$http.get('/teacher/students')
        this.students = res.data.students || []
      } catch (error) {
        this.$message.error('加载学生列表失败')
      }
    },
    async loadWrongQuestions() {
      try {
        const res = await this.$http.get('/teacher/wrong-questions')
        this.wrongQuestions = res.data.wrong_questions || []
      } catch (error) {
        this.$message.error('加载错题分析失败')
      }
    },
    handleTabClick(tab) {
      this.activeTab = tab.name
      if (this.activeTab === 'statistics') {
        this.loadStatistics()
      } else if (this.activeTab === 'students') {
        this.loadStudents()
      } else if (this.activeTab === 'wrong-questions') {
        this.loadWrongQuestions()
      }
    },
    getModuleName(module) {
      const names = {
        'explore': '课前探索',
        'learn': '新知学习',
        'practice': '生活应用',
        'challenge': '成就挑战'
      }
      return names[module] || module
    },
    getScoreColor(score) {
      if (score >= 80) return '#67c23a'
      if (score >= 60) return '#e6a23c'
      return '#f56c6c'
    }
  }
}
</script>

<style scoped>
.teacher-dashboard {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.login-card {
  width: 400px;
}

.login-card h2 {
  text-align: center;
  color: #667eea;
  margin-bottom: 30px;
}

.dashboard-content {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  min-height: 80vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.header h1 {
  color: #667eea;
  font-size: 28px;
}

.statistics-section h2,
.students-section h2,
.wrong-questions-section h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
  padding: 20px;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 16px;
  color: #666;
}

.module-stats-row {
  margin-bottom: 30px;
}

.module-stat-item {
  margin: 10px 0;
  font-size: 14px;
  color: #333;
}

.module-stat-item strong {
  margin-left: 10px;
  font-size: 16px;
}

.section-desc {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

.refresh-section {
  margin-top: 30px;
  text-align: center;
}

::v-deep .el-tabs__item {
  font-size: 18px;
  font-weight: bold;
}

::v-deep .el-tabs__item.is-active {
  color: #667eea;
}

::v-deep .el-tabs__active-bar {
  background-color: #667eea;
}
</style>

