export const useAuth = () => {
  const token = useCookie('token')
  const user = useCookie('user')

  const login = async (email, password) => {
    try {
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)

      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Prijava ni uspela. Preverite e-pošto in geslo.')
      }

      const data = await response.json()
      token.value = data.access_token
      user.value = data.user
      return true
    } catch (err) {
      console.error(err)
      return false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    navigateTo('/login')
  }

  const isLoggedIn = computed(() => !!token.value)
  
  const hasRole = (roles) => {
    if (!user.value) return false
    if (user.value.vloga === 'admin') return true
    return roles.includes(user.value.vloga)
  }

  return { token, user, login, logout, isLoggedIn, hasRole }
}
