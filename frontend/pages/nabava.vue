<script setup>
import { ref } from 'vue'

const { data: narocila, refresh: refreshNarocila } = await useFetch('http://localhost:8000/api/nabava')
const isPOModalOpen = ref(false)

const handlePOSuccess = () => {
  refreshNarocila()
  isPOModalOpen.value = false
}

const potrdiPrejem = async (id) => {
  if(!confirm('Ali ste prepričani, da ste prejeli blago? Zaloga in nabavne cene se bodo posodobile.')) return;
  
  try {
    const res = await fetch(`http://localhost:8000/api/nabava/${id}/potrdi_prejem`, {
      method: 'PUT'
    })
    if (!res.ok) {
      const data = await res.json()
      alert('Napaka: ' + data.detail)
    } else {
      refreshNarocila()
      alert('Prejem uspešno potrjen! Zaloga je posodobljena.')
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
        <h1 class="text-3xl font-bold text-gray-900">Nabava</h1>
        <p class="text-gray-500 mt-1">Pregled nabavnih naročil in prevzem blaga od dobaviteljev</p>
      </div>
      <button 
        @click="isPOModalOpen = true"
        class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium shadow-sm transition-colors"
      >
        + Novo Naročilo
      </button>
    </div>

    <!-- Tabela nabavnih naročil -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Številka</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Datum naročila</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase">Akcije</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="!narocila || narocila.length === 0">
            <td colspan="4" class="px-6 py-8 text-center text-gray-500">
              Ni najdenih nabavnih naročil.
            </td>
          </tr>
          <tr v-for="nar in narocila" :key="nar.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-medium">{{ nar.stevilka_narocila }}</td>
            <td class="px-6 py-4 text-gray-600">{{ new Date(nar.datum_narocila).toLocaleDateString('sl-SI') }}</td>
            <td class="px-6 py-4">
              <span :class="[
                'px-2 py-1 inline-flex text-xs font-semibold rounded-full',
                nar.status === 'prejeto' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
              ]">
                {{ nar.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-right">
              <button 
                v-if="nar.status === 'odprto'"
                @click="potrdiPrejem(nar.id)"
                class="text-green-600 hover:text-green-900 bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-md font-medium"
              >
                Potrdi Prejem
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal za novo naročilo -->
    <PurchaseOrderModal 
      :is-open="isPOModalOpen"
      @close="isPOModalOpen = false"
      @success="handlePOSuccess"
    />
  </div>
</template>
