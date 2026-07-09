<script setup>
import { Bar, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { ref, computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

const selectedPeriod = ref('this_month')

const { data: kpi } = await useFetch('http://localhost:8000/api/dashboard/kpi', {
  query: { period: selectedPeriod }
})
const { data: charts } = await useFetch('http://localhost:8000/api/dashboard/charts', {
  query: { period: selectedPeriod }
})

const formatEur = (value) => {
  return new Intl.NumberFormat('sl-SI', { style: 'currency', currency: 'EUR' }).format(value || 0)
}

const barChartData = computed(() => ({
  labels: charts.value?.monthly_revenue?.labels || [],
  datasets: [{
    label: 'Prihodki',
    backgroundColor: '#3b82f6',
    data: charts.value?.monthly_revenue?.data || []
  }]
}))

const doughnutChartData = computed(() => ({
  labels: charts.value?.top_products?.labels || [],
  datasets: [{
    // Pastelne barve, rdeča je odstranjena
    backgroundColor: ['#93c5fd', '#86efac', '#fcd34d', '#c4b5fd', '#fbcfe8'],
    data: charts.value?.top_products?.data || []
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
      <h1 class="text-3xl font-bold text-gray-900">Nadzorna plošča</h1>
      
      <!-- Časovni filter -->
      <div>
        <select v-model="selectedPeriod" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md shadow-sm">
          <option value="this_month">Ta mesec</option>
          <option value="90days">Zadnjih 90 dni</option>
          <option value="this_year">Letos</option>
        </select>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500 flex justify-between items-center">
        <div>
          <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Vrednost zaloge</h3>
          <p class="mt-2 text-3xl font-bold text-gray-900">{{ formatEur(kpi?.vrednost_zaloge) }}</p>
        </div>
        <div class="text-blue-500 bg-blue-50 p-3 rounded-full">
          <!-- Ikona Škatla/Skladišče -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-green-500 flex justify-between items-center">
        <div>
          <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Prihodki ({{ selectedPeriod === 'this_month' ? 'Ta mesec' : (selectedPeriod === '90days' ? 'Zadnjih 90 dni' : 'Letos') }})</h3>
          <p class="mt-2 text-3xl font-bold text-gray-900">{{ formatEur(kpi?.prihodki_mesec) }}</p>
        </div>
        <div class="text-green-500 bg-green-50 p-3 rounded-full">
          <!-- Ikona Graf rasti -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-red-500 flex justify-between items-center">
        <div>
          <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Neplačani računi</h3>
          <p class="mt-2 text-3xl font-bold text-gray-900">{{ kpi?.neplacani_racuni || 0 }}</p>
        </div>
        <div class="text-red-500 bg-red-50 p-3 rounded-full">
          <!-- Ikona Opozorilo -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
      </div>

    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <!-- Bar Chart: Monthly Revenue -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Mesečni prihodki ({{ selectedPeriod === 'this_month' ? 'Zadnjih 6 mesecev' : (selectedPeriod === '90days' ? 'Zadnji 3 meseci' : 'Letos') }})</h3>
        <div class="h-64">
          <Bar :data="barChartData" :options="chartOptions" />
        </div>
      </div>

      <!-- Doughnut Chart: Top 5 Items -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Top 5 Najbolj Prodajanih Artiklov</h3>
        <div class="h-64 flex justify-center">
          <Doughnut :data="doughnutChartData" :options="chartOptions" />
        </div>
      </div>

    </div>
  </div>
</template>
