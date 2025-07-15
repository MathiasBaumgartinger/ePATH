import { defineConfig } from 'vite'
import { resolve } from 'path'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/static/",
  resolve: {
    alias: {
      // Map the virtual package name to your library folder
      '@epath/vue-questionnaire': resolve(__dirname, 'static/src/libs/questionnaire-forms/src'),
      vue: 'vue/dist/vue.esm-bundler.js',
    },
  },
  build: {
    manifest: "manifest.json",
    outDir: resolve("./assets"),
    assetsDir: "django-assets",
    rollupOptions: {
      input: {
        "test": resolve('./static/src/main.js') // Adjust the path to your main.js file
      }
    }
  }
})
