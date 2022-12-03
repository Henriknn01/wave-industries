import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import {createRouter, createWebHashHistory} from 'vue-router';
import HomeView from "./views/HomeView";
import ShipDashboardView from "@/views/ShipDashboardView";
import VueApexCharts from 'vue3-apexcharts';
import tmpView from "@/views/tmpView";
import DashboardView from "@/views/DashboardView";

const routes = [
    { path: '/', name: 'home', component: HomeView },
    { path: '/dashboard', name: 'dahboard', component: DashboardView },
    { path: '/dashboard/:id', name: 'ship-dashboard', component: ShipDashboardView },
    { path: '/tmp', component: tmpView }
]

const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHashHistory(),
    routes, // short for `routes: routes`
})

const app = createApp(App)

app.config.globalProperties.api_url = "http://127.0.0.1:8000/"
app.use(VueApexCharts);
app.use(router)
//createApp(App)
app.mount('#app')
