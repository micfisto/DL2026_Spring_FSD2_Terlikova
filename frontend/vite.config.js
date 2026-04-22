import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '', '')

  return {
    plugins: [react()],
    base: '/',

    build: {
      outDir: 'dist',
      emptyOutDir: true,
    },

    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(
        env.VITE_API_URL || 'http://localhost:8000'
      ),
    },
  }
})