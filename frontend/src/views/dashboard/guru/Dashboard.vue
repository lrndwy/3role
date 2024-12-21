<template>
  <TransitionWrapper>
    <div class="p-8">
      <h1 class="text-3xl font-bold text-text-light-primary dark:text-text-dark-primary">
        Dashboard Guru
      </h1>
      <div class="mt-8">
        <div class="bg-background-light dark:bg-background-dark p-8 rounded-lg shadow-soft border border-border-light dark:border-border-dark">
          <h2 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary">
            Selamat Datang, {{ user?.username }}
          </h2>
          <p class="mt-2 text-text-light-secondary dark:text-text-dark-secondary">
            Role: Guru
          </p>
        </div>
        <!-- Tambahkan konten dashboard guru di sini -->
      </div>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import TransitionWrapper from '@/components/TransitionWrapper.vue'

const store = useStore()
const user = computed(() => store.state.user)
</script>
