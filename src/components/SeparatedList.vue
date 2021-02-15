<template>
    <template v-for="i in itemsExceptLast" :key="i">{{ i }}, </template>
    <template v-for="i in penultimateItem" :key="i">
        {{ i }}
        <template v-if="oxfordComma && items.length > 2">, </template>
        {{ separator }}{{ " " }}
    </template>
    <template v-for="i in lastItem" :key="i">{{ i }}</template>
</template>

<script>
export default {
  name: 'SeparatedList',
  props: {
    items: Array,
    separator: {
      type: String,
      default: () => " and ",
    },
    oxfordComma: {
        type: Boolean,
        default: () => false
    }
  },
  computed: {
      itemsExceptLast: function(){
          return this.items.slice(0, -2);
      },
      penultimateItem: function(){
          return this.items.slice(-2, -1);
      },
      lastItem: function(){
          return this.items.slice(-1);
      }
  }
}
</script>