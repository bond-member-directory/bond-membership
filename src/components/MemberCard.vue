<template>
  <div
    class="fl bg-bond-grey bw4 border-bond-dark-red f4"
    :class="{ 'w-100': full }"
  >
    <header class="w-100 bg-bond-dark-red white ph3 pv3">
      <img
        v-if="order < 4 && member.logourl"
        :style="{
          backgroundColor: randomColour(),
        }"
        :src="member.logourl"
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
      <h3 class="pa0 ma0 f4">
        <a
          href="#"
          class="link white underline"
          @click.prevent="selectMember()"
          >{{ member.name }}</a
        >
      </h3>
    </header>
    <div class="w-100 pa3">
    <div class="w-100 w-50-ns fr" v-if="full && member.countries.length > 0" ref="worldmapcontainer">
      <world-map
        :countryValues="Object.fromEntries(member.countries.map((c) => [c, 1]))"
        :defaultClasses="['fill-bond-mid-grey', 'stroke-bond-mid-grey']"
        :selectedClasses="['fill-bond-dark-red', 'stroke-bond-mid-grey']"
      />
    </div>
    <div class="" :class="{ '': full }">
      <p v-if="member.website" class="mh0 mt1 mb3 pa0">
        <a
          :href="cleanWebsite(member.website)"
          class="b bond-red link underline bond-link"
          >{{ displayWebsite(member.website) }}</a
        >
      </p>
      <p v-if="member.activities && full" class="mh0 mt1 mb3 pa0 measure">
        {{member.activities}}
      </p>
      <p v-if="member.yearjoined && full" class="mh0 mv2 pa0">
        Bond Member since {{ member.yearjoined.slice(0, 4) }}
      </p>
      <div v-if="member.countries.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.countries.length < 4 || full">
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
          <ul
            class="list mh0 mb0 mt2 pa0"
            style="max-height: 7rem; overflow-y: auto"
          >
            <li v-for="country in member.countries" v-bind:key="country" class="mb2">
              <a
                href="#"
                class="b bond-red link underline bond-link"
                @click.prevent="selectCountry(country)"
                >{{ countries[country] }} ({{ country }})</a
              >
            </li>
          </ul>
        </details>
      </div>
      <div v-if="member.sdgs.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.sdgs.length < 4 || full">
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
  </div>
</template>

<script>
import filterStore from "../FilterStore.js";
import WorldMap from "./WorldMap.vue";

export default {
  name: "MemberCard",
  inject: ["countries", "sdgs"],
  props: {
    member: Object,
    order: Number,
    full: Boolean,
  },
  components: {
    WorldMap,
  },
  computed: {
    mapContainerHeight: function () {
      console.log(this.$refs);
      if (this.$refs.worldMapContainer) {
        return this.$refs.worldMapContainer.clientHeight;
      }
      return 400;
    },
    mapContainerWidth: function () {
      console.log(this.$refs);
      if (this.$refs.worldMapContainer) {
        return this.$refs.worldMapContainer.clientWidth;
      }
      return 400;
    },
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
    selectMember: function () {
      filterStore.setMemberSelected(this.member.id);
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
    randomColour: function () {
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
    },
  },
};
</script>

<style scoped>
.org-logo {
  top: -28px;
  position: relative;
  margin-bottom: -28px;
}
</style>