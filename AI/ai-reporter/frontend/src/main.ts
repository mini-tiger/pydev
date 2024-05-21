import { createApp } from 'vue'
import App from './App.vue'
import { setupI18n } from './locales'
import { setupAssets, setupScrollbarStyle } from './plugins'
import { setupStore } from './store'
import { setupRouter } from './router'
import 'element-plus/dist/index.css'
async function bootstrap() {
  const app = createApp(App)

	// 设置页面标题
	document.title = import.meta.env.VITE_APP_TITLE

	// 动态加载 CSS 文件
	const link = document.createElement('link');
	link.rel = 'icon';
	link.type = 'image/svg+xml'
	link.href = import.meta.env.VITE_APP_TABLE_ICON;
	document.head.appendChild(link);

  setupAssets()

  setupScrollbarStyle()

  setupStore(app)

  setupI18n(app)

  await setupRouter(app)

  app.mount('#app')
}

bootstrap()
