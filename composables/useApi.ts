/**
 * Composable for handling API calls with error management
 */
export const useApi = () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetch = async (url: string, options: any = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await $fetch(url, {
        ...options,
        onRequest({ request, options }) {
          // Add auth headers if needed
        },
        onError({ data, response, status, error }) {
          error.value = data?.message || `Error ${status}`
        }
      })
      return response
    } catch (err: any) {
      error.value = err.message
      console.error(`API Error [${url}]:`, err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    fetch,
    loading: readonly(loading),
    error: readonly(error)
  }
}
