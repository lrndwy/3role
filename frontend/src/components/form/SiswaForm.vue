<template>
  <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
    <div class="flex flex-wrap gap-6 text-left">
      <!-- User Selection Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          User <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.user" 
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="">Pilih User</option>
          <option v-for="user in filteredUsers" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
      </div>

      <!-- Nama Siswa Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Nama Siswa <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.nama_siswa" 
          type="text" 
          required
          placeholder="Masukkan nama siswa"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>

      <!-- Kelas Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Kelas <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.kelas" 
          type="text" 
          required
          placeholder="Masukkan kelas"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-2 pt-6 border-t border-border-light dark:border-border-dark">
      <FwbButton 
        type="button"
        color="dark"
        class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
        @click="$emit('cancel')"
      >
        Batal
      </FwbButton>
      <FwbButton 
        type="submit"
        color="dark"
        class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        {{ siswa ? 'Update' : 'Simpan' }}
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { FwbButton } from 'flowbite-vue'
import api from '@/config/api'
import { useNotifications } from '@/composables/useNotifications'

const { notify } = useNotifications()

const props = defineProps({
  siswa: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])
const users = ref([])

const formData = ref({
  user: '',
  nama_siswa: '',
  kelas: ''
})

// Filter users berdasarkan role siswa
const filteredUsers = computed(() => {
  return users.value.filter(user => user.role === 'siswa')
})

const fetchUsers = async () => {
  try {
    const response = await api.get('/available-users/?role=siswa')
    users.value = response.data
    
    if (props.siswa) {
      const currentUserResponse = await api.get(`/users/${props.siswa.user}`)
      if (!users.value.find(u => u.id === props.siswa.user)) {
        users.value.push(currentUserResponse.data)
      }
    }
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data users'
    })
    console.error('Error fetching users:', error)
  }
}

onMounted(async () => {
  await fetchUsers()
  
  if (props.siswa) {
    formData.value = {
      user: props.siswa.user,
      nama_siswa: props.siswa.nama_siswa,
      kelas: props.siswa.kelas
    }
  }
})

const handleSubmit = () => {
  if (!formData.value.user || !formData.value.nama_siswa || !formData.value.kelas) {
    notify({
      type: 'warning',
      title: 'Peringatan',
      message: 'Semua field harus diisi'
    })
    return
  }
  emit('submit', formData.value)
}
</script>
