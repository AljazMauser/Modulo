<script setup>
defineProps({
  artikli: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['show-history'])
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Šifra</th>
          <th scope="col" class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Naziv</th>
          <th scope="col" class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cena</th>
          <th scope="col" class="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Trenutna Zaloga</th>
          <th scope="col" class="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Akcije</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-if="!artikli || artikli.length === 0">
          <td colspan="5" class="px-6 py-8 text-center text-gray-500">
            Ni najdenih artiklov. Dodajte jih v bazo!
          </td>
        </tr>
        <tr v-for="artikel in artikli" :key="artikel.id" class="hover:bg-gray-50 transition-colors">
          <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ artikel.sifra }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ artikel.naziv }}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{{ artikel.cena }} €</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-right">
            <span :class="[
              'px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
              artikel.trenutna_zaloga > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]">
              {{ artikel.trenutna_zaloga }} kos
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-right">
            <button 
              @click="emit('show-history', artikel)"
              class="text-blue-600 hover:text-blue-900 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-md font-medium transition-colors"
            >
              Zgodovina
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
