<template>
  <div class="flex bg-gray-100">
    <div class="flex flex-col w-80 h-screen px-4 py-8 overflow-y-auto">
      <div class="flex flex-col justify-between mt-6">
        <admin-nav-bar/>
      </div>
    </div>
    <div class="w-full h-full p-4 m-8 overflow-y-auto">
      <div class="grid grid-cols-3 gap-4">
        <div v-for="ship in ships" :key="ship.id">
        <router-link :to="{ name: 'ship-dashboard', params: {id: ship.id}}">
          <div class="max-w-sm rounded overflow-hidden shadow-lg bg-white">
            <img class="w-full" :src="ship.picture_url" alt="Sunset in the mountains">
            <div class="px-6 py-4">
              <div class="font-bold text-xl">{{ ship.name }}</div>
            </div>
            <div class="px-6 pb-2">
              <button class="relative w-full inline-flex items-center justify-center p-0.5 mb-2 mr-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 ">
                <span class="relative w-full px-5 py-2.5 transition-all ease-in duration-75 bg-white rounded-md group-hover:bg-opacity-0">
                    View
                </span>
              </button>
            </div>
          </div>
        </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminNavBar from "@/components/AdminNavBar";
import axios from 'axios';

export default {
  name: "DashboardView",
  components: {
    AdminNavBar,
  },
  mounted() {
    axios.get(this.api_url+"ships/?format=json",)
        .then(response => {
          this.ships = response.data.results;
        }).catch(error => {
          console.log(error)
    })
  },
  data: function () {
    return {
      ships: []
    }
  }
}
</script>

<style scoped>

</style>