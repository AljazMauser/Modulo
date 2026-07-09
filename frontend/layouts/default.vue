<script setup>
const auth = useAuth()
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Navbar -->
    <nav class="bg-blue-600 text-white shadow-md">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 font-bold text-xl tracking-wide">
              Modulo
            </div>
            <div class="ml-10 flex items-baseline space-x-4">
              <NuxtLink 
                v-if="auth.hasRole(['admin'])"
                to="/" 
                class="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-500 transition-colors"
                active-class="bg-blue-700"
              >
                Nadzorna plošča
              </NuxtLink>
              <NuxtLink 
                to="/zaloga" 
                class="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-500 transition-colors"
                active-class="bg-blue-700"
              >
                Upravljanje zalog
              </NuxtLink>
              <NuxtLink 
                v-if="auth.hasRole(['prodajalec'])"
                to="/racuni" 
                class="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-500 transition-colors"
                active-class="bg-blue-700"
              >
                Prodaja
              </NuxtLink>
              <NuxtLink 
                v-if="auth.hasRole(['skladiscnik'])"
                to="/nabava" 
                class="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-500 transition-colors"
                active-class="bg-blue-700"
              >
                Nabava
              </NuxtLink>
              <NuxtLink 
                v-if="auth.hasRole(['admin'])"
                to="/kadri" 
                class="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-500 transition-colors"
                active-class="bg-blue-700"
              >
                Kadri
              </NuxtLink>
            </div>
          </div>
          <div class="flex items-center gap-4" v-if="auth.isLoggedIn.value && auth.user.value">
            <div class="text-sm">
              Prijavljen kot: <b>{{ auth.user.value.ime }} {{ auth.user.value.priimek }}</b> ({{ auth.user.value.vloga }})
            </div>
            <button @click="auth.logout" class="bg-white text-blue-600 hover:bg-gray-100 px-3 py-1.5 rounded-md text-sm font-medium transition-colors">
              Odjava
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <main class="flex-grow">
      <slot />
    </main>
    
    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="max-w-6xl mx-auto px-4 py-4 text-center text-sm text-gray-500">
        &copy; 2026 Modulo
      </div>
    </footer>
  </div>
</template>
