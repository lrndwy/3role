<template>
  <TransitionWrapper>
    <div class="p-8">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Admin Dashboard
      </h1>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- Card Total User -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total User</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_users }}</template>
              </h3>
            </div>
            <div class="bg-primary-100 dark:bg-primary-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-primary-500 dark:text-primary-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Card Total Guru -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total Guru</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_guru }}</template>
              </h3>
            </div>
            <div class="bg-success-100 dark:bg-success-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-success-500 dark:text-success-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Card Total Siswa -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total Siswa</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_siswa }}</template>
              </h3>
            </div>
            <div class="bg-accent-100 dark:bg-accent-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-accent-500 dark:text-accent-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Card Total Karyawan -->
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-4 sm:p-6 border border-border-light dark:border-border-dark">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-text-light-secondary dark:text-text-dark-secondary text-sm">Total Karyawan</p>
              <h3 class="text-text-light-primary dark:text-text-dark-primary text-2xl font-bold">
                <SkeletonLoader v-if="loading" width="60px" height="30px" />
                <template v-else>{{ stats.total_karyawan }}</template>
              </h3>
            </div>
            <div class="bg-secondary-100 dark:bg-secondary-900/30 p-3 rounded-full">
              <svg class="w-6 h-6 text-secondary-500 dark:text-secondary-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Aktivitas Terbaru -->
      <div class="mt-6 sm:mt-8 grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-6 border border-border-light dark:border-border-dark">
          <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary">Statistik User</h2>
          <div class="h-64 bg-surface-light dark:bg-background-dark rounded flex items-center justify-center">
            <SkeletonLoader v-if="loading" width="300px" height="200px" />
            <p v-else class="text-gray-500">Grafik Statistik User</p>
          </div>
        </div>

        <div class="bg-background-light dark:bg-background-dark rounded-lg shadow-soft p-6 border border-border-light dark:border-border-dark">
          <h2 class="text-xl font-semibold mb-4 text-text-light-primary dark:text-text-dark-primary">Aktivitas Terbaru</h2>
          <div class="space-y-4 max-h-[400px] overflow-y-auto">
            <template v-if="loading">
              <div v-for="n in 2" :key="n" class="flex items-center p-4 bg-gray-50 dark:bg-surface-dark rounded">
                <SkeletonLoader class="mr-4" width="40px" height="40px" circle />
                <div class="flex-1">
                  <SkeletonLoader class="mb-2" width="200px" />
                  <SkeletonLoader width="150px" />
                </div>
              </div>
            </template>
            <template v-else>
              <div v-for="activity in stats.latest_activities" :key="activity.id" class="flex items-center p-4 bg-surface-light dark:bg-surface-dark rounded mb-4">
                <div class="bg-primary-100 dark:bg-primary-900/30 p-2 rounded-full mr-4">
                  <svg class="w-4 h-4 text-primary-500 dark:text-primary-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p class="font-medium text-text-light-primary dark:text-text-dark-primary">
                    {{ activity.message }}
                  </p>
                  <p class="text-sm text-text-light-secondary dark:text-text-dark-secondary">
                    {{ activity.time }}
                  </p>
                </div>
              </div>
              <div v-if="stats.latest_activities.length === 0" class="text-center text-gray-500 py-4">
                Tidak ada aktivitas
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/config/api'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()
const loading = ref(true)
const stats = ref({
  total_users: 0,
  total_guru: 0,
  total_siswa: 0,
  total_karyawan: 0,
  latest_activities: []
})

const fetchStats = async () => {
  // Cek apakah masih ada token sebelum fetch
  const token = localStorage.getItem('token')
  if (!token) {
    return
  }
  
  try {
    const response = await api.get('/dashboard/stats/')
    stats.value = response.data
  } catch (error) {
    // Jika mendapat error 401, berarti token tidak valid/expired
    if (error.response?.status === 401) {
      store.dispatch('logout')
    } else {
      console.error('Error fetching stats:', error)
    }
  } finally {
    loading.value = false
  }
}

// Tambahkan watch untuk route
watch(
  () => router.currentRoute.value.path,
  (newPath) => {
    // Hanya fetch stats jika berada di halaman dashboard admin
    if (newPath === '/dashboard/admin') {
      fetchStats()
    }
  }
)

onMounted(() => {
  if (router.currentRoute.value.path === '/dashboard/admin') {
    fetchStats()
  }
})
</script>
