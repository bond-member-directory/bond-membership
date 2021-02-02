<template>
  <svg :width="width" :height="width">
    <map-country 
      v-for="p in paths"
      :path="p[1]"
      :countryProps="p[0]"
      :key="p"
      @select-country="selectedCountry = $event"
      :countrySelected="selectedCountry && selectedCountry[fieldToUse] == p[0][fieldToUse]" />
  </svg>
  <p class="pa3 bg-red white" v-if="selectedCountry && selectedCountry[fieldToUse]">{{ selectedCountry[fieldToUse] }}</p>
</template>

<script>
const d3 = { ...require('d3'), ...require('d3-geo') };

import MapCountry from './MapCountry.vue'

export default {
  name: 'MapContainer',
  props: {
    center: {
      type: Array,
      default: () => [33.561041, -7.584838],
    },
    scale: {
      type: [Number, String],
      default: 1 << 20,
    },
    world: {},
  },
  data () {
    return {
      width: 600,
      height: 400,
      projection: null,
      paths: [],
      selectedCountry: null,
      fieldToUse: 'REGION_WB',
    };
  },
  mounted () {
    this.projection = d3.geoNaturalEarth1()
      .fitSize([this.width, this.height], this.world);
    var geoGenerator = d3.geoPath()
      .projection(this.projection)
    this.paths = this.world.features.map((b) => [b.properties, geoGenerator(b)]);
  },
  components: {
    MapCountry
  },
};
</script>

<style scoped>
.map {
  width: 100%;
  height: 100%;
}
</style>