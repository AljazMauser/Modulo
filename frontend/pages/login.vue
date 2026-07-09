<script setup>
import { ref } from 'vue'

definePageMeta({
  layout: false // Brez default navigacije
})

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const auth = useAuth()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  const success = await auth.login(email.value, password.value)
  if (success) {
    navigateTo('/')
  } else {
    error.value = 'Prijava ni uspela. Preverite e-pošto in geslo.'
  }
  loading.value = false
}
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Prijava v Modulo
      </h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div v-if="error" class="bg-red-50 p-4 rounded-md">
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700"> E-pošta </label>
            <div class="mt-1">
              <input id="email" v-model="email" name="email" type="email" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700"> Geslo </label>
            <div class="mt-1">
              <input id="password" v-model="password" name="password" type="password" required class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" />
            </div>
          </div>

          <div>
            <button type="submit" :disabled="loading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
              {{ loading ? 'Prijavljam...' : 'Prijava' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
