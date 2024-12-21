<template>
  <div class="max-w-3xl mx-auto space-y-6 p-10">
    <h2 class="text-xl font-semibold text-text-light-primary dark:text-text-dark-primary">
      Edit Profil
    </h2>
    <TransitionWrapper>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div v-if="formData.foto_profil" class="w-full">
          <img :src="formData.foto_profil || '/user-profile.jpg'" alt="Foto Profil" class="w-32 h-32 rounded-full border border-border-light dark:border-border-dark object-cover" @error="e => e.target.src = '/user-profile.jpg'">
        </div>
        <!-- Username Field -->
        <div class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Username <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.username" 
            type="text" 
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Email Field -->
        <div class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Email <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.email" 
            type="email" 
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Toggle for Foto Profil -->
        <div class="w-full">
          <Toggle v-model="formData.changeFotoProfil">
            Ubah Foto Profil
          </Toggle>
        </div>

        <!-- Foto Profil Field -->
        <div v-if="formData.changeFotoProfil" class="w-full">
          <label class="block mb-2 text-sm font-medium text-text-light-primary dark:text-text-dark-primary" for="file_input">
            Foto Profil Baru
          </label>
          <input 
            id="file_input"
            type="file" 
            @change="handleFileUpload"
            class="block w-full text-sm text-text-light-primary border border-border-light rounded-lg cursor-pointer bg-surface-light dark:text-text-dark-primary focus:outline-none dark:bg-surface-dark dark:border-border-dark"
          >
        </div>

        <!-- Toggle for Password -->
        <div class="w-full">
          <Toggle v-model="formData.changePassword">
            Ubah Password
          </Toggle>
        </div>

        <!-- Password Field -->
        <div v-if="formData.changePassword" class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Password Baru
          </label>
          <input 
            v-model="formData.password" 
            type="password" 
            placeholder="Masukkan password baru"
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Nama Field -->
        <div v-if="formData.role !== 'admin'" class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Nama <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.nama" 
            type="text" 
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Role-specific Fields -->
        <div v-if="formData.role === 'guru'" class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Mata Pelajaran <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.nama_mapel" 
            type="text" 
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <div v-if="formData.role === 'siswa'" class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Kelas <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.kelas" 
            type="text" 
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <div v-if="formData.role === 'karyawan'" class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Jabatan <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.jabatan" 
            type="text" 
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Alamat Field -->
        <div class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Alamat <span class="text-red-500">*</span>
          </label>
          <textarea 
            v-model="formData.address"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          ></textarea>
        </div>

        <!-- Phone Field -->
        <div class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Nomor Telepon
          </label>
          <input 
            v-model="formData.phone" 
            type="text" 
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Tanggal Lahir Field -->
        <div class="w-full">
          <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
            Tanggal Lahir <span class="text-red-500">*</span>
          </label>
          <input 
            v-model="formData.tanggal_lahir"
            type="date"
            required
            class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
          >
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-2 pt-6 border-t border-border-light dark:border-border-dark">
          <FwbButton 
            type="submit"
            color="dark"
            class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
          >
            Simpan
          </FwbButton>
        </div>
      </form>
    </TransitionWrapper>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FwbButton } from 'flowbite-vue'
import api from '@/config/api'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import Toggle from '@/components/Toggle.vue'
import store from '@/store'

const formData = ref({
  username: '',
  email: '',
  password: '',
  nama: '',
  role: '',
  nama_mapel: '',
  kelas: '',
  jabatan: '',
  address: '',
  foto_profil: null,
  phone: '',
  tanggal_lahir: '',
  changeFotoProfil: false,
  changePassword: false
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  formData.value.foto_profil = file
}

const fetchUserProfile = async () => {
  try {
    const response = await api.get('/user/profile/')
    formData.value = response.data
    formData.value.foto_profil = response.data.foto_profil_url || '/user-profile.jpg'
  } catch (error) {
    console.error('Error fetching user profile:', error.response?.data || error)
  }
}

const handleSubmit = async () => {
  try {
    const formDataToSend = new FormData()
    for (const key in formData.value) {
      if (formData.value[key] !== null && !(formData.value.role === 'admin' && key === 'nama')) {
        if ((key === 'foto_profil' && formData.value.changeFotoProfil) || 
            (key === 'password' && formData.value.changePassword) || 
            (key !== 'foto_profil' && key !== 'password')) {
          formDataToSend.append(key, formData.value[key])
        }
      }
    }
    
    const response = await api.put('/user/profile/', formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    store.commit('setUser', {
      ...response.data,
      foto_profil_url: response.data.foto_profil_url
    })
    alert('Profil berhasil diperbarui')
  } catch (error) {
    console.error('Error updating profile:', error.response?.data || error)
  }
}

onMounted(() => {
  fetchUserProfile()
})
</script> 
