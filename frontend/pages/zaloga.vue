<script setup>
import { ref } from 'vue'

const { data: artikli, refresh } = await useFetch('/api/artikli')

const isMovementModalOpen = ref(false)
const isArticleModalOpen = ref(false)
const isHistoryModalOpen = ref(false)
const selectedArtikel = ref(null)

const handlePremikSuccess = () => {
  refresh() // Ponovno naloži artikle po uspešnem premiku
  isMovementModalOpen.value = false
}

const handleArtikelSuccess = () => {
  refresh() // Ponovno naloži artikle po uspešnem dodajanju
  isArticleModalOpen.value = false
}

const handleShowHistory = (artikel) => {
  selectedArtikel.value = artikel
  isHistoryModalOpen.value = true
}
</script>

<template>
  <div class="min-h-screen p-8 bg-gray-50">
    <div class="max-w-6xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Upravljanje zalog</h1>
          <p class="text-gray-500 mt-1">Pregled artiklov in ustvarjanje premikov</p>
        </div>
        <div class="flex space-x-3">
          <button 
            @click="isArticleModalOpen = true"
            class="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-5 py-2.5 rounded-lg font-medium shadow-sm transition-colors"
          >
            + Nov Artikel
          </button>
          <button 
            @click="isMovementModalOpen = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium shadow-sm transition-colors"
          >
            + Nov Premik
          </button>
        </div>
      </div>

      <InventoryTable 
        :artikli="artikli" 
        @show-history="handleShowHistory"
      />
      
      <MovementModal 
        :is-open="isMovementModalOpen" 
        :artikli="artikli"
        @close="isMovementModalOpen = false"
        @success="handlePremikSuccess"
      />

      <ArticleModal 
        :is-open="isArticleModalOpen"
        @close="isArticleModalOpen = false"
        @success="handleArtikelSuccess"
      />

      <HistoryModal
        :is-open="isHistoryModalOpen"
        :artikel="selectedArtikel"
        @close="isHistoryModalOpen = false"
      />
    </div>
  </div>
</template>
