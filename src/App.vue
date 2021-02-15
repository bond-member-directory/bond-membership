<template>
  <PageHeader />
  <DataFilters />
  <div class="w-100">
    <div class="w-50 fl">
      <CardContainer />
    </div>
    <div class="w-50 fl">
      <MapContainer />
    </div>
  </div>
</template>

<script>
import PageHeader from './components/PageHeader.vue'
import DataFilters from './components/DataFilters.vue'
import CardContainer from './components/CardContainer.vue'
import MapContainer from './components/MapContainer.vue'
import world from './assets/world.json';
import members from './assets/bond_members.json'

export default {
  name: 'App',
  provide() {
    world.features = world.features.filter((b) => b.properties['ISO_A2'] != 'AQ');
    return {
      world: world,
      countries: Object.fromEntries(
        world.features.map((c) => [c.properties['ISO_A2'], c.properties['NAME_EN']])
      ),
      sdgs: members.sdgs,
      members: Object.values(members.members)
        .sort((a, b) => a.name.replace(/^(the )/i, "") > b.name.replace(/^(the )/i, "")),
    }
  },
  components: {
    PageHeader,
    CardContainer,
    MapContainer,
    DataFilters,
  }
}
</script>
