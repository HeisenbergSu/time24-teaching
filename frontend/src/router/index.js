import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import TeacherDashboard from '../views/TeacherDashboard.vue'
import PreExplore from '../views/PreExplore.vue'
import NewLearning from '../views/NewLearning.vue'
import LifeApplication from '../views/LifeApplication.vue'
import Challenge from '../views/Challenge.vue'
import MyAchievements from '../views/MyAchievements.vue'
import TimeConversion from '../views/TimeConversion.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/teacher',
    name: 'TeacherDashboard',
    component: TeacherDashboard
  },
  {
    path: '/pre-explore',
    name: 'PreExplore',
    component: PreExplore
  },
  {
    path: '/new-learning',
    name: 'NewLearning',
    component: NewLearning
  },
  {
    path: '/life-application',
    name: 'LifeApplication',
    component: LifeApplication
  },
  {
    path: '/challenge',
    name: 'Challenge',
    component: Challenge
  },
  {
    path: '/my-achievements',
    name: 'MyAchievements',
    component: MyAchievements
  },
  {
    path: '/time-conversion',
    name: 'TimeConversion',
    component: TimeConversion
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
