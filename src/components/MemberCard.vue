<template>
    <div class="fl bg-bond-grey br3 bb bw4 border-bond-dark-red">
      <header class="w-100 bg-bond-dark-red white ph2 pv3 br3 br--top">
        <h3 class="pa0 ma0 f4">{{ member.name }}</h3>
        <template v-if="(order < 4) && member.logoUrl">
          <img :src="member.logoUrl" class="br-100 fr org-logo border-bond-dark-red bw3 ba w3" />
        </template>
      </header>
      <div class="w-100 pa2">
        <p v-if="member.website" class="mh0 mv1 pa0">
          <a :href="cleanWebsite(member.website)">{{ displayWebsite(member.website) }}</a>
        </p>
        <p v-if="member.yearjoined" class="mh0 mv1 pa0">
          Bond Member since {{ member.yearjoined.slice(0, 4) }}
        </p>
        <div v-if="member.countries.length > 0" class="mh0 mv1 pa0">
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
        <div v-if="member.sdgs.length > 0" class="mh0 mv1 pa0">
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
    order: Number,
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
    cleanWebsite: function(url){
      if(url.startsWith("http") || url.startsWith("//")){
        return url;
      }
      return "//" + url;
    },
    displayWebsite: function(url){
      try {
        var displayUrl = new URL(this.cleanWebsite(url));
      } catch (error) {
        displayUrl = new URL("http://" + url);
      }
      return displayUrl.hostname.replace("www.", "");
    }
  }
}
</script>

<style scoped>
.org-logo {
    top: -50px;
    position: relative;
}
</style>