<template>
    <div class="w-100 bg-bond-gray ph4 mb0 mt4">
      <template v-if="filteredMembers.length != members.length">
        Showing {{ filteredMembers.length }} of {{ members.length }} members
        <p v-if="(filters.country.length > 0) && (filters.sdg.length > 0)">
          Showing members working on Sustainable Development Goal <separated-list :items="sdgNames" separator=" or " />
          and working in <separated-list :items="countryNames" separator="or" />
        </p>
        <p v-else-if="filters.country.length > 0">
          Showing members working in <separated-list :items="countryNames" separator="or" />
        </p>
        <p v-else-if="filters.sdg.length > 0">
          Showing members working on Sustainable Development Goal <separated-list :items="sdgNames" separator=" or " />
        </p>
      </template>
      <template v-else>Showing {{ members.length }} members</template>
    </div>
    <div class="w-100 bg-bond-gray pa4 smol-css-grid card-grid">
      <MemberCard v-for="member in filteredMembers"
        v-bind:key="member.id"
        :member="member" />
    </div>
</template>

<script>
import filterStore from "../FilterStore.js";
import MemberCard from './MemberCard.vue'
import SeparatedList from './SeparatedList.vue'

export default {
  name: 'CardContainer',
  inject: ['members', "countries", "sdgs"],
  components: {
    MemberCard,
    SeparatedList,
  },
  data: function(){
    return {
      filters: filterStore.state
    }
  },
  computed: {
    filteredMembers: function(){
      return this.members.filter((member) => filterStore.memberIsSelected(member))
    },
    countryNames: function(){
      return this.filters.country.map((c) => this.countries[c]);
    },
    sdgNames: function(){
      return this.filters.sdg.map((c) => this.sdgs[c]);
    },
  },
}
</script>

<style scoped>
.card-grid {
  --min: 30ch;
  --gap: 1rem;
}
</style>