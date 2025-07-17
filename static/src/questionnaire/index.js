import { createApp } from 'vue'
import '../style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Overview from './Overview.vue'
import CategoryView from './CategoryView.vue'
import SubmissionSummary from './SubmissionSummary.vue';
import piniaPluginPersistedState from "pinia-plugin-persistedstate"
import axios from "axios"

// Enable CSRF cookie header for Django
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Define routes for the application
const routes = [
  { path: '/questionnaire', name: 'Overview', component: Overview },
  {
    path: '/questionnaire/category/:categoryId',
    name: 'CategoryView',
    component: CategoryView,
    props: true
  },
  { path: '/questionnaire/summary', name: 'SubmissionSummary', component: SubmissionSummary },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedState)
app.use(pinia)
// configure Vue Router to handle questionnaire routes
app.use(router)
app.mount('#questionnaire-app')