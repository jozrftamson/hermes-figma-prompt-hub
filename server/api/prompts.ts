export default defineEventHandler(async (event) => {
  // Mock API - replace with actual database calls
  const prompts = [
    {
      prompt_id: 'cot-analysis',
      name: 'Chain of Thought Analysis',
      description: 'Structured step-by-step analysis',
      version: 'v1',
      strategy: 'chain-of-thought',
      category: 'analysis',
      system: 'You are a step-by-step analytical thinker...',
      user_template: 'Analyze this problem in 5 steps: {{problem}}',
      examples: [
        {
          input: 'Why do users churn?',
          output: '1. Data collection... 2. Trend analysis...'
        }
      ]
    }
  ]
  
  return prompts
})
