<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl w-full text-center space-y-8">
      <div>
        <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          <span class="block">Мультиагентная система</span>
          <span class="block text-blue-600">анализа GDD</span>
        </h1>
        <p class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
          Интеллектуальный инструмент для геймдизайнеров и разработчиков. Загрузите ваш Game Design Document и получите глубокий анализ, рекомендации и декомпозицию задач с помощью передовых ИИ-агентов.
        </p>
      </div>
      
      <div class="bg-white p-8 rounded-xl shadow-md border border-gray-100">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Для начала работы</h2>
        <p class="text-gray-600 mb-8">Зарегистрируйтесь в системе или войдите в существующий аккаунт, чтобы получить доступ к функционалу загрузки и анализа проектов.</p>
        
        <div class="flex flex-col sm:flex-row justify-center gap-4">
          <button 
            @click="goToRegister"
            class="w-full sm:w-auto flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg px-10 shadow-sm transition-colors"
          >
            Зарегистрироваться
          </button>
          <button 
            @click="goToLogin"
            class="w-full sm:w-auto flex items-center justify-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 md:py-4 md:text-lg px-10 shadow-sm transition-colors"
          >
            Войти
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
