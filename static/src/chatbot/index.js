import { createApp } from 'vue'
import '../style.css'
import App from './App.vue'
import axios from "axios"
import { createPinia } from 'pinia'
import piniaPluginPersistedState from "pinia-plugin-persistedstate"

// Enable CSRF cookie header for Django
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedState)
app.use(pinia)
// Mount chatbot app to its dedicated root element
app.mount('#chat-app')