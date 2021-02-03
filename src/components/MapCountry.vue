<template>
  <path :d="path"
    @mouseover="$emit('hoverCountry', countryProps)"
    @mouseleave="$emit('hoverCountry', {})"
    @click="$emit('selectCountry', countryProps)"
    stroke-width="0.5"
    :class="{
      'fill-bond-dark-red': countrySelected && !countryHovered,
      'fill-bond-red': countryHovered,
      'fill-bond-grey': !countryHovered && !countrySelected,
      'stroke-bond-dark-red': countrySelected && !countryHovered,
      'stroke-bond-red': countryHovered,
      'stroke-bond-grey': !countryHovered && !countrySelected,
    }"
    />
</template>

<script>
export default {
  name: 'MapCountry',
  props: {
    path: null,
    countryProps: null,
    countrySelected: Boolean,
    countryHovered: Boolean,
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