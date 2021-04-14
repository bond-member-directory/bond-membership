<template>
  <div class="w-100 bg-bond-gray mb0 mt4 f4">
    <router-link to="/" class="w-100 bond-red link underline bond-link b">&lt; Back to all members</router-link>
  </div>
  <div class="w-100 bg-bond-gray mb0 mt4 cf">
    <MemberPage
      :member="members.find((m) => slugify(m.name) == $route.params.id)"
    />
  </div>
</template>

<script>
import MemberPage from "../components/MemberPage.vue";
import { slugify } from "../FilterStore.js";

export default {
  name: "Member",
  inject: ['world', 'members'],
  components: {
    MemberPage,
  },
  methods: {
    slugify: slugify
  }
};
</script>
