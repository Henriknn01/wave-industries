import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import {createRouter, createWebHashHistory} from 'vue-router';
import HomeView from "./views/HomeView";
import AdminView from "@/views/AdminView";
import VueApexCharts from 'vue3-apexcharts';

const routes = [
    { path: '/', component: HomeView },
    { path: '/admin/', component: AdminView },
]

const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

const app = createApp(App)
app.use(VueApexCharts);
app.use(router)
//createApp(App)
app.mount('#app')
