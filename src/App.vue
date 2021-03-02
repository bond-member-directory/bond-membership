<template>
  <PageHeader />
  <template v-if="filters.memberSelected">
    <div class="w-100 bg-bond-gray mb0 mt4 f4">
      <a
        href="#"
        @click.prevent="backToAll()"
        class="w-100 bond-red link underline bond-link b"
        >&lt; Back to all members</a
      >
    </div>
    <div class="w-100 bg-bond-gray mb0 mt4 cf">
      <MemberCard
        :member="members.find((m) => m.id == filters.memberSelected)"
        :full="true"
      />
    </div>
  </template>
  <template v-else>
    <DataFilters />
    <div class="w-100">
      <a
        href="#"
        @click.prevent="showMap = !showMap"
        class="fr bond-red link underline bond-link b f5"
        ><template v-if="showMap">Hide map</template
        ><template v-else>Show map</template></a
      >
    </div>
    <div class="w-100">
      <div
        class="mb0 mt4 grid-container w-100"
        :class="{ 'with-map': showMap }"
      >
        <CardContainer />
        <div style="grid-area: map" v-if="showMap">
          <MapContainer />
        </div>
      </div>
    </div>
  </template>
</template>

<script>
import DataFilters from "./components/DataFilters.vue";
import PageHeader from "./components/PageHeader.vue";
import CardContainer from "./components/CardContainer.vue";
import MapContainer from "./components/MapContainer.vue";
import MemberCard from "./components/MemberCard.vue";
import world from "./assets/world.json";
import members from "./assets/bond_members.json";
import filterStore from "./FilterStore.js";

export default {
  name: "App",
  data: function () {
    return {
      showMap: false,
      filters: filterStore.state,
      members: Object.values(members.members).sort(
        (a, b) =>
          a.name.replace(/^(the )/i, "").toLowerCase() > b.name.replace(/^(the )/i, "").toLowerCase()
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
          c.properties["NAME_EN"],
        ])
      ),
      sdgs: members.sdgs,
      members: this.members,
    };
  },
  methods: {
    backToAll: function () {
      filterStore.clearMemberSelected();
    },
  },
  components: {
    PageHeader,
    CardContainer,
    MapContainer,
    MemberCard,
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
    "cardheader cardheader"
    "map map"
    "cards cards";
}
@media screen and (min-width:60em) {
  .grid-container.with-map {
    grid-template-areas:
      "cardheader cardheader"
      "cards map";
  }
}
</style>