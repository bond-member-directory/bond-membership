<template>
  <div class="w-100 bg-bond-gray mb0 mt4 f4">
    <router-link to="/" class="w-100 bond-red link underline bond-link b">&lt; Back to all members</router-link>
  </div>
  <div class="w-100 bg-bond-gray mb0 mt4 cf">
    <MemberCard
      :member="members.find((m) => m.id == $route.params.id)"
      :full="true"
    />
  </div>
</template>

<script>
import MemberCard from "../components/MemberCard.vue";

export default {
  name: "Member",
  inject: ['world', 'members'],
  components: {
    MemberCard,
  },
};
</script>
