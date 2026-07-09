<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'success'])

const formData = ref({
  stevilka_racuna: '',
  partner_id: '',
  postavke: []
})

const partnerji = ref([])
const artikli = ref([])
const loading = ref(false)
const error = ref('')

const isPartnerModalOpen = ref(false)

const handlePartnerSuccess = (newPartner) => {
  // Dodamo novega partnerja v seznam in ga takoj izberemo
  partnerji.value.push(newPartner)
  formData.value.partner_id = newPartner.id
  isPartnerModalOpen.value = false
}

const fetchDependencies = async () => {
  try {
    const [pRes, aRes] = await Promise.all([
      fetch('/api/partnerji'),
      fetch('/api/artikli')
    ])
    partnerji.value = await pRes.json()
    artikli.value = await aRes.json()
  } catch (err) {
    console.error('Napaka pri nalaganju odvisnosti:', err)
  }
}

const dodajPostavko = () => {
  formData.value.postavke.push({
    artikel_id: '',
    kolicina: 1,
    prodajna_cena: 0,
    davek_procent: 22.0
  })
}

const odstraniPostavko = (index) => {
  formData.value.postavke.splice(index, 1)
}

const onArtikelSelect = (index) => {
  const selectedId = formData.value.postavke[index].artikel_id
  const artikel = artikli.value.find(a => a.id === selectedId)
  if (artikel) {
    // Predlagaj prodajno ceno iz artikla
    formData.value.postavke[index].prodajna_cena = artikel.cena
  }
}

const resetForm = () => {
  formData.value = {
    stevilka_racuna: `INV-${new Date().getFullYear()}-${Math.floor(Math.random() * 10000)}`,
    partner_id: '',
    postavke: []
  }
  error.value = ''
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    resetForm()
    fetchDependencies()
  }
})

const submitForm = async () => {
  if (formData.value.postavke.length === 0) {
    error.value = 'Dodati morate vsaj eno postavko na račun!'
    return
  }

  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/racuni', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Napaka pri shranjevanju računa')
    
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

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                Nov Račun
              </h3>
              
              <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-md text-sm mb-4">
                {{ error }}
              </div>

              <div class="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Številka računa</label>
                  <input type="text" v-model="formData.stevilka_racuna" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" required>
                </div>
                <div>
                  <div class="flex justify-between items-end">
                    <label class="block text-sm font-medium text-gray-700">Partner (Stranka)</label>
                    <button @click="isPartnerModalOpen = true" type="button" class="text-xs text-blue-600 hover:text-blue-800 font-medium">+ Nova stranka</button>
                  </div>
                  <select v-model="formData.partner_id" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" required>
                    <option value="" disabled>Izberite stranko</option>
                    <option v-for="p in partnerji" :key="p.id" :value="p.id">
                      {{ p.naziv }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="mb-2 flex justify-between items-center">
                <h4 class="text-md font-medium text-gray-900">Postavke na računu</h4>
                <button @click="dodajPostavko" type="button" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                  + Dodaj vrstico
                </button>
              </div>

              <div v-if="formData.postavke.length === 0" class="text-center py-4 bg-gray-50 border border-gray-200 rounded-md text-gray-500 text-sm">
                Na računu še ni postavk.
              </div>

              <div v-else class="space-y-3">
                <div v-for="(postavka, index) in formData.postavke" :key="index" class="flex gap-3 items-end bg-gray-50 p-3 rounded-md border border-gray-200">
                  <div class="flex-grow">
                    <label class="block text-xs font-medium text-gray-500 mb-1">Artikel</label>
                    <select v-model="postavka.artikel_id" @change="onArtikelSelect(index)" class="block w-full px-2 py-1.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm" required>
                      <option value="" disabled>Izberite</option>
                      <option v-for="a in artikli" :key="a.id" :value="a.id">
                        {{ a.naziv }} (Zaloga: {{ a.trenutna_zaloga }})
                      </option>
                    </select>
                  </div>
                  <div class="w-24">
                    <label class="block text-xs font-medium text-gray-500 mb-1">Količina</label>
                    <input type="number" min="1" v-model="postavka.kolicina" class="block w-full px-2 py-1.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm" required>
                  </div>
                  <div class="w-32">
                    <label class="block text-xs font-medium text-gray-500 mb-1">Cena/kos (€)</label>
                    <input type="number" step="0.01" min="0" v-model="postavka.prodajna_cena" class="block w-full px-2 py-1.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm" required>
                  </div>
                  <div class="w-20">
                    <label class="block text-xs font-medium text-gray-500 mb-1">DDV (%)</label>
                    <input type="number" step="0.1" min="0" v-model="postavka.davek_procent" class="block w-full px-2 py-1.5 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm" required>
                  </div>
                  <div>
                    <button @click="odstraniPostavko(index)" type="button" class="p-1.5 text-red-600 hover:bg-red-100 rounded-md transition-colors" title="Odstrani">
                      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button @click="submitForm" :disabled="loading" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50">
            {{ loading ? 'Shranjevanje...' : 'Shrani osnutek' }}
          </button>
          <button @click="emit('close')" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
            Prekliči
          </button>
        </div>
      </div>
    </div>
    
    <PartnerModal 
      :is-open="isPartnerModalOpen"
      @close="isPartnerModalOpen = false"
      @success="handlePartnerSuccess"
    />
  </div>
</template>
