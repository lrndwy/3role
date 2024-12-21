<template>
  <Notifications ref="notificationsRef" />
  <TransitionWrapper>
    <div class="p-8">
      <h1 class="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8 text-text-light-primary dark:text-text-dark-primary">
        Manajemen Karyawan
      </h1>
      
      <div>
        <div class="flex flex-wrap items-center gap-2 mb-6">
          <div class="flex-1">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari nama karyawan..."
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
                    <div class="font-medium mb-2">Jabatan</div>
                    <div class="space-y-2 flex flex-col">
                      <label v-for="jabatan in jabatanList" :key="jabatan">
                        <Checkbox 
                          v-model="selectedFilters.jabatan" 
                          :value="jabatan"
                        >
                          {{ jabatan }}
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
              Tambah Karyawan
            </template>
          </fwb-tooltip>
        </div>

        <div class="overflow-x-auto rounded-lg lg:border lg:border-gray-200 dark:lg:border-border-dark">
          <div class="inline-block min-w-full align-middle">
            <!-- Tampilan desktop -->
            <table class="hidden md:table min-w-full divide-y divide-gray-200 dark:divide-border-dark">
              <thead class="bg-surface-light dark:bg-surface-dark">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Username
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Nama Karyawan
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-text-light-secondary dark:text-text-dark-secondary uppercase tracking-wider">
                    Jabatan
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
                      <SkeletonLoader width="100px" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <SkeletonLoader width="120px" />
                    </td>
                  </tr>
                </template>
                <template v-else>
                  <tr v-for="karyawan in paginatedKaryawan" :key="karyawan.id" 
                      class="hover:bg-gray-50 dark:hover:bg-surface-dark cursor-pointer"
                      @click="showKaryawanDetail(karyawan)">
                    <td class="px-6 py-4 whitespace-nowrap">{{ karyawan.username }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ karyawan.nama_karyawan }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">{{ karyawan.jabatan }}</td>
                    <td class="px-6 py-4 whitespace-nowrap flex space-x-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editKaryawan(karyawan)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Karyawan
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark" 
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteKaryawan(karyawan.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Karyawan
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
                    <SkeletonLoader width="100px" />
                  </div>
                </div>
              </template>
              
              <template v-else>
                <div v-for="karyawan in filteredKaryawan" :key="karyawan.id" 
                    class="bg-white dark:bg-background-dark p-4 mb-4 rounded-lg shadow cursor-pointer"
                    @click="showKaryawanDetail(karyawan)">
                  <div class="space-y-2">
                    <div class="font-medium">
                      {{ karyawan.username }}
                    </div>
                    <div class="font-medium">
                      {{ karyawan.nama_karyawan }}
                    </div>
                    <div class="text-sm text-gray-500">
                      Jabatan: {{ karyawan.jabatan }}
                    </div>
                    <div class="flex space-x-2 pt-2">
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark"
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="editKaryawan(karyawan)"
                          >
                            <PencilIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Edit Karyawan
                        </template>
                      </fwb-tooltip>
                      <fwb-tooltip>
                        <template #trigger>
                          <FwbButton
                            color="dark" 
                            class="flex items-center gap-2 p-2 bg-background-dark dark:bg-background-light text-white dark:text-black hover:bg-surface-dark dark:hover:bg-surface-light"
                            @click.stop="deleteKaryawan(karyawan.id)"
                          >
                            <TrashIcon class="w-4 h-4" />
                          </FwbButton>
                        </template>
                        <template #content>
                          Hapus Karyawan
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
            {{ selectedKaryawan ? 'Edit Karyawan' : 'Tambah Karyawan' }}
          </div>
        </template>
        <template #body>
          <KaryawanForm 
            :karyawan="selectedKaryawan"
            @submit="saveKaryawan"
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
          <p>Apakah Anda yakin ingin menghapus karyawan ini?</p>
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

      <!-- Modal detail karyawan -->
      <BaseModal v-model="showDetailModal">
        <template #header>
          <div class="flex items-center">
            Detail Karyawan
          </div>
        </template>
        <template #body>
          <div v-if="selectedKaryawanDetail" class="space-y-4">
            <div class="flex flex-wrap justify-center gap-4">
              <div class="w-full flex flex-wrap">
                <div class="w-1/2 font-medium">Username:</div>
                <div class="w-1/2 break-words">{{ selectedKaryawanDetail.username }}</div>
              </div>
              
              <div class="w-full flex flex-wrap">
                <div class="w-1/2 font-medium">Nama Karyawan:</div>
                <div class="w-1/2 break-words">{{ selectedKaryawanDetail.nama_karyawan }}</div>
              </div>
              
              <div class="w-full flex flex-wrap">
                <div class="w-1/2 font-medium">Jabatan:</div>
                <div class="w-1/2 break-words">{{ selectedKaryawanDetail.jabatan }}</div>
              </div>
            </div>
          </div>
        </template>
      </BaseModal>

      <!-- Pagination -->
      <div class="mt-4 flex justify-between gap-2">
        <div class="relative flex items-center gap-2 mt-4">
          <div class="mb-4 ml-2 text-md text-gray-600 dark:text-gray-400">
            Jumlah Karyawan: {{ filteredKaryawan.length }}
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
import { ref, onMounted, computed, watch } from 'vue'
import api from '@/config/api'
import KaryawanForm from '@/components/form/KaryawanForm.vue'
import { FwbButton, FwbTooltip } from 'flowbite-vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import TransitionWrapper from '@/components/TransitionWrapper.vue'
import { PencilIcon, TrashIcon, FunnelIcon, PlusIcon } from '@heroicons/vue/24/outline'
import BaseModal from '@/components/BaseModal.vue'
import { onClickOutside } from '@vueuse/core'
import Checkbox from '@/components/Checkbox.vue'
import Notifications from '@/components/Notifications.vue'
import { useNotifications } from '@/composables/useNotifications'

const loading = ref(true)
const karyawanList = ref([])
const showAddModal = ref(false)
const selectedKaryawan = ref(null)
const showDeleteModal = ref(false)
const karyawanToDelete = ref(null)
const showDetailModal = ref(false)
const selectedKaryawanDetail = ref(null)
const searchQuery = ref('')
const showFilterDropdown = ref(false)
const selectedFilters = ref({
  jabatan: []
})

const itemsPerPage = 3
const currentPage = ref(1)

const jabatanList = computed(() => {
  const uniqueJabatan = [...new Set(karyawanList.value.map(karyawan => karyawan.jabatan))]
  return uniqueJabatan.sort()
})

const filteredKaryawan = computed(() => {
  let result = karyawanList.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(karyawan => 
      karyawan.nama_karyawan.toLowerCase().includes(query)
    )
  }

  if (selectedFilters.value.jabatan.length > 0) {
    result = result.filter(karyawan => 
      selectedFilters.value.jabatan.includes(karyawan.jabatan)
    )
  }

  return result
})

const paginatedKaryawan = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredKaryawan.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredKaryawan.value.length / itemsPerPage)
})

const fetchKaryawan = async () => {
  try {
    const response = await api.get('/karyawan/')
    const karyawanWithUsers = await Promise.all(
      response.data.map(async (karyawan) => {
        try {
          const userResponse = await api.get(`/users/${karyawan.user}/`)
          return {
            ...karyawan,
            username: userResponse.data.username
          }
        } catch (error) {
          notify({
            type: 'warning',
            title: 'Peringatan',
            message: `Gagal mengambil data user untuk karyawan ${karyawan.nama_karyawan}`
          })
          return {
            ...karyawan,
            username: 'User tidak ditemukan'
          }
        }
      })
    )
    karyawanList.value = karyawanWithUsers
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: 'Gagal mengambil data karyawan'
    })
    console.error('Error fetching karyawan:', error)
  } finally {
    loading.value = false
  }
}

const showModal = () => {
  selectedKaryawan.value = null
  showAddModal.value = true
}

const editKaryawan = (karyawan) => {
  selectedKaryawan.value = { ...karyawan }
  showAddModal.value = true
}

const closeModal = () => {
  showAddModal.value = false
  selectedKaryawan.value = null
}

const saveKaryawan = async (karyawanData) => {
  try {
    if (selectedKaryawan.value) {
      await api.put(`/karyawan/${selectedKaryawan.value.id}/`, karyawanData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Data karyawan berhasil diperbarui'
      })
    } else {
      await api.post('/karyawan/', karyawanData)
      notify({
        type: 'success',
        title: 'Berhasil',
        message: 'Karyawan baru berhasil ditambahkan'
      })
    }
    closeModal()
    fetchKaryawan()
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menyimpan data karyawan'
    })
    console.error('Error saving karyawan:', error)
  }
}

const deleteKaryawan = async (karyawanId) => {
  karyawanToDelete.value = karyawanId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await api.delete(`/karyawan/${karyawanToDelete.value}/`)
    notify({
      type: 'success',
      title: 'Berhasil',
      message: 'Karyawan berhasil dihapus'
    })
    fetchKaryawan()
    showDeleteModal.value = false
  } catch (error) {
    notify({
      type: 'error',
      title: 'Gagal',
      message: error.response?.data?.message || 'Terjadi kesalahan saat menghapus karyawan'
    })
    console.error('Error deleting karyawan:', error)
  }
}

const showKaryawanDetail = (karyawan) => {
  selectedKaryawanDetail.value = karyawan
  showDetailModal.value = true
}

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

const filterDropdownRef = ref(null)

onClickOutside(filterDropdownRef, () => {
  showFilterDropdown.value = false
})

watch([searchQuery, selectedFilters], () => {
  currentPage.value = 1
})

onMounted(() => {
  fetchKaryawan()
})

const { notify } = useNotifications()
</script> 
