<template>
  <PageHeader />
  <router-view/>
</template>

<script>
import PageHeader from "./components/PageHeader.vue";
import world from "./assets/world.json";
import members from "./assets/bond_members.json";

export default {
  name: "App",
  data: function () {
    return {
      members: Object.values(members.members).sort(
        (a, b) =>
          a.name.replace(/^(the )/i, "").toLowerCase().localeCompare(b.name.replace(/^(the )/i, "").toLowerCase())
      ),
    };
  },
  provide() {
    world.features = world.features.filter(
      (b) => b.properties["ISO_A2"] != "AQ"
    );
    return {
      world: world,
      countries: Object.fromEntries(
        world.features.map((c) => [
          c.properties["ISO_A2"],
          c.properties["NAME"],
        ])
      ),
      sdgs: members.sdgs,
      members: this.members,
    };
  },
  components: {
    PageHeader,
  },
};
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: 50% auto;
  grid-template-rows: auto;
  grid-template-areas:
    "cardheader cardheader"
    "cards cards";
}
.grid-container.with-map {
  display: grid;
  grid-template-columns: 50% auto;
  grid-template-rows: auto;
  grid-template-areas:
    "map map"
    "cardheader cardheader"
    "cards cards";
}
@media screen and (min-width:60em) {
  .grid-container.with-map {
    grid-template-areas:
      "map map"
      "cardheader cardheader"
      "cards cards";
  }
}
</style>