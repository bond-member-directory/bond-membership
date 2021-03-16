<template>
  <path :d="path"
    :class="countryClasses"
    ref="countryPath"
  />
</template>

<script>
export default {
  name: 'MapCountry',
  props: {
    path: null,
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
      mouseLocation: null,
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
  },
};
</script>

<style scoped>
  .active {
      fill: purple;
  }
</style>