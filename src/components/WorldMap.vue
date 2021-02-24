<template>
  <div ref="worldmap" style="width: 100%">
    <svg :width="width" :height="height">
      <g class="dark-shadow">
        <map-country
          v-for="p in paths"
          :path="p[1]"
          :countryProps="p[0]"
          :key="p"
          :countrySelected="Object.keys(countryValues).includes(p[0].ISO_A2)"
          :defaultClasses="defaultClasses"
          :selectedClasses="selectedClasses"
        />
      </g>
    </svg>
  </div>
</template>

<script>
const d3 = { ...require("d3"), ...require("d3-geo") };

import MapCountry from "./MapCountry.vue";

export default {
  name: "WorldMap",
  inject: ["world"],
  props: {
    center: {
      type: Array,
      default: () => [33.561041, -7.584838],
    },
    scale: {
      type: [Number, String],
      default: 1 << 20,
    },
    countryValues: {
      type: Object,
      default: () => {},
    },
    defaultClasses: {
      type: Array,
      default: () => ['fill-bond-grey', 'stroke-bond-grey'],
    },
    selectedClasses: {
      type: Array,
      default: () => ['fill-bond-dark-red', 'stroke-bond-dark-red'],
    },
    hoveredClasses: {
      type: Array,
      default: () => ['fill-bond-red', 'stroke-bond-red'],
    },
  },
  data() {
    return {
      width: null,
      height: null,
      projection: null,
      geoGenerator: null,
      paths: [],
      selectedCountry: null,
      hoveredCountry: null,
      fieldToUse: "REGION_WB",
      zoomLevel: 0,
    };
  },
  //   computed: {
  //     selectedCountryName: function(){
  //       if(!this.selectedCountry){
  //         return null;
  //       } else if(this.zoomLevel > 1){
  //         return this.selectedCountry["NAME_EN"];
  //       } else {
  //         return this.selectedCountry[this.fieldToUse];
  //       }
  //     },
  //   },
  methods: {
    onResize: function () {
      const { width } = this.$refs.worldmap.getBoundingClientRect();
      this.width = width;
      this.height = width / 2;
      this.projection = d3
        .geoNaturalEarth1()
        .fitSize([this.width, this.height], this.world);
      this.geoGenerator = d3.geoPath().projection(this.projection);
      this.paths = this.world.features.map((b) => [
        b.properties,
        this.geoGenerator(b),
      ]);
    },
    // countryIsSelected: function(country){
    //   if(!this.selectedCountry){
    //     return false;
    //   } else if(this.zoomLevel > 1){
    //     return this.selectedCountry["NAME_EN"] == country["NAME_EN"];
    //   } else {
    //     return this.selectedCountry[this.fieldToUse] == country[this.fieldToUse];
    //   }
    // },
    // countryIsHovered: function(country){
    //   if(!this.hoveredCountry){
    //     return false;
    //   } else if(this.zoomLevel > 0){
    //     return this.hoveredCountry["NAME_EN"] == country["NAME_EN"];
    //   } else {
    //     return this.hoveredCountry[this.fieldToUse] == country[this.fieldToUse];
    //   }
    // },
    // zoomMap: function(country){
    //   this.selectedCountry = country;
    //   var countries = this.world.features;
    //   if(country != null){
    //     if(this.zoomLevel>=1){
    //       countries = this.world.features.filter(
    //         (c) => c.properties['ISO_A2'] == country['ISO_A2']
    //       );
    //       this.zoomLevel = 2;
    //       filterStore.setCountry(country['ISO_A2']);
    //     } else {
    //       countries = this.world.features.filter(
    //         (c) => (
    //           c.properties[this.fieldToUse] == country[this.fieldToUse] &&
    //           c.properties['POP_EST'] >= 1000000 &&
    //           !["GL", "RU"].includes(c.properties['ISO_A2'])
    //         )
    //       );
    //       this.zoomLevel = 1;
    //     }
    //   } else {
    //     this.zoomLevel = 0;
    //   }
    //   this.projection.fitSize([this.width, this.height], {
    //     type: "FeatureCollection",
    //     features: countries,
    //   });
    //   this.paths = this.world.features.map((b) => [b.properties, this.geoGenerator(b)]);
    // },
  },
  mounted() {
    this.onResize();
    window.addEventListener("resize", this.onResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.onResize);
  },
  components: {
    MapCountry,
  },
};
</script>

<style scoped>
.map {
  width: 100%;
  height: 100%;
}
.light-shadow {
  filter: drop-shadow(0px 3px 3px rgba(0, 0, 0, 0.4));
}
.dark-shadow {
  filter: drop-shadow(0px 3px 3px rgba(0, 0, 0, 1));
}
</style>