<template>
  <div class="fl bw4 border-bond-dark-red f4 w-100 lh-copy">
    <header class="cf">
      <h3 class="pa0 ma0 f2 b">{{ member.name }}</h3>
      <img
        v-if="member.logourl"
        :src="member.logourl"
        class="fr org-logo border-bond-dark-red bw0 ba w4 bg-bond-dark-red pa2"
      />
    </header>
    <div class="w-100 cf">
      <div
        class="w-100 w-50-ns fr"
        v-if="member.countries.length > 0"
        ref="worldmapcontainer"
      >
        <world-map
          :countryValues="new Map(member.countries.map((c) => [c, 1]))"
          :colourScaleColours="['white', '#560014']"
          :defaultClasses="['fill-bond-mid-grey', 'stroke-bond-mid-grey']"
          :selectedClasses="['fill-bond-dark-red', 'stroke-bond-mid-grey']"
        />
      </div>
      <p v-if="member.website || ccewUrl || member.primarycontactemail" class="mh0 mt1 mb3 pa0">
        <a
          v-if="member.website"
          :href="cleanWebsite(member.website)"
          class="b bond-red link underline bond-link"
          target="_blank"
          >{{ displayWebsite(member.website) }}</a
        >
        <template v-if="member.website && ccewUrl"> | </template>
        <a
          v-if="ccewUrl"
          :href="ccewUrl"
          class="b bond-red link underline bond-link"
          target="_blank"
          >Charity Commission record</a
        >
        <template v-if="(member.website || ccewUrl) && member.primarycontactemail"> | </template>
        <a
          v-if="member.primarycontactemail && !showEmail"
          href="#"
          @click.prevent="showEmail = !showEmail"
          class="b bond-red link underline bond-link"
          >Get in touch</a
        >
        <a
          v-if="member.primarycontactemail && showEmail"
          :href="`mailto:${email}`"
          class="b bond-red link underline bond-link"
          target="_blank"
          >{{email}}</a
        >
        <a
          v-if="member.primarycontactemail && showEmail"
          href="#"
          @click.prevent="showEmail = !showEmail"
          class="b bond-red link underline bond-link f6 ml2"
          >(hide)</a
        >
      </p>
      <blockquote v-if="member.activities" class="mh0 mt4 mb4 pa0 measure">
        {{ member.activities }}
      </blockquote>
      <p v-if="sizeBand" class="mh0 mv4 pa0">
        Annual income {{ sizeBand }}<template v-if="member.latest_fye"> (<time :datetime="member.latest_fye">{{ member.latest_fye.slice(0,4)}}</time>)</template>.
      </p>
      <div v-if="member.sdgs && member.sdgs.length > 0" class="mh0 mv3 pa0">
        <h3>Sustainable Development Goals</h3>
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
      <div v-if="member.countries.length > 0" class="mh0 mv3 pa0">
        <template v-if="member.countries.length < 5">
          Works in
          <separated-list
            :items="member.countries.map((c) => countries[c]).sort()"
          />
        </template>
        <template v-else>
          <p>Works in {{ member.countries.length }} countries</p>
          <ul class="list mh0 mb0 mt2 pa0">
            <li
              v-for="country in member.countries
                .map((c) => countries[c])
                .sort()"
              v-bind:key="country"
              class="mb2"
            >
              {{ countries[country] }}
            </li>
          </ul>
        </template>
      </div>
    </div>
    <footer class="tr w-100">
      <a
        v-if="(member.sdgs && member.sdgs.length > 0) || member.countries.length > 0"
        href="#"
        @click.prevent="selectSDGCountry(member.sdgs, member.countries)"
        class="db f5 bond-red bond-link underline mt2"
        title="Select members that work on one of the same SDGs or in one of the the same countries."
      >
        Find similar members
      </a>
    </footer>
  </div>
</template>

<script>
import WorldMap from "./WorldMap.vue";
import SeparatedList from "./SeparatedList.vue";

export default {
  name: "MemberPage",
  inject: ["countries", "sdgs"],
  props: {
    member: Object,
    order: Number,
  },
  data() {
    return {
      showEmail: false,
    };
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
    sizeBand: function(){
      if(this.member.latest_income > 100000000){
        return "over £100m";
      }
      if(this.member.latest_income > 10000000){
        return "£10m - £100m";
      }
      if(this.member.latest_income > 1000000){
        return "£1m - £10m";
      }
      if(this.member.latest_income > 100000){
        return "£100k - £1m";
      }
      if(this.member.latest_income > 10000){
        return "£10k - £100k";
      }
      if(this.member.latest_income > 0){
        return "under £10k";
      }
      return null;
    },
    ccewUrl: function(){
      if(this.member.charityCommissionnumber){
        return `https://register-of-charities.charitycommission.gov.uk/charity-details/?regId=${this.member.charityCommissionnumber}&subId=0`;
      }
      return null;
    },
    email: function(){
      if(this.member.primarycontactemail){
        return atob(this.member.primarycontactemail);
      }
      return null;
    },
  },
  methods: {
    sdgIcon: function (sdg) {
      return require("../assets/images/sdgs/E-WEB-Goal-" + sdg + ".png");
    },
    selectSDGCountry: function (sdg, country) {
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