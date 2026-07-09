<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'success'])

const formData = ref({
  sifra: '',
  naziv: '',
  cena: 0
})

const loading = ref(false)
const error = ref('')

const resetForm = () => {
  formData.value = {
    sifra: '',
    naziv: '',
    cena: 0
  }
  error.value = ''
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) resetForm()
})

const submitForm = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('http://localhost:8000/api/artikli', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Napaka pri shranjevanju')
    
    emit('success')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="emit('close')"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Nov artikel
              </h3>
              <div class="mt-6 space-y-4">
                
                <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-md text-sm mb-4">
                  {{ error }}
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Šifra artikla</label>
                  <input type="text" v-model="formData.sifra" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Naziv artikla</label>
                  <input type="text" v-model="formData.naziv" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700">Cena (€)</label>
                  <input type="number" step="0.01" v-model="formData.cena" min="0" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" required>
                </div>

              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button @click="submitForm" :disabled="loading || !formData.sifra || !formData.naziv" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50">
            {{ loading ? 'Shranjevanje...' : 'Shrani' }}
          </button>
          <button @click="emit('close')" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
            Prekliči
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
