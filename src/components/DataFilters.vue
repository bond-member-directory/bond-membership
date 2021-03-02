<template>
  <div class="w-100 mv3 smol-flexbox-grid">
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
      <!-- <a href="#" class="fr bond-red link underline bond-link b f5 mt2" @click.prevent="clearCountry">Clear</a> -->
    </div>
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
      <a href="#" class="fr bond-red link underline bond-link b f5" @click.prevent="clearSDG">Clear filters</a>
      <label for="filterSDG" class="b">Sustainable Development Goals</label><span class="" v-if="hoverSDG">: {{ hoverSDG }}</span>
    </div>
    <ul class="ma0 pa0 list smol-css-grid sdg-grid" id="filterSDG">
      <li v-for="(sdg, index) in sdgSelectValues" :key="index" class="di">
        <a href="#" @click.prevent="clearSDG" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null" v-if="sdgSelected(sdg.value) && filters.sdg.length > 0">
          <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="o-100 o-100-hover grow" />
        </a>
        <a href="#" @click.prevent="setSDG(sdg.value)" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null" v-else-if="sdgSelected(sdg.value)">
          <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="o-100 o-100-hover grow" />
        </a>
        <a href="#" @click.prevent="setSDG(sdg.value)" @mouseover="hoverSDG = sdg.label" @mouseleave="hoverSDG = null" v-else>
          <img :src="sdgIcon(sdg.value)" :title="sdg.label" class="o-30 o-100-hover grow" />
        </a>
      </li>
    </ul>
  </div>
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