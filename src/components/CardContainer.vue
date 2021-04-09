<template>
  <div class="w-100 bg-bond-gray f4" style="grid-area: cardheader">
    <template v-if="filteredMembers.length != members.length">
      Found {{ filteredMembers.length }} of {{ members.length }} members.
      Page {{ page + 1 }} of {{ last_page }}.
    </template>
    <template v-else>
      Found {{ members.length }} members.
      Page {{ page + 1 }} of {{ last_page }}.
    </template>
    <p v-if="filters.country.length > 0 && filters.sdg.length > 0">
      Showing members working on SDG
      <separated-list :items="sdgNames" separator=" or " /> and working in
      <separated-list :items="countryNames" separator="or" />
    </p>
    <p v-else-if="filters.country.length > 0">
      Showing members working in
      <separated-list :items="countryNames" separator="or" />
    </p>
    <p v-else-if="filters.sdg.length > 0">
      Showing members working on SDG
      <separated-list :items="sdgNames" separator=" or " />
    </p>
  </div>
  <div
    class="w-100 bg-bond-gray pv4 smol-flexbox-grid card-grid"
    style="grid-area: cards"
  >
    <MemberCard
      v-for="(member, index) in paginatedMembers"
      v-bind:key="member.id"
      :order="index"
      :member="member"
    />
  </div>
  <div class="w-100">
    <div class="fl">
      <a v-if="page > 0" v-on:click.prevent="page = 0" href="#" class="bond-red link underline bond-link b f4 mr3">First page</a>
      <a v-if="page > 0" v-on:click.prevent="page = page - 1" href="#" class="bond-red link underline bond-link b f4 mr3">Previous page</a>
    </div>
    <div class="fr">
      <a v-if="page < last_page" v-on:click.prevent="page = page + 1" href="#" class="bond-red link underline bond-link b f4 mr3">Next page</a>
      <a v-if="page < last_page" v-on:click.prevent="page = last_page - 1" href="#" class="bond-red link underline bond-link b f4 mr3">Last page</a>
    </div>
  </div>
</template>

<script>
import { memberIsSelected, getFiltersFromUrl } from "../FilterStore.js";
import MemberCard from "./MemberCard.vue";
import SeparatedList from "./SeparatedList.vue";

const PAGE_SIZE = 12;

export default {
  name: "CardContainer",
  inject: ["members", "countries", "sdgs"],
  components: {
    MemberCard,
    SeparatedList,
  },
  data: function () {
    return {
      filters: getFiltersFromUrl(this.$route),
      page: 0,
      size: PAGE_SIZE,
    };
  },
  watch: {
    $route: function(to){
      this.filters = getFiltersFromUrl(to);
    },
  },
  computed: {
    filteredMembers: function () {
      return this.members.filter((member) =>
        memberIsSelected(member, this.$route)
      );
    },
    paginatedMembers: function(){
      var members = this.filteredMembers;
      return members.slice(this.page_start, this.page_end);
    },
    page_start: function(){
      return this.page * this.size;
    },
    page_end: function(){
      return Math.min(
        this.page_start + this.size,
        this.filteredMembers.length
      );
    },
    last_page: function(){
      return Math.ceil(
        this.filteredMembers.length / this.size
      )
    },
    countryNames: function () {
      return this.filters.country.map((c) => this.countries[c]);
    },
    sdgNames: function () {
      return this.filters.sdg.map((c) => this.sdgs[c]);
    },
  },
};
</script>

<style scoped>
.card-grid {
  --min: 30ch;
  --max: 25%;
  --gap: 1.5rem;
}
</style>