<template>
  <div class="container">
    <h1>Анализатор GDD</h1>
    
    <div v-if="!projectId">
      <input type="file" @change="onFileSelected" accept="application/pdf" />
      <button @click="uploadFile" :disabled="!selectedFile || isUploading">
        {{ isUploading ? 'Загрузка...' : 'Отправить на анализ' }}
      </button>
    </div>

    <div v-else-if="projectId && !reportData">
      <h3>Нейросети читают GDD...</h3>
      <p>Статус: {{ pollingStatus }}</p>
      </div>

    <div v-else-if="reportData">
      <h3>Анализ завершен!</h3>
      <button @click="reset">Загрузить новый документ</button>
      
      <pre class="report-box">{{ JSON.stringify(reportData, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const isUploading = ref(false)
const projectId = ref(null)
const reportData = ref(null)
const pollingStatus = ref('Ждем ответа от сервера...')

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
  pollingStatus.value = 'Спрашиваем бэкенд...'
  
  try {
    const response = await fetch(`http://localhost:8000/api/v1/projects/${projectId.value}`)
    const data = await response.json()

    if (data.report_data) {
      reportData.value = data.report_data
    } else {
      pollingStatus.value = 'Агенты еще думают...'
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
}
</script>

<style>
.container { max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
.report-box { background: #1e1e1e; color: #a6e22e; padding: 15px; border-radius: 8px; overflow-x: auto; text-align: left; }
button { margin-top: 10px; padding: 8px 16px; cursor: pointer; }
</style>