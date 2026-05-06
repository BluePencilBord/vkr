<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

const handleRegister = async () => {
  try {
    loading.value = true
    errorMsg.value = ''
    await register(email.value, password.value)
    // Optional: auto-login after register, or just redirect to login
    router.push('/login')
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Регистрация</h2>
      
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input 
            v-model="email" 
            type="email" 
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Пароль</label>
          <input 
            v-model="password" 
            type="password" 
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div v-if="errorMsg" class="text-red-500 text-sm text-center">
          {{ errorMsg }}
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
        >
          {{ loading ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="mt-4 text-center text-sm text-gray-600">
        Уже есть аккаунт? 
        <RouterLink to="/login" class="font-medium text-blue-600 hover:text-blue-500">
          Войти
        </RouterLink>
      </p>
    </div>
  </div>
</template>
