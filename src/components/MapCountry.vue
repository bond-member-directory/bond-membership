<template>
  <path :d="path"
    @mouseover="onHover()"
    @mouseleave="leaveHover()"
    :class="{ 'fill-bond-red': countrySelected }"
    />
</template>

<script>
export default {
  name: 'MapCountry',
  props: {
    path: null,
    countryProps: null,
    countrySelected: {
        type: Boolean,
        default: false
    },
  },
  data() {
    return {
      hover: false,
    };
  },
  methods: {
    onHover: function(){
        this.$emit('selectCountry', this.countryProps);
    },
    leaveHover: function(){
        this.$emit('selectCountry', {});
    },
  },
};
</script>

<style scoped>
    .active {
        fill: purple;
    }
</style>