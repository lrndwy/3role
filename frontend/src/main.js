import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
//in your `main.js` file
import '../node_modules/flowbite-vue/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')
