import { createApp } from 'vue'
// import App from './App.vue'
// main.js
import './assets/main.css'
import router from './router'
import MainApp from './MainApp.vue'
createApp(MainApp).use(router).mount('#app')

