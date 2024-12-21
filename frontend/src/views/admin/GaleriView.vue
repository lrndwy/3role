<template>
  <div class="p-4">
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-semibold text-text-light-primary dark:text-text-dark-primary">
        Manajemen Galeri
      </h1>
      <FwbButton
        color="dark"
        @click="showModal = true"
        class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
      >
        <PlusIcon class="w-5 h-5" />
        Tambah Galeri
      </FwbButton>
    </div>

    <!-- Table -->
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
      <table class="w-full text-sm text-left text-text-light-primary dark:text-text-dark-primary">
        <thead class="text-xs uppercase bg-background-light dark:bg-background-dark">
          <tr>
            <th scope="col" class="px-6 py-3">Foto</th>
            <th scope="col" class="px-6 py-3">Judul</th>
            <th scope="col" class="px-6 py-3">Kategori</th>
            <th scope="col" class="px-6 py-3">Tanggal</th>
            <th scope="col" class="px-6 py-3">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in galeriItems" :key="item.id" class="bg-white dark:bg-surface-dark border-b border-border-light dark:border-border-dark">
            <td class="px-6 py-4">
              <img :src="item.foto" alt="Foto" class="w-20 h-20 object-cover rounded">
            </td>
            <td class="px-6 py-4">{{ item.judul }}</td>
            <td class="px-6 py-4">{{ item.kategori }}</td>
            <td class="px-6 py-4">{{ formatDate(item.tanggal) }}</td>
            <td class="px-6 py-4">
              <div class="flex space-x-2">
                <button @click="editItem(item)" class="text-blue-600 hover:text-blue-900 dark:hover:text-blue-400">
                  <PencilIcon class="w-5 h-5" />
                </button>
                <button @click="deleteItem(item.id)" class="text-red-600 hover:text-red-900 dark:hover:text-red-400">
                  <TrashIcon class="w-5 h-5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <BaseModal v-model="showModal">
      <template #header>
        {{ selectedItem ? 'Edit Galeri' : 'Tambah Galeri' }}
      </template>
      
      <template #body>
        <GaleriForm 
          :galeri="selectedItem"
          @submit="handleSubmit"
          @cancel="closeModal"
        />
      </template>
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FwbButton } from 'flowbite-vue'
import { PlusIcon, PencilIcon, TrashIcon, PhotoIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import GaleriForm from '@/components/form/GaleriForm.vue'
import api from '@/config/api'
import { useNotifications } from '@/composables/useNotifications'

const { notify } = useNotifications()
const showModal = ref(false)
const selectedItem = ref(null)
const galeriItems = ref([])

const fetchGaleri = async () => {
  try {
    const response = await api.get('/galeri/')
    galeriItems.value = response.data
  } catch (error) {
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal mengambil data galeri'
    })
  }
}

const handleSubmit = async (formData) => {
  try {
    if (selectedItem.value) {
      await api.put(`/galeri/${selectedItem.value.id}/`, formData)
      notify({
        type: 'success',
        title: 'Sukses',
        message: 'Berhasil mengupdate galeri'
      })
    } else {
      await api.post('/galeri/', formData)
      notify({
        type: 'success',
        title: 'Sukses',
        message: 'Berhasil menambah galeri'
      })
    }
    closeModal()
    fetchGaleri()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Error',
      message: 'Gagal menyimpan data'
    })
  }
}

const editItem = (item) => {
  selectedItem.value = item
  showModal.value = true
}

const deleteItem = async (id) => {
  if (confirm('Apakah Anda yakin ingin menghapus item ini?')) {
    try {
      await api.delete(`/galeri/${id}/`)
      notify({
        type: 'success',
        title: 'Sukses',
        message: 'Berhasil menghapus galeri'
      })
      fetchGaleri()
    } catch (error) {
      notify({
        type: 'error',
        title: 'Error',
        message: 'Gagal menghapus data'
      })
    }
  }
}

const closeModal = () => {
  showModal.value = false
  selectedItem.value = null
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('id-ID')
}

onMounted(() => {
  fetchGaleri()
})
</script> 