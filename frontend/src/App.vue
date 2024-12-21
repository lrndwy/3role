<template>
  <div class="min-h-screen bg-background-light dark:bg-surface-dark text-text-light-primary dark:text-text-dark-primary overflow-hidden">
    <div v-if="isAuthenticated">
      <div class="flex items-center justify-center">
        <Sidebar 
          :is-open="isSidebarOpen" 
          @close-sidebar="closeSidebar"
        />
        
        <div class="flex-1 lg:ml-64 lg:p-5 flex items-start lg:items-center min-h-screen">
          <main class="rounded-2xl lg:bg-white dark:lg:bg-background-dark lg:h-[calc(100vh-40px)] relative lg:shadow-lg lg:border-gray-200 dark:lg:border-border-dark lg:border-[0.5px] w-full h-screen sm:bg-gray-100 sm:shadow-none shadow-none bg-gray-100 dark:bg-surface-dark overflow-hidden">
            <Navbar @toggle-sidebar="toggleSidebar"/>
            <div class="overflow-y-auto h-[calc(100%-64px)]">
              <RouterView />
            </div>
          </main>
        </div>
      </div>
    </div>
    <div v-else>
      <RouterView />
    </div>
    <Notifications ref="notificationsRef" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, provide } from 'vue'
import { useStore } from 'vuex'
import { RouterView } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Navbar from '@/components/Navbar.vue'
import Notifications from '@/components/Notifications.vue'

const store = useStore()
const isAuthenticated = computed(() => store.getters.isAuthenticated)
const isSidebarOpen = ref(false)
const notificationsRef = ref(null)

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const closeSidebar = () => {
  isSidebarOpen.value = false
}

provide('notifications', {
  addNotification: (...args) => notificationsRef.value?.addNotification(...args)
})

onMounted(() => {
  store.dispatch('initializeTheme')
})
</script>


