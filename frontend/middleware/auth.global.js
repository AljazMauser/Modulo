export default defineNuxtRouteMiddleware((to, from) => {
  // Če ne deluje v brskalniku, preskočimo
  if (process.server) return

  const { isLoggedIn } = useAuth()
  
  if (!isLoggedIn.value && to.path !== '/login') {
    return navigateTo('/login')
  }

  if (isLoggedIn.value && to.path === '/login') {
    return navigateTo('/')
  }
})
