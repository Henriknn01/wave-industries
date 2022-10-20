<template>
  <div class="row-span-1 col-span-2 rounded shadow-md text-left p-4 bg-white">
    <div class="p-4 ">
      <div class="relative inline-flex mb-5">
        <h2 class="text-2xl font-bold mb-3 pr-2">Live stats </h2>
        <span class="flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-red-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
        </span>
      </div>
      <div class="grid grid-rows-2 grid-cols-2 w-full h-full gap-4">
        <div class="row-span-1 col-span-1 flex align-middle">
          <div class="m-auto">
            <h1 class="text-xl"><span class="font-bold">Heading:</span> 178°</h1>
          </div>
        </div>
        <div class="row-span-1 col-span-1 flex align-middle">
          <div class="m-auto">
            <h1 class="text-xl"><span class="font-bold">Speed:</span> 10 knots</h1>
          </div>
        </div>
        <div class="row-span-1 col-span-1 flex align-middle">
          <div class="m-auto">
            <h1 class="text-xl"><span class="font-bold">Weather:</span> weather</h1>
          </div>
        </div>
        <div class="row-span-1 col-span-1 flex align-middle">
          <div class="m-auto">
            <h1 class="text-xl"><span class="font-bold">Destination:</span> unknown</h1>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LiveStatsCard",
}
</script>

<style scoped>

</style>