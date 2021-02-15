import { reactive } from 'vue';

export default {
    debug: true,
  
    state: reactive({
      country: [],
      sdg: [],
      search: '',
    }),
  
    setCountry(newValue) {
      if (this.debug) {
        console.log('setCountry triggered with', newValue)
      }
      if(Array.isArray(newValue)){
        this.state.country = newValue;
      } else {
        this.state.country = [newValue];
      }
    },
  
    clearCountry() {
      if (this.debug) {
        console.log('clearCountry triggered')
      }
  
      this.state.country = [];
    },
  
    setSDG(newValue) {
      if (this.debug) {
        console.log('setSDG triggered with', newValue)
      }
  
      if(Array.isArray(newValue)){
        this.state.sdg = newValue;
      } else {
        this.state.sdg = [newValue];
      }
    },
  
    clearSDG() {
      if (this.debug) {
        console.log('clearSDG triggered')
      }
  
      this.state.sdg = [];
    },
  
    setSearch(newValue) {
      if (this.debug) {
        console.log('setSearch triggered with', newValue)
      }
  
      this.state.search = newValue;
    },
  
    clearSearch() {
      if (this.debug) {
        console.log('clearSearch triggered')
      }
  
      this.state.search = '';
    },

    memberIsSelected(member){
      var toShow = [];
      if(this.state.country.length > 0){
        toShow.push(member.countries.filter((c) => this.state.country.includes(c)).length > 0);
      }
      if(this.state.sdg.length > 0){
        toShow.push(member.sdgs.filter((c) => this.state.sdg.includes(c)).length > 0);
      }
      if(this.state.search.length > 0){
        toShow.push(
          member.name.replace(/[^0-9a-z]/gi, '').toLowerCase().includes(
            this.state.search.replace(/[^0-9a-z]/gi, '').toLowerCase()
          )
        );
      }
      return toShow.every((v) => v);
    }
  }