<template>
  <TransitionWrapper>
    <div class="p-8">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Siswa
      </h1>
      
      <div>
        <div class="flex flex-wrap items-center gap-2 mb-6">
          <div class="flex-1">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari nama siswa..."
              class="w-full px-4 py-2 border border-gray-200 dark:border-border-dark rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-surface-dark"
            />
          </div>
          
          <div class="relative" ref="filterDropdownRef">
            <fwb-tooltip>
              <template #trigger>
                <FwbButton color="dark" class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" @click="toggleFilterDropdown">
                  <FunnelIcon class="w-6 h-6" />
                </FwbButton>
              </template>
              <template #content>
                Filter
              </template>
            </fwb-tooltip>

            
            <Transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-200 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <div v-if="showFilterDropdown" 
                   class="absolute right-0 mt-2 w-72 bg-white dark:bg-surface-dark rounded-lg shadow-lg border border-gray-200 dark:border-border-dark p-4 z-50">
                <div class="space-y-4">
                  <div>
                    <div class="font-medium mb-2">Kelas</div>
                    <div class="space-y-2 flex flex-col">
                      <label v-for="kelas in kelasList" :key="kelas" class="block">
                        <Checkbox
                          v-model="selectedFilters.kelas"
                          :value="kelas"
                        >
                          {{ kelas }}
                        </Checkbox>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>
          </div>

          <fwb-tooltip>
            <template #trigger>
              <FwbButton color="dark" class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light" @click="showModal">
                <PlusIcon class="w-6 h-6" />
              </FwbButton>
            </template>
            <template #content>
              Tambah Siswa
            </template>
          </fwb-tooltip>
          
        </div>
        
        <div class="overflow-x-auto rounded-lg lg:border lg:border-gray-200 dark:border-border-dark">
          <div class="inline-block min-w-full align-middle">
            <!-- Tampilan desktop -->
            <table class="hidden md:table min-w-full divide-y divide-gray-200 dark:divide-border-dark">
              <thead class="bg-surface-light dark:bg-surface-dark">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Username
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Nama Siswa
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Kelas
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Aksi
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200 dark:divide-border-dark dark:bg-background-dark">
                <template v-if="loading">
                  <tr v-for="n in 5" :key="n" class="hover:bg-gray-50 dark:hover:bg-surface-dark">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="150px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="150px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="80px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="120px" />
                    </td>
                  </tr>
                </template>
                <template v-else>
                  <tr v-for="siswa in paginatedSiswa" :key="siswa.id" 
                      class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                      @click="showSiswaDetail(siswa)">
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.username }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.nama_siswa }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ siswa.kelas }}</td>
                    <td class="px-6 py-4 whitespace-nowrap flex space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editSiswa(siswa)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Siswa
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton 
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteSiswa(siswa.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Siswa
                        </template>
                      </fwb-tooltip>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>

            <!-- Tampilan mobile -->
            <div class="block md:hidden">
              <template v-if="loading">
                <div v-for="n in 5" :key="n" class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                  <div class="space-y-3">
                    <SkeletonLoader width="150px" />
                    <SkeletonLoader width="80px" />
                  </div>
                </div>
              </template>
              
              <template v-else>
                <div v-for="siswa in paginatedSiswa" :key="siswa.id" 
                     class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow cursor-pointer"
                     @click="showSiswaDetail(siswa)">
                  <div class="space-y-2">
                    <div class="font-medium">{{ siswa.username }}</div>
                    <div class="font-medium">{{ siswa.nama_siswa }}</div>
                    <div class="text-sm text-gray-500">
                      Kelas: {{ siswa.kelas }}
                    </div>
                    <div class="flex space-x-2 pt-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editSiswa(siswa)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Siswa
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark" 
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteSiswa(siswa.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Siswa
                        </template>
                      </fwb-tooltip>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal dengan ukuran responsif -->
      <BaseModal v-model="showAddModal">
        <template #header>
          <div class="flex items-center">
            {{ selectedSiswa ? 'Edit Siswa' : 'Tambah Siswa' }}
          </div>
        </template>
        <template #body>
          <SiswaForm 
            :siswa="selectedSiswa"
            @submit="saveSiswa"
            @cancel="closeModal"
          />
        </template>
      </BaseModal>

      <!-- Tambah modal konfirmasi hapus -->
      <BaseModal v-model="showDeleteModal">
        <template #header>
          <div class="flex items-center">
            Konfirmasi Hapus
          </div>
        </template>
        <template #body>
          <p>Apakah Anda yakin ingin menghapus siswa ini?</p>
        </template>
        <template #footer>
      
          <FwbButton 
            type="button"
            color="dark"
            class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
            @click="showDeleteModal = false"
          >
            Batal
          </FwbButton>
          <FwbButton 
            type="button"
            color="dark"
            class="flex items-center gap-2 px-4 py-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
            @click="confirmDelete"
          >
            Hapus
          </FwbButton>
      
        </template>
      </BaseModal>

      <!-- Tambah modal detail siswa -->
      <BaseModal v-model="showDetailModal">
        <template #header>
          <div class="flex items-center">
            Detail Siswa
          </div>
        </template>
        <template #body>
          <div v-if="selectedSiswaDetail" class="space-y-4">
            <div class="flex flex-wrap justify-center gap-4">
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Username:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.username }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Nama Siswa:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.nama_siswa }}</div>
              </div>
              
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Kelas:</div>
                <div class="w-1/2">{{ selectedSiswaDetail.kelas }}</div>
              </div>
            </div>
          </div>
        </template>
      </BaseModal>

      <div class="mt-4 flex justify-between gap-2">
        <div class="relative flex items-center gap-2 mt-4">
          <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
            Jumlah Siswa: {{ filteredSiswa.length }}
          </div>
        </div>
        <div class="relative flex items-center gap-2">
          <button 
              @click="currentPage--" 
              :disabled="currentPage === 1"
              class="px-3 py-1 rounded-md bg-gray-100 dark:bg-surface-dark hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Sebelumnya
            </button>
              
          <div class="flex items-center gap-2">
            <template v-for="page in totalPages" :key="page">
              <button 
                @click="currentPage = page"
                :class="[
                  'px-3 py-1 rounded-md',
                  currentPage === page 
                    ? 'bg-background-dark dark:bg-surface-light text-white dark:text-black' 
                    : 'bg-gray-100 dark:bg-surface-dark hover:bg-gray-200'
                ]"
              >
                {{ page }}
              </button>
            </template>
          </div>

          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="px-3 py-1 rounded-md bg-gray-100 dark:bg-surface-dark hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Selanjutnya
          </button>
        </div>
      </div>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/config/api'
import SiswaForm from '@/components/form/SiswaForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import { useNotifications } from '@/composables/useNotifications'

const loading = ref(true)
const siswaList = ref([])
const showAddModal = ref(false)
const selectedSiswa = ref(null)
const showDeleteModal = ref(false)
const siswaToDelete = ref(null)
const showDetailModal = ref(false)
const selectedSiswaDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedFilters = ref({
  kelas: []
})

const itemsPerPage = 3
const currentPage = ref(1)

const paginatedSiswa = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredSiswa.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredSiswa.value.length / itemsPerPage)
})

const jumlahGuru = ref(0)

// Tambah computed property untuk kelasList
const kelasList = computed(() => {
  // Mengambil unique kelas dari data siswa
  const uniqueKelas = [...new Set(siswaList.value.map(siswa => siswa.kelas))]
  // Mengurutkan kelas
  return uniqueKelas.sort()
})

// Tambah computed property untuk filtered siswa
const filteredSiswa = computed(() => {
  let result = siswaList.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(siswa => 
      siswa.nama_siswa.toLowerCase().includes(query)
    )
  }

  if (selectedFilters.value.kelas.length > 0) {
    result = result.filter(siswa => 
      selectedFilters.value.kelas.includes(siswa.kelas)
    )
  }

  return result
})

const { notify } = useNotifications()

const fetchSiswa = async () => {
  try {
    const response = await api.get('/siswa/')
    const siswaWithUsers = await Promise.all(
      response.data.map(async (siswa) => {
        try {
          const userResponse = await api.get(`/users/${siswa.user}/`)
          return {
            ...siswa,
            username: userResponse.data.username
          }
        } catch (error) {
          notify({
            type: 'warning',
            title: 'Peringatan',
            message: `Gagal mengambil data user untuk siswa ${siswa.nama_siswa}`
          })
          return {
            ...siswa,
            username: 'User tidak ditemukan'
          }
        }
      })
    )
    siswaList.value = siswaWithUsers
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data siswa'
    })
    console.error('Error fetching siswa:', error)
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedSiswa.value = null
  showAddModal.value = true
}

const editSiswa = (siswa) => {
  selectedSiswa.value = { ...siswa }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedSiswa.value = null
}

const saveSiswa = async (siswaData) => {
  try {
    if (selectedSiswa.value) {
      await api.put(`/siswa/${selectedSiswa.value.id}/`, siswaData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Data siswa berhasil diperbarui'
      })
    } else {
      await api.post('/siswa/', siswaData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Siswa baru berhasil ditambahkan'
      })
    }
    closeModal()
    fetchSiswa()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menyimpan data siswa'
    })
    console.error('Error saving siswa:', error)
  }
}

const deleteSiswa = async (siswaId) => {
  siswaToDelete.value = siswaId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await api.delete(`/siswa/${siswaToDelete.value}/`)
    notify({
      type: 'success',
      title: 'Berhasil',
      message: 'Siswa berhasil dihapus'
    })
    showDeleteModal.value = false
    siswaToDelete.value = null
    fetchSiswa()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus siswa'
    })
    console.error('Error deleting siswa:', error)
  }
}

const showSiswaDetail = (siswa) => {
  selectedSiswaDetail.value = siswa
  showDetailModal.value = true
}

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

const filterDropdownRef = ref(null)

onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

onMounted(() => {
  fetchSiswa()
})
</script>
