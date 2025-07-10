// middleware/auth.global.ts
export default defineNuxtRouteMiddleware((to) => {
  const publicPages = ['/login', '/register']
  const userStore = useUserStore()

  if (process.client) {
    userStore.loadFromToken()

    const hasToken = localStorage.getItem('access_token')
    const isAuthenticated = userStore.isAuthenticated

    if (!hasToken || !isAuthenticated) {
      if (!publicPages.includes(to.path)) {
        return navigateTo('/login')
      }
    }
  }
})
