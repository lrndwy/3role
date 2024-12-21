<template>
  <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto space-y-6">
    <div class="flex flex-wrap gap-6 text-left">
      <!-- User Field -->
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

      <!-- Nama Karyawan Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Nama Karyawan <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.nama_karyawan"
          type="text"
          required
          placeholder="Masukkan nama karyawan"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>

      <!-- Jabatan Field -->
      <div class="w-full">
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Jabatan <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.jabatan"
          type="text"
          required
          placeholder="Masukkan jabatan"
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
        {{ karyawan ? 'Update' : 'Simpan' }}
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { FwbButton } from 'flowbite-vue'
import api from '@/config/api'
import { useNotifications } from '@/composables/useNotifications'

const props = defineProps({
  karyawan: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])
const users = ref([])

const formData = ref({
  user: '',
  nama_karyawan: '',
  jabatan: ''
})

// Filter users berdasarkan role karyawan
const filteredUsers = computed(() => {
  return users.value.filter(user => user.role === 'karyawan')
})

const { notify } = useNotifications()

const fetchUsers = async () => {
  try {
    const response = await api.get('/available-users/?role=karyawan')
    users.value = response.data
    
    if (props.karyawan) {
      const currentUserResponse = await api.get(`/users/${props.karyawan.user}/`)
      if (!users.value.find(u => u.id === props.karyawan.user)) {
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
  
  if (props.karyawan) {
    formData.value = {
      user: props.karyawan.user,
      nama_karyawan: props.karyawan.nama_karyawan,
      jabatan: props.karyawan.jabatan
    }
  }
})

const handleSubmit = () => {
  // Validasi form
  if (!formData.value.user || !formData.value.nama_karyawan || !formData.value.jabatan) {
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
