<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <form @submit.prevent="handleLogin" class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
      
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2">Username</label>
        <input 
          v-model="credentials.username" 
          type="text" 
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
      </div>
      
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2">Password</label>
        <input 
          v-model="credentials.password" 
          type="password" 
          required
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
        >
      </div>
      
      <FwbButton 
        type="submit"
        color="green"
        class="w-full"
      >
        Login
      </FwbButton>
      
      <p v-if="error" class="mt-4 text-red-500 text-center">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { FwbButton } from 'flowbite-vue'

const store = useStore()
const router = useRouter()

const credentials = ref({
  username: '',
  password: ''
})

const error = ref('')

const handleLogin = async () => {
  try {
    const response = await store.dispatch('login', credentials.value)
    if (response && response.role) {
      router.push(`/dashboard/${response.role}`)
    } else {
      error.value = 'Invalid user data received'
    }
  } catch (err) {
    error.value = 'Username atau password salah'
  }
}
</script>
