<template>
  <div class="row-span-1 col-span-1 flex align-middle rounded shadow-md text-left p-4 bg-white">
    <div class="m-auto">
      <div id="chart">
        <apexchart type="radialBar" height="350" :options="chartOptions" :series="[value]"></apexchart>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RadialChartBasic",
  props: {
    title: String,
    value: Array,
    chartColor: String,
  },
  data: function () {
    return {
      series: [this.value],
      chartOptions: {
        chart: {
          height: 350,
          type: 'radialBar',
        },
        plotOptions: {
          radialBar: {
            startAngle: -135,
            endAngle: 225,
            hollow: {
              margin: 0,
              size: '70%',
              background: '#fff',
              image: undefined,
              imageOffsetX: 0,
              imageOffsetY: 0,
              position: 'front',
              dropShadow: {
                enabled: true,
                top: 3,
                left: 0,
                blur: 4,
                opacity: 0.24
              }
            },
          },
        },
        fill: {
          type: 'solid',
          colors: [this.chartColor],
        },
        labels: [this.title],
        stroke: {
          lineCap: 'round'
        },
      },
    }
  },
}
</script>

<style scoped>

</style>