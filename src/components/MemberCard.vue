<template>
  <div class="fl bw4 border-bond-dark-red f4 bg-bond-white member-card">
    <header class="w-100 bg-bond-red white ph3 pv3">
      <img
        v-if="member.logourl"
        :style="{
          backgroundColor: randomColour(),
        }"
        :src="member.logourl"
        :alt="'Logo of ' + member.name"
        class="br-100 fr org-logo border-bond-red bw3 ba w3 h3"
      />
      <div
        v-else
        :style="{
          backgroundColor: randomColour(),
          width: '80px',
          height: '80px',
        }"
        class="br-100 fr org-logo border-bond-red bw0 ba w3"
      ></div>
      <h3 class="pa0 ma0 f4">
        <router-link
          :to="{ name: 'Member', params: { id: slugify(member.name) } }"
          class="link white underline-hover bond-link"
          >{{ member.name }}</router-link
        >
      </h3>
    </header>
    <div class="w-100 ma3 member-card-contents">
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
          <separated-list
            :items="member.countries.map((c) => countries[c]).sort()"
          />
        </template>
        <details v-else>
          <summary class="pointer">Works in {{ member.countries.length }} countries</summary>
          <ul
            class="list mh0 mb0 mt2 pa0"
            style="max-height: 7rem; overflow-y: auto"
          >
            <li
              v-for="country in member.countries
                .map((c) => countries[c])
                .sort()"
              v-bind:key="country"
              class="mb2"
            >
              {{ country }}
            </li>
          </ul>
        </details>
      </div>
      <div v-if="member.sdgs && member.sdgs.length > 0" class="mh0 mv3 pa0">
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
    </div>
    <footer class="tr w-100 ph3 mb3">
      <a
        v-if="(member.sdgs && member.sdgs.length > 0) || member.countries.length > 0"
        href="#"
        @click.prevent="selectSDGCountry(member.sdgs, member.countries)"
        class="db f6 bond-red bond-link underline mb3"
        title="Select members that work on one of the same SDGs or in one of the the same countries."
      >
        Find similar members
      </a>
      <router-link
        :to="{ name: 'Member', params: { id: slugify(member.name) } }"
        class="db f6 bond-red bond-link underline"
        >More about this member &gt;</router-link
      >
    </footer>
  </div>
</template>

<script>
import SeparatedList from "./SeparatedList.vue";
import { slugify } from "../FilterStore.js";

export default {
  name: "MemberCard",
  inject: ["countries", "sdgs"],
  props: {
    member: Object,
    order: Number,
  },
  components: {
    SeparatedList,
  },
  computed: {
  },
  methods: {
    sdgIcon: function (sdg) {
      return require("../assets/images/sdgs/E-WEB-Goal-" + sdg + ".png");
    },
    selectSDGCountry: function (sdg, country) {
      if(!sdg){sdg = [];}
      if(!country){country = [];}
      this.$router.push({
        name: "Home",
        query: {
          ...this.$route.query,
          country: country.join(","),
          sdg: sdg.join(","),
        },
      });
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
    slugify: slugify,
  },
};
</script>

<style scoped>
.org-logo {
  top: -28px;
  position: relative;
  margin-bottom: -56px;
  object-fit: contain;
}
.member-card {
  display: flex;
  flex-direction: column;
}
.member-card > .member-card-contents { 
  flex-grow: 1;
}
</style>