<template>
  <div class="w-100 cf">
    <div class="w-100 fl cf" v-bind:class="{ 'w-40-l': showMap }">
      <div class="w-100 mv3 smol-flexbox-grid">
        <div class="dn">
          <Multiselect
            v-model="filters.sdg"
            :options="sdgSelectValues"
            :searchable="true"
            mode="single"
            @change="setSDG"
            placeholder="Filter by Sustainable Development Goal"
            class="w-100 bg-bond-grey"
          />
          <!-- <a href="#" class="fr bond-red link underline bond-link b f5 mt2" @click.prevent="clearSDG">Clear</a> -->
        </div>
        <div class="">
          <input :value="filters.search"
            type="search"
            @keyup.prevent="setSearch"
            placeholder="Search organisations"
            class="w-100 bg-bond-grey pa2 bw0 filter"
          />
        </div>
        <div class="">
          <Multiselect
            v-model="filters.country"
            :options="countrySelectValues"
            :searchable="true"
            mode="tags"
            :maxHeight="240"
            @change="setCountry"
            placeholder="Filter by country"
            class="w-100 bg-bond-grey"
          />
        </div>
      </div>
      <div class="w-100 mv3">
        <div class="mb2">
          <h3 class="ma0 pa0 f5 normal">Filter by Sustainable Development Goals (<abbr title="Sustainable Development Goals">SDGs</abbr>)</h3>
        </div>
        <div class="ma0 pa0 smol-css-grid sdg-grid" role="radiogroup">
          <label v-for="(sdg, index) in sdgSelectValues" :key="index" class="di o-100-hover grow pointer" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null">
            <input v-if="filters.sdg && sdgSelected(sdg.value) && filters.sdg.length > 0" @click.prevent="clearSDG" type="checkbox" :checked="sdgSelected(sdg.value)" class="sr-only" />
            <input v-else @click.prevent="setSDG(sdg.value)" type="checkbox" :checked="sdgSelected(sdg.value)" class="sr-only" />
            <span class="sr-only">{{ sdg.label }}</span>
            <img :src="sdgIcon(sdg.value)" :title="sdg.label" tabindex="0" class=""
              role="radio"
              :aria-checked="sdgSelected(sdg.value)"
              :class="{
              'o-100': sdgSelected(sdg.value),
              'o-30': !sdgSelected(sdg.value),
            }" />
          </label>
        </div>
        <p class="ma0 pa0" style="min-height: 2rem;">
          <span class="" v-if="hoverSDG">{{ hoverSDG }}</span>
          <span v-else><separated-list :items="selectedSDGs" /></span>
        </p>
      </div>
      <div class="mv3 w-100 tr">
        <a href="#" class="bond-red link underline bond-link b f5 ml3" @click.prevent="clearFilters">Clear filters</a>
        <a href="#" class="bond-red link underline bond-link b f5 ml3" @click.prevent="showMap = !showMap">
          <template v-if="showMap">Hide map</template>
          <template v-else>Show map</template>
        </a>
        <!-- <a href="#" class="fr bond-red link underline bond-link b f5 mt2" @click.prevent="clearCountry">Clear</a> -->
      </div>
    </div>
    <div class="w-100 w-60-l fl cf pl0 pl3-l" v-if="showMap">
      <MapContainer />
    </div>
  </div>
</template>

<script>
import Multiselect from "@vueform/multiselect";
import MapContainer from "./MapContainer.vue";
import SeparatedList from "./SeparatedList.vue";
import { getFiltersFromUrl } from "../FilterStore.js";

export default {
  name: "DataFilters",
  components: {
    Multiselect,
    MapContainer,
    SeparatedList,
  },
  inject: ["countries", "sdgs"],
  computed: {
    countrySelectValues: function () {
      var countries = Object.entries(this.countries).map(([v, k]) => ({
        value: v,
        label: k,
      }));
      countries.sort((a, b) => a.label.localeCompare(b.label));
      return countries;
    },
    sdgSelectValues: function () {
      var sdgs = Object.entries(this.sdgs).map(([v, k]) => ({
        value: v,
        label: k,
      }));
      sdgs.sort((a, b) => a.value.localeCompare(b.value));
      return sdgs;
    },
    selectedSDGs: function(){
      var component = this;
      var selected = this.sdgSelectValues.filter(function(sdg) {
        return component.sdgSelected(sdg.value);
      }).map((sdg) => sdg.label);
      if(selected.length == this.sdgSelectValues.length){
        return [];
      }
      return selected;
    },
  },
  watch: {
    $route: function(to){
      this.filters = getFiltersFromUrl(to);
    },
  },
  methods: {
    setCountry: function(value){
      if(Array.isArray(value)){
        value = value.join(",");
      }
      this.$router.push({path: this.$route.path, query: {...this.$route.query, country: value}});
    },
    setSDG: function(value){
      if(Array.isArray(value)){
        value = value.join(",");
      }
      this.$router.push({path: this.$route.path, query: {...this.$route.query, sdg: value}});
    },
    clearCountry: function(){
      this.$router.push({path: this.$route.path, query: {...this.$route.query, country: ""}});
    },
    clearSDG: function(){
      this.$router.push({path: this.$route.path, query: {...this.$route.query, sdg: ""}});
    },
    clearFilters: function(){
      this.$router.push({path: this.$route.path, query: {}});
    },
    setSearch: function(event){
      this.$router.push({path: this.$route.path, query: {...this.$route.query, search: event.target.value}});
    },
    sdgIcon: function(sdg){
      return require("../assets/images/sdgs/E-WEB-Goal-" + sdg + ".png");
    },
    sdgSelected: function(sdg){
      if(!this.$route.query.sdg || this.$route.query.sdg.length==0){
        return true;
      }
      return this.$route.query.sdg.includes(sdg);
    }
  }, 
  data() {
    return {
      filters: getFiltersFromUrl(this.$route),
      hoverSDG: null,
      showMap: true,
    };
  },
};
</script>

<style src="@vueform/multiselect/themes/default.css"></style>
<style scoped>
.multiselect-tag {
    font-size: 2em;
}

.sdg-grid {
  --min: 9ch;
  --gap: 0.25rem;
}

.o-100-hover:hover {
  opacity: 1;
}

.filter {
  padding: 0.69rem;
}
</style>