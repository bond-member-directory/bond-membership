<template>
  <div v-if="full" class="fl bw4 border-bond-dark-red f4 w-100 lh-copy">
    <header class="cf">
      <h3 class="pa0 ma0 f2 b">{{ member.name }}</h3>
      <img
        v-if="member.logourl"
        :style="{
          backgroundColor: randomColour(),
        }"
        :src="member.logourl"
        class="br-100 fr org-logo border-bond-dark-red bw0 ba w4"
      />
    </header>
    <div class="w-100 cf">
      <div class="w-100 w-50-ns fr" v-if="member.countries.length > 0" ref="worldmapcontainer">
        <world-map
          :countryValues="new Map(member.countries.map((c) => [c, 1]))"
          :colourScaleColours='["white", "#560014"]'
          :defaultClasses="['fill-bond-mid-grey', 'stroke-bond-mid-grey']"
          :selectedClasses="['fill-bond-dark-red', 'stroke-bond-mid-grey']"
        />
      </div>
      <p v-if="member.website" class="mh0 mt1 mb3 pa0">
        <a
          :href="cleanWebsite(member.website)"
          class="b bond-red link underline bond-link"
          >{{ displayWebsite(member.website) }}</a
        >
      </p>
      <p v-if="member.activities" class="mh0 mt1 mb4 pa0 measure">
        {{member.activities}}
      </p>
      <p v-if="member.yearjoined" class="mh0 mv4 pa0">
        Bond Member since {{ member.yearjoined.slice(0, 4) }}
      </p>
      <div v-if="member.countries.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.countries.length < 5">
          Works in
          <separated-list :items="member.countries.map((c) => countries[c]).sort()" />
        </template>
        <template v-else>
          <p>Works in {{ member.countries.length }} countries</p>
          <ul
            class="list mh0 mb0 mt2 pa0"
          >
            <li v-for="country in member.countries.map((c) => countries[c]).sort()" v-bind:key="country" class="mb2">
              {{ countries[country] }}
            </li>
          </ul>
        </template>
      </div>
      <div v-if="member.sdgs.length > 0" class="mh0 mv3 pa0">
        Sustainable Development Goals
        <ul class="list mh0 mb0 mt2 pa0 flex flex-wrap">
          <li
            v-for="sdg in member.sdgs"
            v-bind:key="sdg"
            class="di fl mb1 mr1 w4 h4"
          >
            <img :src="sdgIcon(sdg)" :alt="sdgs[sdg]" :title="sdgs[sdg]" />
          </li>
        </ul>
      </div>
      <div class="tr w-100">
        <a v-if="member.sdgs.length > 0 || member.countries.length > 0" href="#" @click.prevent="selectSDGCountry(member.sdgs, member.countries)" class="db f6 bond-red bond-underline mt2" title="Select members that work on one of the same SDGs or in one of the the same countries.">
          Find similar members
        </a>
      </div>
    </div>
  </div>

  <div v-else class="fl bw4 border-bond-dark-red f4 bg-bond-grey">
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
      <p v-if="member.website" class="mh0 mt1 mb3 pa0">
        <a
          :href="cleanWebsite(member.website)"
          class="b bond-red link underline bond-link"
          >{{ displayWebsite(member.website) }}</a
        >
      </p>
      <div v-if="member.countries.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.countries.length < 5">
          Works in
          <separated-list :items="member.countries.map((c) => countries[c]).sort()" />
        </template>
        <details v-else>
          <summary class="pointer">Works in {{ member.countries.length }} countries</summary>
          <ul
            class="list mh0 mb0 mt2 pa0"
            style="max-height: 7rem; overflow-y: auto"
          >
            <li v-for="country in member.countries.map((c) => countries[c]).sort()" v-bind:key="country" class="mb2">
              {{ countries[country] }}
            </li>
          </ul>
        </details>
      </div>
      <div v-if="member.sdgs.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.sdgs.length <= 5">
          Sustainable Development Goals
          <ul class="list mh0 mb0 mt2 pa0 flex flex-wrap">
            <li
              v-for="sdg in member.sdgs"
              v-bind:key="sdg"
              class="di fl mb1 mr1 w3 h3"
            >
              <img :src="sdgIcon(sdg)" :alt="sdgs[sdg]" :title="sdgs[sdg]" />
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
              <img :src="sdgIcon(sdg)" :alt="sdgs[sdg]" :title="sdgs[sdg]" />
            </li>
          </ul>
        </details>
      </div>
      <div class="tr w-100">
        <a href="#" @click.prevent="selectMember()" class="db f5 bond-red bond-underline">
          More about this member &gt;
        </a> 
        <a v-if="member.sdgs.length > 0 || member.countries.length > 0" href="#" @click.prevent="selectSDGCountry(member.sdgs, member.countries)" class="db f6 bond-red bond-underline mt2" title="Select members that work on one of the same SDGs or in one of the the same countries.">
          Find similar members
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import filterStore from "../FilterStore.js";
import WorldMap from "./WorldMap.vue";
import SeparatedList from "./SeparatedList.vue";

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
    SeparatedList,
  },
  computed: {
    mapContainerHeight: function () {
      if (this.$refs.worldMapContainer) {
        return this.$refs.worldMapContainer.clientHeight;
      }
      return 400;
    },
    mapContainerWidth: function () {
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
    selectSDGCountry: function (sdg, country) {
      filterStore.setSDG(sdg);
      filterStore.setCountry(country);
      filterStore.clearMemberSelected();
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