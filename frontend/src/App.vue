<template>
  <div class="min-h-screen bg-gray-900 text-gray-100 font-sans selection:bg-indigo-500 selection:text-white pb-12">
    
    <header class="border-b border-gray-800 bg-gray-900/50 backdrop-blur-md sticky top-0 z-10">
      <div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-2xl">🎮</span>
          <h1 class="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            GameDesign AI
          </h1>
        </div>
      </div>
    </header>

    <main class="max-w-3xl mx-auto px-6 mt-12">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-extrabold tracking-tight text-white mb-4">
          Анализ GDD с помощью нейросетей
        </h2>
        <p class="text-gray-400 text-lg">
          Загрузи свой геймдизайн-документ (PDF), и наша команда AI-агентов разберет его на механики, риски и целевую аудиторию.
        </p>
      </div>

      <div v-if="!projectId" class="bg-gray-800 rounded-2xl p-8 border border-gray-700 shadow-2xl transition-all hover:border-indigo-500/50 relative overflow-hidden">
        
        <div class="absolute -top-24 -right-24 w-48 h-48 bg-indigo-500/20 blur-3xl rounded-full"></div>

        <div class="relative z-10 flex flex-col items-center justify-center text-center">
          <div class="w-16 h-16 bg-gray-700 rounded-full flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
          </div>
          
          <label class="cursor-pointer group">
            <span class="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 shadow-lg shadow-indigo-500/30">
              Выбрать PDF файл
            </span>
            <input type="file" @change="onFileSelected" accept="application/pdf" class="hidden" />
          </label>
          
          <p class="mt-4 text-sm text-gray-400">
            {{ selectedFile ? `Выбран файл: ${selectedFile.name}` : 'Или перетащи файл сюда' }}
          </p>

          <button 
            @click="uploadFile" 
            :disabled="!selectedFile || isUploading"
            class="mt-8 w-full py-3 rounded-lg font-bold transition-all duration-200"
            :class="selectedFile && !isUploading ? 'bg-white text-gray-900 hover:bg-gray-200 shadow-[0_0_20px_rgba(255,255,255,0.3)]' : 'bg-gray-700 text-gray-500 cursor-not-allowed'"
          >
            {{ isUploading ? 'Отправляем на сервер...' : 'Начать анализ' }}
          </button>
        </div>
      </div>

      <div v-else-if="projectId && !reportData" class="bg-gray-800 rounded-2xl p-12 border border-gray-700 shadow-xl text-center">
        <div class="flex flex-col items-center justify-center">
          <svg class="animate-spin h-12 w-12 text-indigo-500 mb-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <h3 class="text-2xl font-bold text-white mb-2">Агенты за работой</h3>
          <p class="text-indigo-300 animate-pulse">{{ pollingStatus }}</p>
        </div>
      </div>

      <div v-else-if="reportData" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-2xl font-bold text-white">Результаты анализа</h3>
          <button @click="reset" class="text-sm text-gray-400 hover:text-white transition-colors flex items-center gap-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
            Новый анализ
          </button>
        </div>

        <div class="bg-gray-800 rounded-2xl border border-gray-700 shadow-xl overflow-hidden">
          <div class="bg-gray-900/50 px-6 py-3 border-b border-gray-700 flex items-center">
            <div class="flex gap-2">
              <div class="w-3 h-3 rounded-full bg-red-500"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div class="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <span class="ml-4 text-sm font-mono text-gray-500">report.json</span>
          </div>
          <pre class="p-6 overflow-x-auto text-sm font-mono text-green-400 leading-relaxed">{{ JSON.stringify(reportData, null, 2) }}</pre>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const isUploading = ref(false)
const projectId = ref(null)
const reportData = ref(null)
const pollingStatus = ref('Инициализация роутера...')

const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0]
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  isUploading.value = true

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const response = await fetch('http://localhost:8000/api/v1/projects/', {
      method: 'POST',
      body: formData
    })
    
    const data = await response.json()
    projectId.value = data.id
    
    startPolling()
  } catch (error) {
    console.error('Ошибка загрузки:', error)
    alert('Ошибка загрузки файла!')
  } finally {
    isUploading.value = false
  }
}

const startPolling = async () => {
  // ИЗМЕНИТЬ В БУДУЩЕМ
  const statuses = [
    'Нарративщик изучает лор...',
    'Продюсер считает деньги...',
    'Геймдизайнер тестирует механики...',
    'Маркетолог ищет конкурентов в Steam...',
    'Лид собирает финальный отчет...'
  ]
  pollingStatus.value = statuses[Math.floor(Math.random() * statuses.length)]
  
  try {
    const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId.value}`)
    const data = await response.json()

    if (data.report_data) {
      reportData.value = data.report_data
    } else {
      setTimeout(startPolling, 3000)
    }
  } catch (error) {
    console.error('Ошибка при опросе:', error)
    pollingStatus.value = 'Ошибка связи с сервером'
    setTimeout(startPolling, 5000)
  }
}

const reset = () => {
  selectedFile.value = null
  projectId.value = null
  reportData.value = null
  pollingStatus.value = 'Инициализация роутера...'
}
</script>