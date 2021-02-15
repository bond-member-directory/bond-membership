<template>
  <header class="w-100 bg-white">
    <div class="w-100 pv2 ph4 flex items-center f4">
        <img alt="Bond logo" src="../assets/logo.png" class="w5">
        <h1 class="bond-dark-red ml5 header-text">Membership directory</h1>
    </div>
    <DataFilters />
  </header>
</template>

<script>
import DataFilters from './DataFilters.vue'

export default {
  name: 'PageHeader',
  components: {
    DataFilters,
  },
}
</script>

<style scoped>
.header-text {
  padding-top: 30px;
}
</style>