export default defineNuxtRouteMiddleware((to, from) => {
  // Če ne deluje v brskalniku, preskočimo
  if (process.server) return

  const { isLoggedIn, hasRole } = useAuth()
  
  if (!isLoggedIn.value && to.path !== '/login') {
    return navigateTo('/login')
  }

  if (isLoggedIn.value && to.path === '/login') {
    return navigateTo('/')
  }

  // Prepreči dostop do Nadzorne plošče (/) za ne-admine
  if (isLoggedIn.value && to.path === '/' && !hasRole(['admin'])) {
    return navigateTo('/zaloga')
  }
})
