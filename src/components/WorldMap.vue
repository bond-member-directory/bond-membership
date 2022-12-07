<template>
  <figure ref="worldmap" class="ma0" style="width: 100%;">
    <svg :width="width" :height="height">
      <title>{{ alt }}</title>
      <g class="dark-shadow">
        <map-country
          v-for="p in unSelectedPaths"
          :path="p[1]"
          :key="p"
          :style="countryStyle(p[0])"
          @mousemove='onHover($event, p[0])'
          @mouseleave="leaveHover"
          @click="$emit('select-country', p[0])"
        />
        <map-country
          v-for="p in selectedPaths"
          :path="p[1]"
          :key="p"
          :style="countryStyle(p[0])"
          @mousemove='onHover($event, p[0])'
          @mouseleave="leaveHover"
          @click="$emit('select-country', p[0])"
        />
      </g>
    </svg>
    <WorldMapTooltip
      v-if="mouseLocation"
      :x="mouseLocation.x"
      :y="mouseLocation.y"
      :title="tooltipText"
    />
  </figure>
</template>

<script>
const d3 = { ...require("d3"), ...require("d3-geo") };

import MapCountry from "./MapCountry.vue";
import WorldMapTooltip from "./WorldMapTooltip.vue";

export default {
  name: "WorldMap",
  inject: ["world"],
  props: {
    center: {
      type: Array,
      default: () => [33.561041, -7.584838],
    },
    alt: {
      type: String,
      default: () => '',
    },
    scale: {
      type: [Number, String],
      default: 1 << 20,
    },
    countryValues: {
      type: Map,
      default: () => (new Map()),
    },
    selectedCountry: {
      type: Array,
      default: () => [],
    },
    colourScaleColours: {
      type: Array,
      default: () => ["white", "blue"],
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
      hoveredCountry: null,
      fieldToUse: "REGION_WB",
      zoomLevel: 0,
      mouseLocation: null,
      tooltipText: null,
      hoveredCountries: [],
      hoverField: "NAME",
    };
  },
  computed: {
    colourScale: function(){
      var max_value = Math.max(...this.countryValues.values());
      // var min_value = Math.min(...this.countryValues.values(), 0);
      return d3.scaleSqrt().domain([0, max_value])
        .range(this.colourScaleColours);
    },
    selectedPaths: function(){
      return this.paths.filter((p) => this.selectedCountry.includes(p[0]["ISO_A2"]));
    },
    unSelectedPaths: function(){
      return this.paths.filter((p) => !this.selectedCountry.includes(p[0]["ISO_A2"]));
    }
  },
  methods: {
    countryColour: function(country){
      var value = this.countryValues.get(country);
      return this.colourScale(value);
    },
    countryStyle: function(country){
      var style = {
        fill: this.countryColour(country.ISO_A2),
        stroke: this.countryColour(country.ISO_A2),
        strokeOpacity: 1,
        opacity: 1,
        strokeWidth: 1,
        cursor: 'pointer',
      }
      if(this.hoveredCountries.includes(country[this.hoverField])){
        style.fill = '#D50032';
        style.stroke = '#D50032';
      }
      if(this.selectedCountry.includes(country["ISO_A2"])){
        style.stroke = '#D50032';
        style.strokeWidth = 3;
      }
      return style;
    },
    onHover: function(ev, country){
      if(this.countryValues.get(country.ISO_A2)){
        this.tooltipText = country[this.hoverField] + "\n" + this.countryValues.get(country.ISO_A2) + " members";
      } else {
        this.tooltipText = country[this.hoverField];
      }
      this.hoveredCountries = [country[this.hoverField]];
      this.mouseLocation = {
          x: ev.pageX,
          y: ev.pageY,
      };
    },
    leaveHover: function(){
      this.mouseLocation = null;
      this.hoveredCountries = [];
    },
    onResize: function () {
      const { width } = this.$refs.worldmap.parentElement.getBoundingClientRect();
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
    //     return this.selectedCountry["NAME"] == country["NAME"];
    //   } else {
    //     return this.selectedCountry[this.fieldToUse] == country[this.fieldToUse];
    //   }
    // },
    // countryIsHovered: function(country){
    //   if(!this.hoveredCountry){
    //     return false;
    //   } else if(this.zoomLevel > 0){
    //     return this.hoveredCountry["NAME"] == country["NAME"];
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
    WorldMapTooltip,
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