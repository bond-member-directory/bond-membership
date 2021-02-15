<template>
  <header class="w-100 bg-white">
    <div class="w-100 pb2 pt3 ph4 f4">
        <img alt="Bond logo" src="../assets/logo.png" class="w5">
        <h1 class="bond-mid-grey ml5 header-text fr normal f1">Membership directory</h1>
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
  font-weight: 200;
  /* padding-top: 30px; */
}
</style>