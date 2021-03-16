<template>
  <DataFilters />
  <CardContainer />
</template>

<script>
import DataFilters from "../components/DataFilters.vue";
import CardContainer from "../components/CardContainer.vue";

export default {
  name: "Home",
  inject: ['members', 'world'],
  components: {
    CardContainer,
    DataFilters,
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