<template>
  <div id="app">
    <NavMenu 
      v-if="shouldShowNav" 
      :mode="navMode" 
    />
    <div 
      class="app-content" 
      :class="{ 'with-sidebar': navMode === 'sidebar' && shouldShowNav }"
    >
      <router-view @login-success="checkLoginStatus"/>
    </div>
  </div>
</template>

<script>
import NavMenu from './components/NavMenu.vue'

export default {
  name: 'App',
  components: {
    NavMenu
  },
  data() {
    return {
      isLoggedIn: false
    }
  },
  computed: {
    isTeacherPage() {
      return this.$route.path.startsWith('/teacher')
    },
    shouldShowNav() {
      return this.isLoggedIn && !this.isTeacherPage
    },
    navMode() {
      return this.$route.path === '/' ? 'center' : 'sidebar'
    }
  },
  created() {
    this.checkLoginStatus()
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('studentId')
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 50%, #fff3e0 100%);
  min-height: 100vh;
  color: #333;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}

.app-content {
  min-height: 100vh;
  transition: padding-left 0.3s ease;
}

.app-content.with-sidebar {
  padding-left: 280px;
}

/* 全局滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #5568d3;
}

/* Element UI 样式覆盖 */
.el-card {
  border-radius: 12px;
  border: 1px solid #e4e7ed;
}

.el-button {
  border-radius: 8px;
}

.el-input__inner {
  border-radius: 8px;
}
</style>

