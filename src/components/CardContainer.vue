<template>
    <div class="w-100 bg-bond-gray pa4 flex flex-wrap">
      <MemberCard v-for="member in members"
        v-bind:key="member.id"
        :member="member"
        :countries="countries" />
    </div>
</template>

<script>
import MemberCard from './MemberCard.vue'
import members from '../assets/bond_members.json'

export default {
  name: 'CardContainer',
  data() {
    return {
      members: members.members
        .sort((a, b) => a.name.replace(/^(the )/i, "") > b.name.replace(/^(the )/i, ""))
    }
  },
  props: {
    countries: Object,
  },
  components: {
    MemberCard
  }
}
</script>