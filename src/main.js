import { createApp } from 'vue'
import App from './App.vue'
import 'tachyons/css/tachyons.min.css'
import router from './router'

createApp(App).use(router).mount('#app')
