<template>
  <div class="fl bg-bond-grey bw4 border-bond-dark-red f4">
    <header class="w-100 bg-bond-dark-red white ph3 pv3">
      <img
        v-if="order < 4 && member.logoUrl"
        :src="member.logoUrl"
        class="br-100 fr org-logo border-bond-dark-red bw3 ba w3"
      />
      <div
        v-else
        :style="{
          backgroundColor: randomColour(),
          width: '80px',
          height: '80px',
        }"
        class="br-100 fr org-logo border-bond-dark-red bw3 ba w3"
      ></div>
      <h3 class="pa0 ma0 f4">{{ member.name }}</h3>
    </header>
    <div class="w-100 pa3">
      <p v-if="member.website" class="mh0 mt1 mb3 pa0">
        <a
          :href="cleanWebsite(member.website)"
          class="b bond-red link underline bond-link"
          >{{ displayWebsite(member.website) }}</a
        >
      </p>
      <p v-if="member.yearjoined" class="mh0 mv2 pa0">
        Bond Member since {{ member.yearjoined.slice(0, 4) }}
      </p>
      <div v-if="member.countries.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.countries.length < 4">
          Works in 
          <template class="" v-for="country in member.countries" :key="country">
            <a
              href="#"
              class="b bond-red link underline bond-link mr1"
              @click.prevent="selectCountry(country)"
              >{{ countries[country] }}</a
            >
          </template>
        </template>
        <details v-else>
          <summary class="pointer">Works in {{ member.countries.length }} countries</summary>
          <ul class="list mh0 mb0 mt2 pa0" style="max-height: 7rem; overflow-y: auto;">
            <li v-for="country in member.countries" v-bind:key="country">
              <a href="#" @click.prevent="selectCountry(country)"
                >{{ countries[country] }} ({{ country }})</a
              >
            </li>
          </ul>
        </details>
      </div>
      <div v-if="member.sdgs.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.sdgs.length < 4">
          Sustainable Development Goals
          <ul class="list mh0 mb0 mt2 pa0 flex flex-wrap">
            <li
              v-for="sdg in member.sdgs"
              v-bind:key="sdg"
              class="di w3 h3 fl mb1 mr1"
            >
              <a href="#" @click.prevent="selectSDG(sdg)">
                <img :src="sdgIcon(sdg)" :title="sdgs[sdg]" />
              </a>
            </li>
          </ul>
        </template>
        <details v-else>
          <summary class="pointer">
            {{ member.sdgs.length }} Sustainable Development Goals
          </summary>
          <ul class="list mh0 mb0 mt2 pa0 flex flex-wrap">
            <li
              v-for="sdg in member.sdgs"
              v-bind:key="sdg"
              class="di w3 h3 fl mb1 mr1"
            >
              <a href="#" @click.prevent="selectSDG(sdg)">
                <img :src="sdgIcon(sdg)" :title="sdgs[sdg]" />
              </a>
            </li>
          </ul>
        </details>
      </div>
    </div>
  </div>
</template>

<script>
import filterStore from "../FilterStore.js";

export default {
  name: "MemberCard",
  inject: ["countries", "sdgs"],
  props: {
    member: Object,
    order: Number,
  },
  methods: {
    sdgIcon: function (sdg) {
      return require("../assets/images/sdgs/E-WEB-Goal-" + sdg + ".png");
    },
    selectCountry: function (country) {
      filterStore.setCountry(country);
    },
    selectSDG: function (sdg) {
      filterStore.setSDG(sdg);
    },
    cleanWebsite: function (url) {
      if (url.startsWith("http") || url.startsWith("//")) {
        return url;
      }
      return "//" + url;
    },
    displayWebsite: function (url) {
      try {
        var displayUrl = new URL(this.cleanWebsite(url));
      } catch (error) {
        displayUrl = new URL("http://" + url);
      }
      return displayUrl.hostname.replace("www.", "");
    },
    randomColour: function(){
      var colours = [
        "#FFEE5F",
        "#00C8D2",
        "#8EE1AA",
        "#D78AAF",
        "#FFB400",
        "#00648C",
        "#326466",
        "#7D004B",
      ];
      return colours[Math.floor(Math.random() * colours.length)];
    }
  },
};
</script>

<style scoped>
.org-logo {
  top: -28px;
  position: relative;
}
</style>