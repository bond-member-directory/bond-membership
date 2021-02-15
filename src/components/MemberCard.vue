<template>
    <div class="fl bg-bond-grey br2 mr3 mb3">
      <header class="w-100 bg-bond-dark-red white pa2 br2 br--top">
        {{ member.name }}
      </header>
      <div class="w-100 pa2">
        <div v-if="member.countries.length > 0">
          Works in
          <span v-if="member.countries.length < 4">
            <a href="#" @click.prevent="selectCountry(country)" v-for="country in member.countries" :key="country">{{ countries[country] }} ({{ country }})</a>
          </span>
          <span v-else>{{ member.countries.length }} countries</span>
          <!--<ul>
            <li v-for="country in member.countries" v-bind:key="country">
              <a href="#" @click.prevent="selectCountry(country)">{{ countries[country] }} ({{ country }})</a>
            </li>
          </ul>-->
        </div>
        <div v-if="member.sdgs.length > 0">
          Works on:
          <ul class="list ma0 pa0 flex flex-wrap">
            <li v-for="sdg in member.sdgs" v-bind:key="sdg" class="di w3 h3 fl mb1 mr1">
              <a href="#" @click.prevent="selectSDG(sdg)">
                <img :src="sdgIcon(sdg)" :title="sdgs[sdg]" />
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
</template>

<script>
import filterStore from "../FilterStore.js";

export default {
  name: 'MemberCard',
  inject: ['countries', 'sdgs'],
  props: {
    member: Object,
  },
  methods: {
    sdgIcon: function(sdg){
      return require("../assets/images/sdgs/E-WEB-Goal-" + sdg + ".png");
    },
    selectCountry: function(country){
      filterStore.setCountry(country);
    },
    selectSDG: function(sdg){
      filterStore.setSDG(sdg);
    },
  }
}
</script>