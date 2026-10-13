export const usePrompts = defineStore('prompts', () => {
  const prompts = ref<any[]>([])
  const selectedPrompt = ref<any>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchPrompts = async () => {
    loading.value = true
    try {
      const response = await $fetch('/api/prompts')
      prompts.value = response
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch prompts'
    } finally {
      loading.value = false
    }
  }

  const selectPrompt = (prompt: any) => {
    selectedPrompt.value = prompt
  }

  const createPrompt = async (promptData: any) => {
    try {
      const response = await $fetch('/api/prompts', {
        method: 'POST',
        body: promptData
      })
      prompts.value.push(response)
      return response
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create prompt'
      throw err
    }
  }

  const updatePrompt = async (id: string, promptData: any) => {
    try {
      const response = await $fetch(`/api/prompts/${id}`, {
        method: 'PUT',
        body: promptData
      })
      const index = prompts.value.findIndex(p => p.prompt_id === id)
      if (index !== -1) {
        prompts.value[index] = response
      }
      return response
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update prompt'
      throw err
    }
  }

  const deletePrompt = async (id: string) => {
    try {
      await $fetch(`/api/prompts/${id}`, { method: 'DELETE' })
      prompts.value = prompts.value.filter(p => p.prompt_id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete prompt'
      throw err
    }
  }

  return {
    prompts,
    selectedPrompt,
    loading,
    error,
    fetchPrompts,
    selectPrompt,
    createPrompt,
    updatePrompt,
    deletePrompt
  }
})
