<template>
  <path :d="path"
    @mouseover="$emit('hoverCountry', countryProps)"
    @mouseleave="$emit('hoverCountry', {})"
    @click="$emit('selectCountry', countryProps)"
    stroke-width="0.5"
    :class="countryClasses"
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
    defaultClasses: {
      type: Array,
      default: () => ['fill-bond-grey', 'stroke-bond-grey'],
    },
    selectedClasses: {
      type: Array,
      default: () => ['fill-bond-dark-red', 'stroke-bond-dark-red'],
    },
    hoveredClasses: {
      type: Array,
      default: () => ['fill-bond-red', 'stroke-bond-red'],
    },
  },
  data() {
    return {
      hover: false,
    };
  },
  computed: {
    countryClasses: function(){
      if(this.countrySelected && !this.countryHovered){
        return this.selectedClasses;
      }
      if(this.countryHovered){
        return this.hoveredClasses;
      }
      return this.defaultClasses;
    }
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