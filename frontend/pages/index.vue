<script setup>
import { Bar, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'
import { ref } from 'vue'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

const { data: kpi, error: kpiError } = await useFetch('http://localhost:8000/api/dashboard/kpi')
const { data: charts, error: chartError } = await useFetch('http://localhost:8000/api/dashboard/charts')

const formatEur = (value) => {
  return new Intl.NumberFormat('sl-SI', { style: 'currency', currency: 'EUR' }).format(value || 0)
}

const barChartData = ref({
  labels: charts.value?.monthly_revenue?.labels || [],
  datasets: [{
    label: 'Prihodki',
    backgroundColor: '#3b82f6',
    data: charts.value?.monthly_revenue?.data || []
  }]
})

const doughnutChartData = ref({
  labels: charts.value?.top_products?.labels || [],
  datasets: [{
    backgroundColor: ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6'],
    data: charts.value?.top_products?.data || []
  }]
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Nadzorna plošča</h1>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      
      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
        <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Vrednost zaloge</h3>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ formatEur(kpi?.vrednost_zaloge) }}</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
        <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Prihodki (ta mesec)</h3>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ formatEur(kpi?.prihodki_mesec) }}</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6 border-l-4 border-red-500">
        <h3 class="text-sm font-medium text-gray-500 uppercase tracking-wider">Neplačani računi</h3>
        <p class="mt-2 text-3xl font-bold text-gray-900">{{ kpi?.neplacani_racuni || 0 }}</p>
      </div>

    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <!-- Bar Chart: Monthly Revenue -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Mesečni prihodki (Zadnjih 6 mesecev)</h3>
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
