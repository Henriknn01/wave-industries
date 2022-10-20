<template>
  <div class="flex bg-gray-100">
    <div class="flex flex-col w-80 h-screen px-4 py-8 overflow-y-auto">
      <div class="flex flex-col justify-between mt-6">
        <admin-nav-bar/>
      </div>
    </div>
    <div class="w-full h-full p-4 m-8 overflow-y-auto">
      <div class="grid grid-rows-5 grid-cols-4 gap-4">
        <div class="row-span-1 col-span-full bg-hero shadow-md bg-blend-darken bg-cover rounded bg-blur align-middle text-left flex">
          <div class="m-auto">
            <h1 class="text-5xl font-extrabold uppercase text-white">R/V Gunnerus</h1>
          </div>
        </div>
        <ShortInfoCard content="2000 kW h" description="Energy produced the last 24 hours"/>
        <ShortInfoCard content="100,000 Liters" description="Fuel consumed the last 24 hours"/>
        <ShortInfoCard content="1337 NM" description="Distance traveled the last 24 hours"/>
        <ShortInfoCard content="100 Tons" description="Co2 produced last 24 hours"/>

        <div class="row-span-3 col-span-2 rounded shadow-md text-left p-4 bg-white">
          <h2 class="text-2xl font-bold p-2">Fuel consumption <span class="text-sm font-light">(liters per hour)</span></h2>
          <div id="chart">
            <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>
          </div>
        </div>
        <div class="row-span-3 col-span-2 rounded shadow-md text-left p-4 bg-white">
          <h2 class="text-2xl font-bold p-2">Location <span class="font-light text-[0.7rem]">[LAT: 47.41322, LONG: -1.219482]</span></h2>
          <div style="height: 85%">
            <l-map ref="map h-" v-model:zoom="zoom" :center="[47.41322, -1.219482]">
              <l-tile-layer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  layer-type="base"
                  name="OpenStreetMap"
                  :max-zoom="10"
              />
            </l-map>
          </div>
        </div>
        <radial-chart-basic title="Fuel efficiency" value=100 chart-color="#00FF89"/>
        <radial-chart-basic title="Fuel level" value=15 chart-color="#FF3131"/>
        <maintenance-card/>
        <live-stats-card/>
        <ShortInfoCard content="210,320 Kr" description="NOx emissions tax so far"/>


        <ShortInfoCard content="410 L/nm" description="Liters per nauticle mile the last 24 hours"/>
        <ShortInfoCard content="153,102 Kr" description="Co2 emissions tax so far"/>


      </div>
    </div>
  </div>
</template>

<script>
import AdminNavBar from "@/components/AdminNavBar";
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
import ShortInfoCard from "@/components/ShortInfoCard";
import RadialChartBasic from "@/components/RadialChartBasic";
import MaintenanceCard from "@/components/MaintenanceCard";
import LiveStatsCard from "@/components/LiveStatsCard";

export default {
  name: "AdminView",
  components: {
    LiveStatsCard,
    MaintenanceCard,
    RadialChartBasic,
    ShortInfoCard,
    AdminNavBar,
    LMap,
    LTileLayer,
  },
  data: function() {
    return {
      series: [{
        name: 'Engine 1',
        data: [31, 40, 28, 51, 42, 109, 100]
      }, {
        name: 'Engine 2',
        data: [11, 32, 45, 32, 34, 52, 41]
      }],
      chartOptions: {
        chart: {
          height: 350,
          type: 'area'
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        xaxis: {
          type: 'datetime',
          categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
        },
        tooltip: {
          x: {
            format: 'dd/MM/yy HH:mm'
          },
        },
      },
      geojson: {
        type: "FeatureCollection",
        features: [
          // ...
        ],
      },
      geojsonOptions: {
        // Options that don't rely on Leaflet methods.
      },
      zoom: 2,
    }
  },
  async beforeMount() {
    this.mapIsReady = true;
  },
}
</script>

<style scoped>

</style>