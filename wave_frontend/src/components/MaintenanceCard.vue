<template>
  <div class="row-span-1 col-span-2 flex align-middle rounded shadow-md text-left p-4 bg-white">
    <div class="p-4">
      <h2 class="text-2xl font-bold mb-3">Upcoming maintenance</h2>
      <div class="overflow-x-auto relative shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500 ">
          <tbody>
          <tr class="bg-white border-b hover:bg-gray-50">
            <th scope="row" class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap ">
              Engine overhaul and inspection.
            </th>
            <td class="py-4 px-6">
              <span class="bg-blue-100 text-blue-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded">Inspection</span>
              <span class="bg-gray-100 text-gray-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded">Repair</span>
            </td>
            <td class="py-4 px-6">
              24.12.2022
            </td>
          </tr>

          <tr class="bg-white border-b hover:bg-gray-50">
            <th scope="row" class="py-4 px-6 font-medium text-gray-900 whitespace-nowrap ">
              Paint the ship hull.
            </th>
            <td class="py-4 px-6">
              <span class="bg-gray-100 text-gray-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded">Repair</span>
            </td>
            <td class="py-4 px-6">
              29.12.2022
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <!--<p class="font-light text-md text-gray-500">No upcoming maintenance</p>-->
    </div>
  </div>
</template>

<script>
export default {
  name: "MaintenanceCard"
}
</script>

<style scoped>

</style>