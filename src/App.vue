<template>
  <div class="w-100 white bg-bond-darkest-red pa3 tc"><strong>!! Work in Progress !!</strong></div>
  <PageHeader />
  <div class="w-100 ph4">
    <a href="#" @click.prevent="showMap = !showMap" class="fr bond-dark-blue link underline f5"><template v-if="showMap">Hide map</template><template v-else>Show map</template></a>
  </div>
  <div class="w-100">
    <div class="fl" :class="{ 'w-50': showMap }">
      <CardContainer />
    </div>
    <div class="fl w-50" v-if="showMap">
      <MapContainer />
    </div>
  </div>
</template>

<script>
import PageHeader from './components/PageHeader.vue'
import CardContainer from './components/CardContainer.vue'
import MapContainer from './components/MapContainer.vue'
import world from './assets/world.json';
import members from './assets/bond_members.json'

export default {
  name: 'App',
  data: function(){
    return {
      showMap: false,
    }
  },
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
  }
}
</script>
