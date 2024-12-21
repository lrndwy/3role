<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="space-y-4">
      <!-- Foto Upload -->
      <div>
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Foto <span class="text-red-500">*</span>
        </label>
        <input 
          type="file"
          @change="handleFileChange"
          accept="image/*"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>

      <!-- Judul -->
      <div>
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Judul <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.judul"
          type="text"
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>

      <!-- Deskripsi -->
      <div>
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Deskripsi <span class="text-red-500">*</span>
        </label>
        <textarea 
          v-model="formData.deskripsi"
          required
          rows="4"
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        ></textarea>
      </div>

      <!-- Tanggal -->
      <div>
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Tanggal <span class="text-red-500">*</span>
        </label>
        <input 
          v-model="formData.tanggal"
          type="date"
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
      </div>

      <!-- Kategori -->
      <div>
        <label class="block text-sm font-medium mb-2 text-text-light-primary dark:text-text-dark-primary">
          Kategori <span class="text-red-500">*</span>
        </label>
        <select 
          v-model="formData.kategori"
          required
          class="w-full px-4 py-2.5 bg-white dark:bg-surface-dark border border-border-light dark:border-border-dark rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 transition-all duration-200"
        >
          <option value="kegiatan">Kegiatan</option>
          <option value="prestasi">Prestasi</option>
          <option value="fasilitas">Fasilitas</option>
          <option value="lainnya">Lainnya</option>
        </select>
      </div>
    </div>

    <!-- Buttons -->
    <div class="flex justify-end space-x-2">
      <FwbButton
        type="button"
        color="dark"
        @click="$emit('cancel')"
        class="px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        Batal
      </FwbButton>
      <FwbButton
        type="submit"
        color="dark"
        class="px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        {{ galeri ? 'Update' : 'Simpan' }}
      </FwbButton>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FwbButton } from 'flowbite-vue'

const props = defineProps({
  galeri: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formData = ref({
  foto: null,
  judul: '',
  deskripsi: '',
  tanggal: '',
  kategori: 'kegiatan'
})

const handleFileChange = (event) => {
  formData.value.foto = event.target.files[0]
}

onMounted(() => {
  if (props.galeri) {
    formData.value = { ...props.galeri }
  }
})

const handleSubmit = () => {
  const submitData = new FormData()
  
  if (formData.value.foto instanceof File) {
    submitData.append('foto', formData.value.foto)
  }
  
  submitData.append('judul', formData.value.judul)
  submitData.append('deskripsi', formData.value.deskripsi)
  submitData.append('tanggal', formData.value.tanggal)
  submitData.append('kategori', formData.value.kategori)
  
  emit('submit', submitData)
}
</script> 