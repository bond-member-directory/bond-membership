<template>
  <PageHeader />
  <div class="w-100">
    <div class="w-25 fl">
      <CardContainer :countries="countries" />
    </div>
    <div class="w-75 fl">
      <MapContainer :world="world" />
    </div>
  </div>
</template>

<script>
import PageHeader from './components/PageHeader.vue'
import CardContainer from './components/CardContainer.vue'
import MapContainer from './components/MapContainer.vue'
import world from './assets/world.json';

export default {
  name: 'App',
  data () {
    return {
      world: world,
      countries: Object.fromEntries(
        world.features.map((c) => [c.properties['ISO_A2'], c.properties['NAME_EN']])
      ),
    };
  },
  components: {
    PageHeader,
    CardContainer,
    MapContainer,
  }
}
</script>
