<template>
  <TransitionWrapper>
    <div class="p-8">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Guru
      </h1>
      
      <div>
        <div class="flex flex-wrap gap-2 mb-6">
          <div class="flex-1">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari nama guru..."
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
                    <div class="font-medium mb-2">Mata Pelajaran</div>
                    <div class="space-y-2 flex flex-col">
                      <Checkbox 
                        v-for="mapel in mapelList" 
                        :key="mapel"
                        v-model="selectedFilters.mapel"
                        :value="mapel"
                      >
                        {{ mapel }}
                      </Checkbox>
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
              Tambah Guru
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
                    Nama Guru
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Mata Pelajaran
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Aksi
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200 dark:divide-border-dark dark:bg-background-dark">
                <template v-if="loading">
                  <tr v-for="n in 5" :key="n" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="150px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="150px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="120px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="120px" />
                    </td>
                  </tr>
                </template>
                <template v-else>
                  <tr v-for="guru in paginatedGuru" :key="guru.id" 
                      class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                      @click="showGuruDetail(guru)">
                    <td class="px-6 py-4 whitespace-nowrap">{{ guru.username }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ guru.nama_guru }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ guru.nama_mapel }}</td>
                    <td class="px-6 py-4 whitespace-nowrap flex space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editGuru(guru)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Guru
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteGuru(guru.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Guru
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
                    <SkeletonLoader width="120px" />
                  </div>
                </div>
              </template>
              
              <template v-else>
                <div v-for="guru in guruList" :key="guru.id" class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow">
                  <div class="space-y-2">
                    <div class="font-medium">
                      {{ guru.username }}
                    </div>
                    <div class="font-medium">
                      {{ guru.nama_guru }}
                    </div>
                    <div class="text-gray-600">
                      {{ guru.nama_mapel }}
                    </div>
                    <div class="flex space-x-2 pt-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click="editGuru(guru)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Guru
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click="deleteGuru(guru.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Guru
                        </template>
                      </fwb-tooltip>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="mt-4 flex justify-between gap-2">
          <div class="relative flex items-center gap-2 mt-4">
            <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
              Jumlah Guru: {{ filteredGuru.length }}
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

      <!-- Modal dengan ukuran responsif -->
      <BaseModal v-model="showAddModal">
        <template #header>
          <div class="flex items-center">
            {{ selectedGuru ? 'Edit Guru' : 'Tambah Guru' }}
          </div>
        </template>
        <template #body>
          <GuruForm 
            :guru="selectedGuru"
            @submit="saveGuru"
            @cancel="closeModal"
          />
        </template>
      </BaseModal>

      <!-- Modal konfirmasi hapus -->
      <BaseModal v-model="showDeleteModal">
        <template #header>
          <div class="flex items-center">
            Konfirmasi Hapus
          </div>
        </template>
        <template #body>
          <p>Apakah Anda yakin ingin menghapus guru ini?</p>
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

      <!-- Modal detail guru -->
      <BaseModal v-model="showDetailModal">
        <template #header>
          <div class="flex items-center">
            Detail Guru
          </div>
        </template>
        <template #body>
          <div v-if="selectedGuruDetail" class="space-y-4">
            <div class="flex flex-wrap justify-center gap-4">
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Username:</div>
                <div class="w-1/2 break-words">{{ selectedGuruDetail.username }}</div>
              </div>
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Nama Guru:</div>
                <div class="w-1/2 break-words">{{ selectedGuruDetail.nama_guru }}</div>
              </div>
              <div class="w-full flex">
                <div class="w-1/2 font-medium">Mata Pelajaran:</div>
                <div class="w-1/2 break-words">{{ selectedGuruDetail.nama_mapel }}</div>
              </div>
            </div>
          </div>
        </template>
      </BaseModal>
    </div>
  </TransitionWrapper>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/config/api'
import GuruForm from '@/components/form/GuruForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import { useNotifications } from '@/composables/useNotifications'

const loading = ref(true)
const guruList = ref([])
const showAddModal = ref(false)
const selectedGuru = ref(null)
const showDeleteModal = ref(false)
const guruToDelete = ref(null)
const showDetailModal = ref(false)
const selectedGuruDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedFilters = ref({
  mapel: []
})

const itemsPerPage = 3
const currentPage = ref(1)

const paginatedGuru = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredGuru.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredGuru.value.length / itemsPerPage)
})

// Computed property untuk mapelList
const mapelList = computed(() => {
  const uniqueMapel = [...new Set(guruList.value.map(guru => guru.nama_mapel))]
  return uniqueMapel.sort()
})

// Computed property untuk filtered guru
const filteredGuru = computed(() => {
  let result = guruList.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(guru => 
      guru.nama_guru.toLowerCase().includes(query)
    )
  }

  if (selectedFilters.value.mapel.length > 0) {
    result = result.filter(guru => 
      selectedFilters.value.mapel.includes(guru.nama_mapel)
    )
  }

  return result
})

// Inisialisasi notifications
const { notify } = useNotifications()

const fetchGuru = async () => {
  try {
    const response = await api.get('/guru/')
    const guruWithUsers = await Promise.all(
      response.data.map(async (guru) => {
        try {
          const userResponse = await api.get(`/users/${guru.user}/`)
          return {
            ...guru,
            username: userResponse.data.username
          }
        } catch (error) {
          notify({
            type: 'warning',
            title: 'Peringatan',
            message: `Gagal mengambil data user untuk guru ${guru.nama_guru}`
          })
          return {
            ...guru,
            username: 'User tidak ditemukan'
          }
        }
      })
    )
    guruList.value = guruWithUsers
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data guru'
    })
    console.error('Error fetching guru:', error)
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedGuru.value = null
  showAddModal.value = true
}

const editGuru = (guru) => {
  selectedGuru.value = { ...guru }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedGuru.value = null
}

const saveGuru = async (guruData) => {
  try {
    if (selectedGuru.value) {
      await api.put(`/guru/${selectedGuru.value.id}/`, guruData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Data guru berhasil diperbarui'
      })
    } else {
      await api.post('/guru/', guruData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Guru baru berhasil ditambahkan'
      })
    }
    closeModal()
    fetchGuru()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menyimpan data guru'
    })
    console.error('Error saving guru:', error)
  }
}

const deleteGuru = async (guruId) => {
  guruToDelete.value = guruId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await api.delete(`/guru/${guruToDelete.value}/`)
    notify({
      type: 'success',
      title: 'Berhasil',
      message: 'Guru berhasil dihapus'
    })
    fetchGuru()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus guru'
    })
    console.error('Error deleting guru:', error)
  }
  showDeleteModal.value = false
}

const showGuruDetail = (guru) => {
  selectedGuruDetail.value = guru
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
  fetchGuru()
})
</script>
