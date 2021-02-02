<template>
    <div class="w5 fl bg-bond-grey br2 mr3 mb3">
      <header class="w-100 bg-bond-dark-red white pa2 br2 br--top">
        {{ member.name }}
      </header>
      <div class="w-100 pa2">
        <div v-if="member.country.length > 0">
          Works in:
          <ul>
            <li v-for="country in member.country" v-bind:key="country">
              {{ countries[country] }} ({{ country }})
            </li>
          </ul>
        </div>
        <div v-if="member.sdg.length > 0">
          Works on:
          <ul class="list ma0 pa0 flex flex-wrap">
            <li v-for="sdg in member.sdg" v-bind:key="sdg" class="di w3 h3 fl mb1 mr1">
              <img :src="sdgIcon(sdg)" :title="sdg" />
            </li>
          </ul>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'MemberCard',
  props: {
    member: Object,
    countries: Object,
  },
  methods: {
    sdgIcon: function(sdg){
      var SDG_list = {
        "No Poverty": "01",
        "Zero Hunger": "02",
        "Good Health and Well-being": "03",
        "Quality Education": "04",
        "Gender Equality": "05",
        "Clean Water and Sanitation": "06",
        "Affordable and Clean Energy": "07",
        "Decent Work and Economic Growth": "08",
        "Industry, Innovation and Infrastructure": "09",
        "Reducing Inequality": "10",
        "Reduced inequalities": "10",
        "Sustainable Cities and Communities": "11",
        "Responsible Consumption and Production": "12",
        "Climate Action": "13",
        "Life Below Water": "14",
        "Life On Land": "15",
        "Peace, Justice, and Strong Institutions": "16",
        "Partnerships for the Goals": "17",
      }

      var cleanString = function(s){
        return s.toLowerCase().replace(/[^a-z0-9]/gmi, "");
      }

      SDG_list = Object.fromEntries(
        Object.entries(SDG_list).map(([k, v]) => [cleanString(k), v])
      );
      sdg = cleanString(sdg);
      return require("../assets/images/sdgs/E-WEB-Goal-" + SDG_list[sdg] + ".png");
    }
  }
}
</script>