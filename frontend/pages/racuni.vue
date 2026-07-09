<script setup>
import { ref } from 'vue'

const { data: racuni, refresh: refreshRacuni } = await useFetch('/api/racuni')
const isInvoiceModalOpen = ref(false)

const handleInvoiceSuccess = () => {
  refreshRacuni()
  isInvoiceModalOpen.value = false
}

const potrdiRacun = async (id) => {
  try {
    const res = await fetch(`/api/racuni/${id}/potrdi`, {
      method: 'PUT'
    })
    if (!res.ok) {
      const data = await res.json()
      alert('Napaka: ' + data.detail)
    } else {
      refreshRacuni()
      alert('Račun uspešno potrjen! Zaloga je zmanjšana.')
    }
  } catch (err) {
    alert('Napaka na omrežju.')
  }
}
</script>

<template>
  <div class="p-8 max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Prodaja in Računi</h1>
        <p class="text-gray-500 mt-1">Pregled izdanih računov in dodajanje novih</p>
      </div>
      <button 
        @click="isInvoiceModalOpen = true"
        class="bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-lg font-medium shadow-sm transition-colors"
      >
        + Nov Račun
      </button>
    </div>

    <!-- Tabela računov -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Številka</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Datum</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Znesek</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase">Akcije</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="!racuni || racuni.length === 0">
            <td colspan="5" class="px-6 py-8 text-center text-gray-500">
              Ni najdenih računov.
            </td>
          </tr>
          <tr v-for="racun in racuni" :key="racun.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-medium">{{ racun.stevilka_racuna }}</td>
            <td class="px-6 py-4 text-gray-600">{{ new Date(racun.datum_izdaje).toLocaleDateString('sl-SI') }}</td>
            <td class="px-6 py-4 font-bold">{{ racun.skupni_znesek }} €</td>
            <td class="px-6 py-4">
              <span :class="[
                'px-2 py-1 inline-flex text-xs font-semibold rounded-full',
                racun.status === 'potrjeno' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
              ]">
                {{ racun.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-right">
              <button 
                v-if="racun.status === 'osnutek'"
                @click="potrdiRacun(racun.id)"
                class="text-green-600 hover:text-green-900 bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-md font-medium mr-2"
              >
                Potrdi
              </button>
              <a 
                :href="`/api/racuni/${racun.id}/pdf`" 
                target="_blank"
                class="inline-block text-blue-600 hover:text-blue-900 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-md font-medium"
              >
                Poglej PDF
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal za nov račun -->
    <InvoiceModal 
      :is-open="isInvoiceModalOpen"
      @close="isInvoiceModalOpen = false"
      @success="handleInvoiceSuccess"
    />
  </div>
</template>
