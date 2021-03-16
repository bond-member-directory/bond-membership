<template>
  <div
    class="tooltip f5 pa1"
    :style="{
      top: (y - 55) + 'px',
      left: (x - 15) + 'px',
      whiteSpace: 'pre',
    }">
    {{ title }}
  </div>
</template>

<script>

export default {
  name: "WorldMapTooltip",
  props: {
    x: {
      type: Number,
      default: () => 0,
    },
    y: {
      type: Number,
      default: () => 0,
    },
    title: {
      type: String,
      default: "Tooltip",
    },
  },
};
</script>

<style scoped>
div {
  position: absolute;
  pointer-events:none;
  background-color: var(--bond-dark-red);
  color: var(--bond-white);
}
</style>