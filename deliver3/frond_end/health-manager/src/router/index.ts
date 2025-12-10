import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import AccountView from '../views/AccountView.vue'
import AppointmentsView from '../views/AppointmentsView.vue'
import ChallengesView from '../views/ChallengesView.vue'
import FamilyView from '../views/FamilyView.vue'
import InvitationsView from '../views/InvitationsView.vue'
import DelegationView from '../views/DelegationView.vue'
import ReportsView from '../views/ReportsView.vue'
import MetricsView from '../views/MetricsView.vue'

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
  },
  {
    path: '/family',
    name: 'family',
    component: FamilyView,
    meta: { requiresAuth: true }
  },
  {
    path: '/invitations',
    name: 'invitations',
    component: InvitationsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/delegation',
    name: 'delegation',
    component: DelegationView,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'reports',
    component: ReportsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/metrics',
    name: 'metrics',
    component: MetricsView,
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
