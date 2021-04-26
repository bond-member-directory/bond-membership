<template>
  <WorldMap
    :countryValues="countryValues"
    :colourScaleColours='colourScaleColours'
    :selectedCountry="filters.country"
    @select-country="selectCountry($event)"
    :alt="'Map showing where Bond Members work in the world'"
  />
  <p class="tr bond-dark-grey">Area of operation data from Charity Commission for England and Wales.</p>
</template>

<script>
const d3 = { ...require('d3'), ...require('d3-geo') };
const COLOUR_SCALE = [
  "white",
  // "#D50032",
  // "#B6002D",
  "#A20026",
  "#8A0026",
  // "#560014",
];

import { getFiltersFromUrl, memberIsSelected } from '../FilterStore.js';
import WorldMap from './WorldMap.vue';

export default {
  name: 'MapContainer',
  inject: ['world', 'members'],
  props: {
    center: {
      type: Array,
      default: () => [33.561041, -7.584838],
    },
    scale: {
      type: [Number, String],
      default: 1 << 20,
    },
  },
  data () {
    return {
      width: 600,
      height: 400,
      projection: null,
      geoGenerator: null,
      paths: [],
      selectedCountry: null,
      hoveredCountry: null,
      fieldToUse: 'REGION_WB',
      zoomLevel: 0,
      filters: getFiltersFromUrl(this.$route),
      colourScaleColours: COLOUR_SCALE,
    };
  },
  watch: {
    $route: function(to){
      this.filters = getFiltersFromUrl(to);
    }
  },
  computed: {
    selectedCountryName: function(){
      if(!this.selectedCountry){
        return null;
      } else if(this.zoomLevel > 1){
        return this.selectedCountry["NAME"];
      } else {
        return this.selectedCountry[this.fieldToUse];
      }
    },
    countryValues: function(){
      var members = this.members.filter((member) => memberIsSelected(member, this.$route));
      var memberCount = [].concat.apply(
        [],
        members.map((member) => member["countries"])
      ).reduce(
        (acc, e) => acc.set(e, (acc.get(e) || 0) + 1),
        new Map()
      );
      memberCount.delete("GB");
      return memberCount;
    }
  },
  methods: {
    selectCountry: function(country){
      if(this.filters.country.includes(country.ISO_A2)){
        var new_countries = this.filters.country.filter((value) => value != country.ISO_A2);
        this.$router.push({path: this.$route.path, query: {...this.$route.query, country: new_countries}});
      } else {
        this.$router.push({path: this.$route.path, query: {...this.$route.query, country: country.ISO_A2}});
      }
    },
    countryIsSelected: function(country){
      if(!this.selectedCountry){
        return false;
      } else if(this.zoomLevel > 1){
        return this.selectedCountry["NAME"] == country["NAME"];
      } else {
        return this.selectedCountry[this.fieldToUse] == country[this.fieldToUse];
      }
    },
    countryIsHovered: function(country){
      if(!this.hoveredCountry){
        return false;
      } else if(this.zoomLevel > 0){
        return this.hoveredCountry["NAME"] == country["NAME"];
      } else {
        return this.hoveredCountry[this.fieldToUse] == country[this.fieldToUse];
      }
    },
    zoomMap: function(country){
      this.selectedCountry = country;
      var countries = this.world.features;
      if(country != null){
        if(this.zoomLevel>=1){
          countries = this.world.features.filter(
            (c) => c.properties['ISO_A2'] == country['ISO_A2']
          );
          this.zoomLevel = 2;
          this.selectCountry(country)
        } else {
          countries = this.world.features.filter(
            (c) => (
              c.properties[this.fieldToUse] == country[this.fieldToUse] &&
              c.properties['POP_EST'] >= 1000000 &&
              !["GL", "RU"].includes(c.properties['ISO_A2'])
            )
          );
          this.zoomLevel = 1;
        }
      } else {
        this.zoomLevel = 0;
      }
      this.projection.fitSize([this.width, this.height], {
        type: "FeatureCollection",
        features: countries,
      });
      this.paths = this.world.features.map((b) => [b.properties, this.geoGenerator(b)]);
    },
  },
  mounted() {
    this.projection = d3.geoNaturalEarth1()
      .fitSize([this.width, this.height], this.world);
    this.geoGenerator = d3.geoPath()
      .projection(this.projection);
    this.paths = this.world.features.map((b) => [b.properties, this.geoGenerator(b)]);
  },
  components: {
    WorldMap,
  },
};
</script>

<style scoped>
.map {
  width: 100%;
  height: 100%;
}
.light-shadow{
  filter: drop-shadow(0px 3px 3px rgba(0, 0, 0, 0.4));
}
.dark-shadow{
  filter: drop-shadow(0px 3px 3px rgba(0, 0, 0, 1));
}
</style>