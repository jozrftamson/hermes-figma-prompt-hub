/**
 * Utility functions for validation and data manipulation
 */

export const validators = {
  isValidPromptId: (id: string): boolean => {
    return /^[a-z0-9\-_]+$/.test(id) && id.length >= 3 && id.length <= 100
  },

  isValidEmail: (email: string): boolean => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  },

  isValidUrl: (url: string): boolean => {
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  },

  isValidJSON: (str: string): boolean => {
    try {
      JSON.parse(str)
      return true
    } catch {
      return false
    }
  }
}

export const formatters = {
  truncate: (str: string, length: number = 100): string => {
    return str.length > length ? str.substring(0, length) + '...' : str
  },

  formatDate: (date: Date | string): string => {
    const d = new Date(date)
    return d.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  },

  formatTime: (ms: number): string => {
    if (ms < 1000) return `${ms}ms`
    return `${(ms / 1000).toFixed(2)}s`
  }
}
