<template>
  <div class="w-100 bg-bond-gray f4 cf" style="grid-area: cardheader">
    <p>
      <template v-if="filteredMembers.length != members.length">
        <template v-if="filters.country.length > 0 && filters.sdg.length > 0">
          {{ filteredMembersCount }} of our {{ members.length }} members
          {{ isOrAre }} working on SDG
          <separated-list :items="sdgNames" separator=" or " /> and working in
          <separated-list :items="countryNames" separator="or" />
        </template>
        <template v-else-if="filters.country.length > 0">
          {{ filteredMembersCount }} of our {{ members.length }} members
          {{ isOrAre }} working in
          <separated-list :items="countryNames" separator="or" />
        </template>
        <template v-else-if="filters.sdg.length > 0">
          {{ filteredMembersCount }} of our {{ members.length }} members
          {{ isOrAre }} working on SDG
          <separated-list :items="sdgNames" separator=" or " />
        </template>
        <template v-else>
          {{ filteredMembersCount }} of our {{ members.length }} members
        </template>
      </template>
      <template v-else> Found {{ members.length }} members. </template>
    </p>
  </div>
  <div class="w-100 bg-bond-gray pv4 card-grid" style="grid-area: cards">
    <MemberCard
      v-for="(member, index) in paginatedMembers"
      v-bind:key="member.id"
      :order="index"
      :member="member"
    />
  </div>
  <div class="w-100 cf flex-l">
    <div class="w-100 w5-l">
      <a
        v-if="page > 0"
        v-on:click.prevent="page = 0"
        href="#"
        class="bond-red link underline bond-link b f4 mr3"
        >First page</a
      >
      <a
        v-if="page > 0"
        v-on:click.prevent="page = page - 1"
        href="#"
        class="bond-red link underline bond-link b f4 mr3"
        >Previous page</a
      >
    </div>
    <div class="center-l pv3 pb0-l pt2-l">
      <template v-if="last_page == 1"> </template>
      <template v-else> Page {{ page + 1 }} of {{ last_page }} </template>
    </div>
    <div class="w-100 w5-l tr">
      <a
        v-if="page < last_page - 1 && last_page > 1"
        v-on:click.prevent="page = page + 1"
        href="#"
        class="bond-red link underline bond-link b f4 ml3"
        >Next page</a
      >
      <a
        v-if="page < last_page - 1 && last_page > 1"
        v-on:click.prevent="page = last_page - 1"
        href="#"
        class="bond-red link underline bond-link b f4 ml3"
        >Last page</a
      >
    </div>
  </div>
</template>

<script>
import {
  memberIsSelected,
  getFiltersFromUrl,
  debounce,
} from "../FilterStore.js";
import MemberCard from "./MemberCard.vue";
import SeparatedList from "./SeparatedList.vue";

const PAGE_SIZE = 12;

function readableFilters(filters) {
  var filtersStr = [];
  if (filters.search.length > 0) {
    filtersStr.push("Search: " + filters.search);
  }
  if (filters.country.length > 0) {
    filtersStr.push("Countries: " + filters.country.join(", "));
  }
  if (filters.sdg.length > 0) {
    filtersStr.push("SDGs: " + filters.sdg.join(", "));
  }

  return filtersStr.join("; ");
}

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
    $route: function (to) {
      this.filters = getFiltersFromUrl(to);
    },
    filters: debounce(function (to) {
      this.$gtm.trackEvent({
        event: "interaction",
        category: "Members",
        action: "change",
        label: "Filter members",
        value: readableFilters(to),
      });
    }, 500),
  },
  computed: {
    filteredMembers: function () {
      return this.members.filter((member) =>
        memberIsSelected(member, this.$route)
      );
    },
    isOrAre: function () {
      return this.filteredMembers.length == 1 ? "is" : "are";
    },
    filteredMembersCount: function () {
      var count = this.filteredMembers.length;
      if (count == 0) {
        return "None";
      } else if (count == 1) {
        return "One";
      } else if (count == 2) {
        return "Two";
      } else if (count == 3) {
        return "Three";
      } else if (count == 4) {
        return "Four";
      } else if (count == 5) {
        return "Five";
      } else if (count == 6) {
        return "Six";
      } else if (count == 7) {
        return "Seven";
      } else if (count == 8) {
        return "Eight";
      } else if (count == 9) {
        return "Nine";
      } else {
        return count;
      }
    },
    paginatedMembers: function () {
      var members = this.filteredMembers;
      return members.slice(this.page_start, this.page_end);
    },
    page_start: function () {
      return this.page * this.size;
    },
    page_end: function () {
      return Math.min(this.page_start + this.size, this.filteredMembers.length);
    },
    last_page: function () {
      return Math.ceil(this.filteredMembers.length / this.size);
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
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 1.5rem;
}

@media screen and (min-width: 60em) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
