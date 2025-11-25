<template>
  <div class="student-home">
    <!-- 未登录状态 -->
    <div v-if="!studentId" class="login-section">
      <el-card class="login-card">
        <div class="login-header">
          <div class="icon-wrapper">
            <i class="el-icon-time"></i>
          </div>
          <h2 class="login-title">24时计时法课堂教学系统</h2>
          <p class="login-subtitle">小学三年级数学 - 时间学习</p>
        </div>
        <el-form :model="registerForm" label-width="80px" class="login-form">
          <el-form-item label="姓名">
            <el-input 
              v-model="registerForm.name" 
              placeholder="请输入你的姓名"
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item label="班级">
            <el-input 
              v-model="registerForm.className" 
              placeholder="请输入班级（如：三年级一班）"
              size="large"
            ></el-input>
          </el-form-item>
          <el-button 
            type="primary" 
            @click="register" 
            size="large"
            class="login-button"
          >
            开始学习
          </el-button>
        </el-form>
        <div class="teacher-link">
          <el-link @click="goToTeacher" type="primary">教师入口 →</el-link>
        </div>
      </el-card>
    </div>

    <!-- 已登录状态 - 模块卡片 (已由App.vue中的NavMenu接管，此处移除) -->
    <div v-else class="modules-section-placeholder">
      <!-- 空占位符，NavMenu 会覆盖在上面 -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentHome',
  data() {
    return {
      studentId: null,
      studentName: '',
      registerForm: {
        name: '',
        className: '三年级一班'
      }
      // modules: [...] // 已移除，由NavMenu管理
    }
  },
  mounted() {
    const savedStudentId = localStorage.getItem('studentId')
    const savedStudentName = localStorage.getItem('studentName')
    if (savedStudentId) {
      this.studentId = parseInt(savedStudentId)
      this.studentName = savedStudentName || '同学'
    }
  },
  methods: {
    async register() {
      if (!this.registerForm.name) {
        this.$message.error('请输入姓名')
        return
      }
      try {
        const res = await this.$http.post('/student/register', {
          name: this.registerForm.name,
          class_name: this.registerForm.className
        })
        if (res.data.success) {
          this.studentId = res.data.student_id
          this.studentName = this.registerForm.name
          localStorage.setItem('studentId', this.studentId)
          localStorage.setItem('studentName', this.studentName)
          this.$message.success('注册成功！')
          this.$emit('login-success')
        }
      } catch (error) {
        this.$message.error('注册失败，请重试')
      }
    },
    goToTeacher() {
      this.$router.push('/teacher')
    }
  }
}
</script>

<style scoped>
.student-home {
  min-height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 50%, #fff3e0 100%);
  padding: 40px 20px;
}

/* 登录区域 */
.login-section {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.login-card {
  width: 100%;
  max-width: 450px;
  text-align: center;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.login-header {
  margin-bottom: 30px;
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper i {
  font-size: 40px;
  color: white;
}

.login-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 0;
}

.login-form {
  margin-top: 30px;
}

.login-button {
  width: 100%;
  margin-top: 10px;
  font-size: 16px;
  height: 44px;
}

.teacher-link {
  margin-top: 20px;
  text-align: right;
}
</style>
