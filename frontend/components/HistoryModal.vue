<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  artikel: Object // Sprejme izbrani artikel
})

const emit = defineEmits(['close'])

const premiki = ref([])
const loading = ref(false)
const error = ref('')

const fetchPremiki = async () => {
  if (!props.artikel) return
  
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`/api/artikli/${props.artikel.id}/premiki`)
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Napaka pri nalaganju zgodovine')
    premiki.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    fetchPremiki()
  } else {
    premiki.value = []
  }
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('sl-SI', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="emit('close')"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Zgodovina premikov: {{ artikel?.naziv }} ({{ artikel?.sifra }})
                </h3>
                <button @click="emit('close')" class="text-gray-400 hover:text-gray-500">
                  <span class="sr-only">Zapri</span>
                  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div class="mt-4">
                <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-md text-sm mb-4">
                  {{ error }}
                </div>
                
                <div v-if="loading" class="text-center py-8 text-gray-500">
                  Nalaganje zgodovine...
                </div>
                
                <div v-else-if="premiki.length === 0" class="text-center py-8 text-gray-500 border border-gray-200 rounded-lg bg-gray-50">
                  Za ta artikel še ni zabeleženih premikov.
                </div>

                <div v-else class="border border-gray-200 rounded-lg overflow-hidden">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Datum in čas</th>
                        <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tip</th>
                        <th scope="col" class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Količina</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="premik in premiki" :key="premik.id" class="hover:bg-gray-50">
                        <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                          {{ formatDate(premik.datum) }}
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-sm">
                          <span :class="[
                            'px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                            premik.tip_premika === 'prevzem' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                          ]">
                            {{ premik.tip_premika === 'prevzem' ? 'Prevzem' : 'Izdaja' }}
                          </span>
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-right text-gray-900">
                          {{ premik.tip_premika === 'prevzem' ? '+' : '-' }}{{ premik.kolicina }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button @click="emit('close')" type="button" class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:w-auto sm:text-sm">
            Zapri
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
