<template>
  <div :class="['nav-menu', mode]">
    <div class="nav-content" :class="{ 'accordion-mode': true }">
      <div 
        v-for="module in modules" 
        :key="module.id"
        class="nav-item"
        :class="[module.color, { active: currentPath === module.path }]"
        @click="handleModuleClick(module.path)"
      >
        <div class="nav-item-bg"></div>
        <div class="nav-item-content">
          <div class="icon-box">
            <i :class="module.icon"></i>
          </div>
          <div class="text-box">
            <h3 class="title">{{ module.title }}</h3>
            <p class="desc">{{ module.description }}</p>
          </div>
        </div>
      </div>

      <!-- 成就卡片作为最后一个菜单项 -->
      <div 
        class="nav-item icon-purple" 
        :class="{ active: currentPath === '/my-achievements' }"
        @click="handleModuleClick('/my-achievements')"
      >
        <div class="nav-item-bg"></div>
        <div class="nav-item-content">
          <div class="icon-box">
            <i class="el-icon-medal"></i>
          </div>
          <div class="text-box">
            <h3 class="title">我的成就</h3>
            <p class="desc">查看徽章和成绩</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavMenu',
  props: {
    mode: {
      type: String,
      default: 'center' // 'center' or 'sidebar'
    }
  },
  data() {
    return {
      modules: [
        {
          id: 'pre-explore',
          title: '课前探索',
          description: '复习旧知识，情景导入',
          icon: 'el-icon-light-rain',
          color: 'icon-yellow',
          path: '/pre-explore'
        },
        {
          id: 'new-learning',
          title: '新知学习',
          description: '地球钟表动画演示',
          icon: 'el-icon-reading',
          color: 'icon-blue',
          path: '/new-learning'
        },
        {
          id: 'time-conversion',
          title: '时间转换',
          description: '12时/24时计时法转换',
          icon: 'el-icon-refresh',
          color: 'icon-blue',
          path: '/time-conversion'
        },
        {
          id: 'life-application',
          title: '生活应用',
          description: '场景练习与应用',
          icon: 'el-icon-time',
          color: 'icon-green',
          path: '/life-application'
        },
        {
          id: 'challenge',
          title: '成就挑战',
          description: '综合测验排行榜',
          icon: 'el-icon-trophy',
          color: 'icon-purple',
          path: '/challenge'
        }
      ]
    }
  },
  computed: {
    currentPath() {
      return this.$route.path
    }
  },
  methods: {
    handleModuleClick(path) {
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
    }
  }
}
</script>

<style scoped>
.nav-menu {
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
  z-index: 100;
}

/* ---------------- 中心模式 (首页) ---------------- */
.nav-menu.center {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: transparent;
  pointer-events: none; /* 让底部内容可点击(如果有) */
}

.nav-menu.center .nav-content {
  pointer-events: auto;
  width: 100%;
  max-width: 1000px;
  height: 500px;
  display: flex;
  gap: 10px;
}

.nav-menu.center .nav-item {
  flex: 1;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: flex 0.5s ease, transform 0.3s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* 手风琴悬停效果 */
.nav-menu.center .nav-item:hover {
  flex: 3; /* 悬停时变宽 */
}

.nav-menu.center .nav-item-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: transform 0.5s ease;
}

.nav-menu.center .nav-item-content {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  color: white;
  text-align: center;
  background: rgba(0, 0, 0, 0.1); /* 遮罩 */
  backdrop-filter: blur(0px);
  transition: all 0.5s ease;
}

.nav-menu.center .nav-item:hover .nav-item-content {
  background: rgba(0, 0, 0, 0);
}

.nav-menu.center .icon-box {
  font-size: 40px;
  margin-bottom: 20px;
  transition: transform 0.5s ease;
}

.nav-menu.center .nav-item:hover .icon-box {
  transform: scale(1.2);
}

.nav-menu.center .title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  white-space: nowrap;
}

.nav-menu.center .desc {
  font-size: 14px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
  max-width: 200px;
}

.nav-menu.center .nav-item:hover .desc {
  opacity: 1;
  transform: translateY(0);
}

/* ---------------- 侧边栏模式 (内页) ---------------- */
.nav-menu.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 260px;
  height: 100vh;
  background: white;
  box-shadow: 4px 0 20px rgba(0,0,0,0.05);
  padding: 20px 10px;
  overflow-y: auto;
}

.nav-menu.sidebar .nav-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: auto;
}

.nav-menu.sidebar .nav-item {
  height: 80px; /* 默认高度 */
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.nav-menu.sidebar .nav-item:hover,
.nav-menu.sidebar .nav-item.active {
  height: 140px; /* 展开高度 */
}

.nav-menu.sidebar .nav-item-content {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: row; /* 侧边栏图标和文字横排? 或者保持竖排看设计 */
  align-items: center;
  padding: 15px;
  color: white;
}

/* 侧边栏内容布局 */
.nav-menu.sidebar .icon-box {
  font-size: 24px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  margin-right: 15px;
  flex-shrink: 0;
}

.nav-menu.sidebar .text-box {
  flex: 1;
  overflow: hidden;
}

.nav-menu.sidebar .title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}

.nav-menu.sidebar .desc {
  font-size: 12px;
  opacity: 0.8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: none; /* 默认不显示描述 */
}

.nav-menu.sidebar .nav-item:hover .desc,
.nav-menu.sidebar .nav-item.active .desc {
  display: block; /* 展开时显示描述 */
  animation: fadeIn 0.3s ease;
}

/* 颜色定义 */
.icon-yellow { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
.icon-blue { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); }
.icon-green { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); } /* 修正为更鲜艳的 */
.icon-purple { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }

/* 覆盖一些颜色以匹配原设计 */
.icon-yellow { background: linear-gradient(135deg, #ffd700 0%, #ffb347 100%); }
.icon-blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.icon-green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.icon-purple { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
