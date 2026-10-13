export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  
  try {
    // Trigger Figma import
    const response = await $fetch('/api/figma/import', { method: 'POST' })
    
    return {
      status: 'success',
      message: 'Sync started',
      imported: response.imported
    }
  } catch (err) {
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to sync from Figma'
    })
  }
})
