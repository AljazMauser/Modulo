export default defineNuxtPlugin((nuxtApp) => {
  const originalFetch = globalThis.fetch
  globalThis.fetch = async (url, options = {}) => {
    const token = useCookie('token')
    if (token.value) {
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token.value}`
      }
    }
    return originalFetch(url, options)
  }

  globalThis.$fetch = $fetch.create({
    onRequest({ request, options }) {
      const token = useCookie('token')
      if (token.value) {
        options.headers = options.headers || {}
        options.headers.Authorization = `Bearer ${token.value}`
      }
    }
  })
})
