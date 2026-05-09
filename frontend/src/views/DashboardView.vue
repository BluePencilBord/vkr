<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProjects, getProject, uploadProject, analyzeProject, deleteProject } from '../api'
import { marked } from 'marked'

const router = useRouter()
const projects = ref([])
const activeProject = ref(null)
const loadingProjects = ref(true)

// Upload form state
const showUploadForm = ref(false)
const uploadTitle = ref('')
const uploadFile = ref(null)
const uploadLoading = ref(false)
const uploadError = ref('')

// Polling state
const analyzingStatus = ref({})
let pollInterval = null

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const fetchProjects = async () => {
  try {
    loadingProjects.value = true
    projects.value = await getProjects()
  } catch (error) {
    console.error('Error fetching projects:', error)
  } finally {
    loadingProjects.value = false
  }
}

const selectProject = (project) => {
  activeProject.value = project
  showUploadForm.value = false
}

const handleFileChange = (e) => {
  uploadFile.value = e.target.files[0]
}

const submitUpload = async () => {
  if (!uploadFile.value || !uploadTitle.value) return
  
  try {
    uploadLoading.value = true
    uploadError.value = ''
    const newProject = await uploadProject(uploadTitle.value, uploadFile.value)
    projects.value.push(newProject)
    selectProject(newProject)
    uploadTitle.value = ''
    uploadFile.value = null
  } catch (err) {
    uploadError.value = err.message
  } finally {
    uploadLoading.value = false
  }
}

const startPolling = (projectId) => {
  if (pollInterval) clearInterval(pollInterval)
  
  pollInterval = setInterval(async () => {
    try {
      const updatedProject = await getProject(projectId)
      
      if (activeProject.value?.id === projectId) {
        activeProject.value = updatedProject
      }
      
      const index = projects.value.findIndex(p => p.id === projectId)
      if (index !== -1) projects.value[index] = updatedProject
      
      if (updatedProject.report_data) {
        analyzingStatus.value[projectId] = false
        clearInterval(pollInterval)
      }
    } catch (e) {
      console.error('Polling error', e)
    }
  }, 3000)
}

const handleAnalyze = async (projectId) => {
  try {
    analyzingStatus.value[projectId] = true
    if (activeProject.value?.id === projectId) {
      activeProject.value.report_data = null
    }
    const index = projects.value.findIndex(p => p.id === projectId)
    if (index !== -1) {
      projects.value[index].report_data = null
    }
    await analyzeProject(projectId)
    startPolling(projectId)
  } catch (error) {
    analyzingStatus.value[projectId] = false
    alert('Ошибка при запуске анализа: ' + error.message)
  }
}

const handleDelete = async (projectId) => {
  if (!confirm('Вы уверены, что хотите удалить этот проект? Это действие нельзя отменить.')) return
  
  try {
    await deleteProject(projectId)
    projects.value = projects.value.filter(p => p.id !== projectId)
    if (activeProject.value?.id === projectId) {
      activeProject.value = null
    }
  } catch (error) {
    alert('Ошибка при удалении проекта: ' + error.message)
  }
}

const openUploadForm = () => {
  activeProject.value = null
  showUploadForm.value = true
}

onMounted(() => {
  fetchProjects()
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-4 border-b border-gray-200 flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-800">Проекты</h1>
      </div>
      
      <div class="flex-1 overflow-y-auto p-4 space-y-2">
        <div v-if="loadingProjects" class="text-sm text-gray-500">Загрузка проектов...</div>
        <div v-else-if="projects.length === 0" class="text-sm text-gray-500">Нет проектов</div>
        
        <div
          v-for="project in projects"
          :key="project.id"
          class="flex items-center w-full rounded-md transition-colors cursor-pointer group"
          :class="activeProject?.id === project.id ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-100'"
          @click="selectProject(project)"
        >
          <div class="flex-1 text-left px-4 py-2 truncate">
            {{ project.title }}
          </div>
          <button
            @click.stop="handleDelete(project.id)"
            class="p-2 text-gray-400 hover:text-red-600 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
            title="Удалить проект"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
          </button>
        </div>
      </div>

      <div class="p-4 border-t border-gray-200 space-y-3">
        <button 
          @click="openUploadForm"
          class="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
        >
          Новый проект
        </button>
        <button 
          @click="handleLogout"
          class="w-full flex justify-center items-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          Выйти
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-8">
      
      <!-- Upload Form -->
      <div v-if="showUploadForm" class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Загрузить новый GDD</h2>
        <form @submit.prevent="submitUpload" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Название проекта</label>
            <input 
              v-model="uploadTitle" 
              type="text" 
              required
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Файл (PDF или DOCX)</label>
            <input 
              type="file" 
              accept=".pdf,.docx"
              @change="handleFileChange"
              required
              class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>
          
          <div v-if="uploadError" class="text-red-500 text-sm">{{ uploadError }}</div>
          
          <button 
            type="submit" 
            :disabled="uploadLoading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            {{ uploadLoading ? 'Загрузка...' : 'Создать проект' }}
          </button>
        </form>
      </div>

      <!-- Project Detail -->
      <div v-else-if="activeProject" class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div class="flex justify-between items-start mb-6">
          <h2 class="text-3xl font-bold text-gray-800">{{ activeProject.title }}</h2>
          <div class="flex gap-2">
            <button 
              @click="handleAnalyze(activeProject.id)"
              :disabled="analyzingStatus[activeProject.id]"
              class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 disabled:opacity-50"
            >
              {{ analyzingStatus[activeProject.id] ? 'Анализ идет...' : (activeProject.report_data ? 'Сделать повторный анализ' : 'Запустить анализ') }}
            </button>
            <button 
              @click="handleDelete(activeProject.id)"
              class="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Удалить
            </button>
          </div>
        </div>
        
        <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 mb-6">
          <p class="text-sm text-gray-600 mb-2"><span class="font-semibold">ID:</span> {{ activeProject.id }}</p>
          <p class="text-sm text-gray-600 mb-2"><span class="font-semibold">Создан:</span> {{ new Date(activeProject.created_at).toLocaleString() }}</p>
          <div v-if="activeProject.gdd_url" class="mt-4">
            <a :href="activeProject.gdd_url" target="_blank" class="text-blue-600 hover:underline flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              Скачать GDD документ
            </a>
          </div>
          <div v-else class="mt-4 text-sm text-gray-500 italic">Файл недоступен (возможно, еще загружается или S3 не настроен)</div>
        </div>

        <div class="border-t border-gray-200 pt-6">
          <h3 class="text-xl font-semibold mb-4">Результаты анализа</h3>
          <div v-if="activeProject.report_data?.summary_text" class="bg-white p-6 rounded-lg border border-gray-200">
            <div class="prose prose-blue max-w-none text-gray-800" v-html="marked.parse(activeProject.report_data.summary_text)"></div>
          </div>
          <div v-else-if="activeProject.report_data?.error" class="bg-red-50 p-6 rounded-lg border border-red-200">
            <h4 class="text-red-800 font-semibold mb-2">Ошибка при анализе:</h4>
            <p class="text-red-700 whitespace-pre-wrap">{{ activeProject.report_data.error }}</p>
          </div>
          <div v-else-if="analyzingStatus[activeProject.id]" class="text-blue-600 font-medium flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Анализ запущен и процесс идет. Пожалуйста, подождите...
          </div>
          <div v-else class="text-gray-500 italic">
            Анализ еще не завершен или не был запущен. Нажмите "Запустить анализ", если вы еще этого не сделали.
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="h-full flex flex-col items-center justify-center text-gray-500">
        <svg class="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
        <p class="text-lg">Выберите проект из списка слева или создайте новый</p>
      </div>

    </main>
  </div>
</template>
