import path from 'path'
import type { PluginOption } from 'vite'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

function setupPlugins(env: ImportMetaEnv): PluginOption[] {
  return [
    vue(),
    env.VITE_GLOB_APP_PWA === 'true' && VitePWA({
      injectRegister: 'auto',
      manifest: {
        name: 'chatGPT',
        short_name: 'chatGPT',
        icons: [
          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ]
}

export default defineConfig((env) => {
  const viteEnv = loadEnv(env.mode, process.cwd()) as unknown as ImportMetaEnv

  return {
    base: process.env.VITE_BASE || '/',
    resolve: {
      alias: {
        '@': path.resolve(process.cwd(), 'src'),
      },
    },
    plugins: setupPlugins(viteEnv),
    server: {
      host: '0.0.0.0',
      port: 1010,
      open: false,
      proxy: {
        // '/api': {
        //   target: 'http://120.133.83.144:7861',
        //   changeOrigin: true, // 允许跨域
        //   rewrite: path => path.replace('/api', ''),
        // },
        '/api': {
          target: 'http://120.133.63.166:9001/',
          changeOrigin: true, // 允许跨域
          // rewrite: path => path.replace('/api', ''),
        },
        // '/api': {
        //   target: 'http://172.22.220.21:5001/',
        //   changeOrigin: true, // 允许跨域
        //   // rewrite: path => path.replace('/api', ''),
        // },
      },
    },
    build: {
      reportCompressedSize: false,
      sourcemap: false,
      commonjsOptions: {
        ignoreTryCatch: false,
      },
    },
  }
})
