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
      </div>
      <div class="w-100 mv3">
        <div class="mb2 f4">
          <h3 class="ma0 pa0 f3">Sustainable Development Goals (<abbr title="Sustainable Development Goals">SDGs</abbr>)</h3>
          <p class="ma0 pa0 h2"><span class="" v-if="hoverSDG">{{ hoverSDG }}</span></p>
        </div>
        <div class="ma0 pa0 smol-css-grid sdg-grid">
          <label v-for="(sdg, index) in sdgSelectValues" :key="index" class="di" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null">
            <input v-if="sdgSelected(sdg.value) && filters.sdg.length > 0" @click.prevent="clearSDG" type="checkbox" :checked="sdgSelected(sdg.value)" class="sr-only" />
            <input v-else @click.prevent="setSDG(sdg.value)" type="checkbox" :checked="sdgSelected(sdg.value)" class="sr-only" />
            <span class="sr-only">{{ sdg.label }}</span>
            <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="o-100-hover grow" :class="{
              'o-100': sdgSelected(sdg.value),
              'o-30': !sdgSelected(sdg.value),
            }" />
          </label>
        </div>
      </div>
      <div class="mv3 w-100">
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
import filterStore from "../FilterStore.js";
import Multiselect from "@vueform/multiselect";
import MapContainer from "./MapContainer.vue";
import { readonly } from 'vue';

export default {
  name: "DataFilters",
  components: {
    Multiselect,
    MapContainer,
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
  },
  methods: {
    setCountry: function(value){
      filterStore.setCountry(value);
    },
    setSDG: function(value){
      filterStore.setSDG(value);
    },
    clearCountry: function(){
      filterStore.clearCountry();
    },
    clearSDG: function(){
      filterStore.clearSDG();
    },
    clearFilters: function(){
      filterStore.clearSDG();
      filterStore.clearCountry();
      filterStore.clearSearch();
    },
    setSearch: function(event){
      filterStore.setSearch(event.target.value);
    },
    sdgIcon: function(sdg){
      return require("../assets/images/sdgs/E-WEB-Goal-" + sdg + ".png");
    },
    sdgSelected: function(sdg){
      if(this.filters.sdg.length==0){
        return true;
      }
      return this.filters.sdg.includes(sdg);
    }
  }, 
  data() {
    return {
      filters: readonly(filterStore.state),
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