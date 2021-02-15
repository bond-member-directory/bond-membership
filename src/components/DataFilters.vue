<template>
  <div class="w-100 bg-light-gray pv3 ph4 smol-flexbox-grid">
    <div class="">
      <Multiselect
        v-model="filters.country"
        :options="countrySelectValues"
        :searchable="true"
        mode="tags"
        @change="setCountry"
        placeholder="Filter by country"
        class="w-100 bg-bond-grey"
      />
      <a href="#" class="fr blue link underline f6 mt2" @click.prevent="clearCountry">Clear</a>
    </div>
    <div class="">
      <Multiselect
        v-model="filters.sdg"
        :options="sdgSelectValues"
        :searchable="true"
        mode="single"
        @change="setSDG"
        placeholder="Filter by Sustainable Development Goal"
        class="w-100 bg-bond-grey"
      />
      <a href="#" class="fr blue link underline f6 mt2" @click.prevent="clearSDG">Clear</a>
    </div>
    <div class="">
      <input :value="filters.search"
        type="search"
        @keyup.prevent="setSearch"
        placeholder="Search organisations"
        class="w-100 bg-bond-grey pa2 bw0"
      />
    </div>
  </div>
  <div class="w-100 bg-light-gray pt3 ph4">
    <template v-for="(sdg, index) in sdgSelectValues" :key="index">
      <a href="#" @click.prevent="clearSDG" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null" v-if="sdgSelected(sdg.value) && filters.sdg.length > 0">
        <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="w3 o-100 o-100-hover grow" />
      </a>
      <a href="#" @click.prevent="setSDG(sdg.value)" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null" v-else-if="sdgSelected(sdg.value)">
        <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="w3 o-100 o-100-hover grow" />
      </a>
      <a href="#" @click.prevent="setSDG(sdg.value)" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null" v-else>
        <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="w3 o-30 o-100-hover grow" />
      </a>
    </template>
  </div>
  <div class="w-100 bg-light-gray pb3 ph4 cf"><p class="h2">{{ hoverSDG }}</p></div>
</template>

<script>
import filterStore from "../FilterStore.js";
import Multiselect from "@vueform/multiselect";
import { readonly } from 'vue';

export default {
  name: "DataFilters",
  components: {
    Multiselect,
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
    };
  },
};
</script>

<style src="@vueform/multiselect/themes/default.css"></style>
<style scoped>
.smol-flexbox-grid {
  --min: 40ch;
  --gap: 1rem;

  display: flex;
  flex-wrap: wrap;
  gap: var(--gap);
}

.smol-flexbox-grid > * {
  flex: 1 1 var(--min);
}

.o-100-hover:hover {
  opacity: 1;
}
</style>