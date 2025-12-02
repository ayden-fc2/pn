import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import AccountView from '../views/AccountView.vue'
import AppointmentsView from '../views/AppointmentsView.vue'
import ChallengesView from '../views/ChallengesView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/account',
    name: 'account',
    component: AccountView,
    meta: { requiresAuth: true }
  },
  {
    path: '/appointments',
    name: 'appointments',
    component: AppointmentsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/challenges',
    name: 'challenges',
    component: ChallengesView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (!authStore.isAuthenticated && to.name !== 'login') {
    await authStore.checkAuth()
    if (!authStore.isAuthenticated) {
      next({ name: 'login' })
      return
    }
  }
  
  if (authStore.isAuthenticated && to.name === 'login') {
    next({ name: 'dashboard' })
    return
  }

  next()
})

export default router
