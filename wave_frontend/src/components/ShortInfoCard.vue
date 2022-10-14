<template>
  <div class="col-span-1 flex align-middle rounded shadow-md p-4 bg-white">
    <div class="m-auto">
      <h3 class="text-2xl font-bold">{{ content }}</h3>
      <p class="text-gray-400 font-light">{{ description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ShortInfoCard",
  props: {
    content: String,
    description: String,
  }
}
</script>

<style scoped>

</style>