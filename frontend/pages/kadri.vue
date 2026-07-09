<script setup>
import { ref } from 'vue'

const auth = useAuth()
if (!auth.hasRole(['admin'])) {
  navigateTo('/')
}

const { data: uporabniki, refresh } = await useFetch('http://localhost:8000/api/uporabniki')

const formData = ref({
  ime: '',
  priimek: '',
  email: '',
  vloga: 'prodajalec',
  geslo: ''
})

const isSubmitting = ref(false)
const errorMsg = ref('')

const shraniUporabnika = async () => {
  isSubmitting.value = true
  errorMsg.value = ''
  try {
    const res = await fetch('http://localhost:8000/api/uporabniki', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.detail || 'Napaka pri shranjevanju')
    }
    
    // Počisti formo
    formData.value = {
      ime: '',
      priimek: '',
      email: '',
      vloga: 'prodajalec',
      geslo: ''
    }
    refresh()
  } catch (e) {
    errorMsg.value = e.message
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Upravljanje Kadrov</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Obrazec za dodajanje -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-medium text-gray-900 mb-4">Nov Zaposleni</h2>
        
        <div v-if="errorMsg" class="mb-4 bg-red-50 text-red-600 p-3 rounded-md text-sm">
          {{ errorMsg }}
        </div>

        <form @submit.prevent="shraniUporabnika" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Ime</label>
              <input type="text" v-model="formData.ime" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Priimek</label>
              <input type="text" v-model="formData.priimek" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">E-pošta</label>
            <input type="email" v-model="formData.email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Geslo</label>
            <input type="password" v-model="formData.geslo" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Vloga</label>
            <select v-model="formData.vloga" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              <option value="prodajalec">Prodajalec (računi, prodaja)</option>
              <option value="skladiscnik">Skladiščnik (nabava, zaloga)</option>
              <option value="admin">Administrator (vse)</option>
            </select>
          </div>
          <div class="pt-2">
            <button type="submit" :disabled="isSubmitting" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
              Dodaj uporabnika
            </button>
          </div>
        </form>
      </div>

      <!-- Tabela kadrov -->
      <div class="lg:col-span-2">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ime in priimek</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">E-pošta</th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vloga</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="u in uporabniki" :key="u.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap font-medium text-gray-900">{{ u.ime }} {{ u.priimek }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ u.email }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                        :class="u.vloga === 'admin' ? 'bg-purple-100 text-purple-800' : (u.vloga === 'prodajalec' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800')">
                    {{ u.vloga }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>
