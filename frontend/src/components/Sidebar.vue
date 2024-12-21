<template>
  <BaseModal v-model="showLogoutModal">
    <template #header>
      Konfirmasi Logout
    </template>
    
    <template #body>
      <p>Apakah Anda yakin ingin keluar dari aplikasi?</p>
    </template>
    
    <template #footer>
      <button
        @click="showLogoutModal = false"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        Batal
      </button>
      <button
        @click="confirmLogout"
        class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        Ya, Logout
      </button>
    </template>
  </BaseModal>

  <div 
    class="fixed left-0 z-40 w-64 pt-5 bg-background-light dark:bg-surface-dark transform transition-transform duration-150 ease-in-out lg:translate-x-0 top-0 h-screen overflow-y-auto flex flex-col justify-between"
    :class="[isOpen ? 'translate-x-0' : '-translate-x-full']"
  >
    <nav class="mt-2 px-3 lg:px-4 space-y-1">
      <div class="flex p-2 gap-2 items-center mb-2">
        <img src="../assets/logo.svg" alt="Logo" class="w-8 h-8">
        <div class="flex flex-col ml-2">
          <span class="text-black dark:text-text-dark-primary rounded-md text-md font-bold truncate max-w-[200px] lg:max-w-none">
            Hexanest.id
          </span>
          <p class="text-xs text-gray-500 dark:text-text-dark-secondary">
            Hexanest.id
          </p>
        </div>
      </div>
      <div class="border-t border-gray-400 pb-2"></div>
      <!-- Menu items dengan padding yang disesuaikan -->
      <router-link 
        :to="`/dashboard/${userRole}`"
        :class="[
          $route.path === `/dashboard/${userRole}`
            ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
            : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
          'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
        ]"
        @click="closeSidebarOnMobile"
      >
        <component 
          :is="DashboardIcon"
          :class="[
            $route.path === `/dashboard/${userRole}`
              ? 'text-secondary-700 dark:text-white'
              : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
            'mr-3 h-6 w-6'
          ]"
          aria-hidden="true"
        />
        Dashboard
      </router-link>

      <!-- Menu Admin -->
      <template v-if="userRole === 'admin'">
        <!-- Users Dropdown Menu -->
        <div class="relative">
          <button 
            @click="toggleUsersMenu"
            :class="[
              isAnyUserMenuActive
                ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
                : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
              'group flex items-center justify-between w-full px-2 py-2 text-sm font-medium rounded-md'
            ]"
          >
            <div class="flex items-center">
              <UserIcon 
                :class="[
                  isAnyUserMenuActive
                    ? 'text-secondary-700 dark:text-white'
                    : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
                  'mr-3 h-6 w-6'
                ]"
              />
              <span>Users</span>
            </div>
            <ChevronRightIcon 
              :class="[
                'w-5 h-5 transition-transform duration-200',
                isUsersMenuOpen ? 'transform rotate-90' : ''
              ]"
            />
          </button>

          <!-- Dropdown Content -->
          <div 
            v-show="isUsersMenuOpen"
            class="mt-1 ml-4 space-y-1 overflow-hidden transition-all duration-200 ease-in-out"
          >
            <router-link 
              v-for="menu in adminMenus"
              :key="menu.path"
              :to="menu.path"
              :class="[
                $route.path === menu.path
                  ? 'bg-secondary-100 dark:bg-background-dark text-secondary-900 dark:text-white'
                  : 'text-secondary-600 dark:text-gray-300 hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-secondary-900 dark:hover:text-white',
                'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
              ]"
              @click="closeSidebarOnMobile"
            >
              <component 
                :is="menu.icon"
                :class="[
                  $route.path === menu.path
                    ? 'text-secondary-700 dark:text-white'
                    : 'text-gray-400 group-hover:text-secondary-700 dark:group-hover:text-white',
                  'mr-3 h-6 w-6'
                ]"
                aria-hidden="true"
              />
              {{ menu.name }}
            </router-link>
          </div>
        </div>
      </template>

      <!-- Tambahkan menu profil -->

      
    </nav>

    

    <!-- Logout section -->
    <div class="p-6 mb-4">
      <router-link 
        to="/profile"
        :class="[
          $route.path === '/profile'
            ? 'bg-secondary-100 dark:bg-background-dark text-text-light-primary dark:text-text-dark-primary'
            : 'text-text-light-secondary dark:text-text-dark-secondary hover:bg-secondary-50 dark:hover:bg-background-dark hover:text-text-light-primary dark:hover:text-text-dark-primary',
          'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
        ]"
        @click="closeSidebarOnMobile"
      >
        <img 
          :src="userData.foto_profil_url || '/user-profile.jpg'"
          :alt="userData.username"
          @error="e => e.target.src = '/user-profile.jpg'"
          class="w-8 h-8 rounded-full mr-3 object-cover"
        />
        <div class="flex flex-col">
          <span class="text-text-light-primary dark:text-text-dark-primary">{{ userData.username }}</span>
          <span class="text-text-light-secondary dark:text-text-dark-secondary">{{ userData.email }}</span>
        </div>
      </router-link>
      <div class="border-t border-gray-400 pb-2 mt-4"></div>
      <button
        @click="showLogoutModal = true"
        class="mt-2 w-full flex items-center justify-between px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 hover:text-gray-900 dark:hover:text-white bg-white dark:bg-surface-dark hover:bg-gray-100 dark:hover:bg-background-dark rounded-md shadow-sm group"
      >
        <div class="flex items-center">
          <ArrowRightOnRectangleIcon class="w-5 h-5 mr-2 text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300" />
          <span>Logout</span>
        </div>
        <ChevronRightIcon class="w-4 h-4 text-gray-400 dark:text-gray-500 group-hover:text-gray-600 dark:group-hover:text-gray-300" />
      </button>
    </div>
  </div>

  <!-- Overlay untuk mobile -->
  <div 
    v-if="isOpen" 
    class="fixed inset-0 bg-gray-600 bg-opacity-50 transition-opacity lg:hidden z-30" 
    @click="$emit('close-sidebar')"
  ></div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import BaseModal from './BaseModal.vue'
import {
  UserIcon,
  AcademicCapIcon,
  UserGroupIcon,
  BuildingOfficeIcon,
  HomeIcon as DashboardIcon,
  ArrowRightOnRectangleIcon,
  ChevronRightIcon,
  PhotoIcon
} from '@heroicons/vue/24/outline'
import api from '@/config/api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

// Inisialisasi formData dengan nilai default yang valid
const formData = ref({
  foto_profil: '/user-profile.jpg',
  nama_pengguna: 'Guest'
})



const emit = defineEmits(['close-sidebar'])

const store = useStore()
const userRole = computed(() => store.getters.userRole)

const adminMenus = [
  {
    name: 'Manajemen User',
    path: '/dashboard/admin/users',
    icon: UserIcon
  },
  {
    name: 'Guru',
    path: '/dashboard/admin/guru',
    icon: AcademicCapIcon
  },
  {
    name: 'Siswa',
    path: '/dashboard/admin/siswa',
    icon: UserGroupIcon
  },
  {
    name: 'Karyawan',
    path: '/dashboard/admin/karyawan',
    icon: BuildingOfficeIcon
  },
  {
    name: 'Galeri',
    path: '/dashboard/admin/galeri',
    icon: PhotoIcon
  }
]

// Tambahkan fungsi untuk menutup sidebar di mobile
const closeSidebarOnMobile = () => {
  if (window.innerWidth < 1024) { // 1024px adalah breakpoint untuk lg di Tailwind
    emit('close-sidebar')
  }
}

const router = useRouter()

// Tambahkan state untuk modal
const showLogoutModal = ref(false)

const handleLogout = async () => {
  try {
    await store.dispatch('logout')
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// Tambahkan fungsi confirmLogout
const confirmLogout = async () => {
  await handleLogout()
  showLogoutModal.value = false
}

// Tambahkan state untuk user data
const userData = ref({
  username: '',
  foto_profil_url: '/user-profile.jpg',
  email: ''
})

// Tambahkan fungsi untuk mengambil data profil
const fetchUserProfile = async () => {
  try {
    const response = await api.get('/user/profile/')
    userData.value = response.data
  } catch (error) {
    console.error('Error fetching user profile:', error)
  }
}

// Panggil fetchUserProfile saat komponen di-mount
onMounted(() => {
  fetchUserProfile()
})

const isUsersMenuOpen = ref(false)

const toggleUsersMenu = () => {
  isUsersMenuOpen.value = !isUsersMenuOpen.value
}

const isAnyUserMenuActive = computed(() => {
  return adminMenus.some(menu => menu.path === router.currentRoute.value.path)
})

</script>
