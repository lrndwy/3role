import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import AdminDashboard from '../views/dashboard/admin/Dashboard.vue'
import KaryawanDashboard from '../views/dashboard/karyawan/Dashboard.vue'
import GuruDashboard from '../views/dashboard/guru/Dashboard.vue'
import SiswaDashboard from '../views/dashboard/siswa/Dashboard.vue'
import AdminDashboard_Users from '../views/dashboard/admin/Users.vue'
import AdminDashboard_Guru from '../views/dashboard/admin/Guru.vue'
import AdminDashboard_Karyawan from '../views/dashboard/admin/Karyawan.vue'
import AdminDashboard_Siswa from '../views/dashboard/admin/Siswa.vue'
import Profile from '../views/profile/Profile.vue'
import GaleriView from '@/views/admin/GaleriView.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/admin/users',
    name: 'AdminDashboard_Users',
    component: AdminDashboard_Users,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/karyawan',
    name: 'KaryawanDashboard',
    component: KaryawanDashboard,
    meta: { requiresAuth: true, role: 'karyawan' }
  },
  {
    path: '/dashboard/guru',
    name: 'GuruDashboard',
    component: GuruDashboard,
    meta: { requiresAuth: true, role: 'guru' }
  },
  {
    path: '/dashboard/siswa',
    name: 'SiswaDashboard',
    component: SiswaDashboard,
    meta: { requiresAuth: true, role: 'siswa' }
  },
  {
    path: '/dashboard/admin/guru',
    name: 'AdminDashboard_Guru',
    component: AdminDashboard_Guru,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/admin/karyawan',
    name: 'AdminDashboard_Karyawan',
    component: AdminDashboard_Karyawan,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/admin/siswa',
    name: 'AdminDashboard_Siswa',
    component: AdminDashboard_Siswa,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/admin/galeri',
    name: 'admin-galeri',
    component: GaleriView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  // Redirect dari login page jika sudah terotentikasi
  if (to.path === '/login' && token) {
    next('/dashboard/' + userRole)
    return
  }

  // Cek authentication untuk protected routes
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    next('/dashboard/' + userRole)
  } else {
    next()
  }
})

export default router
