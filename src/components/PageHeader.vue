<template>
  <header class="w-100 bg-white mb3 cf">
    <div class="w-100 f4 flex-l">
        <h1 class="bond-mid-grey header-text normal f1 f2 mt0 mb3 w100 w-50-l">Members Directory</h1>
        <div class="ml-auto-l pv3 normal">
          <p class="measure f5 ma0 pa0 lh-copy tl">
            Browse the international development organisations that are members of 
            <a href="https://www.bond.org.uk/about-us" target="_blank" class="bond-red link underline bond-link b">the Bond network</a>, 
            and see which countries they work in and which Sustainable Development Goals they focus on.
          </p>
          <!--<p class="measure f5 ma0 pa0 lh-copy">
            You can view the results of your search as a listing or a map. You can also search by an 
            organisation’s name. 
          </p>-->
          <p class="measure f5 ma0 pa0 lh-copy tl">
            If you have any feedback on this directory, please 
            <a href="https://www.bond.org.uk/contact-us" target="_blank" class="bond-red link underline bond-link b">get in touch</a>.
          </p>
        </div>
    </div>
  </header>
</template>

<script>

export default {
  name: 'PageHeader',
}
</script>

<style scoped>
.header-text {
  font-weight: 200;
  /* padding-top: 30px; */
}
</style>