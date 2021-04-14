export function getFiltersFromUrl(route){
  var filters = {
    country: [],
    sdg: [],
    search: '',
  };
  if(Array.isArray(route.query.country)){
    filters.country = route.query.country;
  } else if(route.query.country){
    filters.country = route.query.country.split(",");
  }
  if(Array.isArray(route.query.sdg)){
    filters.sdg = route.query.sdg;
  } else if(route.query.sdg){
    filters.sdg = route.query.sdg.split(",");
  }
  if(route.query.search){
    filters.search = route.query.search;
  }
  return filters;
}

export function memberIsSelected(member, route){
  var toShow = [];
  var filters = getFiltersFromUrl(route);
  if(filters.country.length > 0){
    toShow.push(member.countries.filter((c) => filters.country.includes(c)).length > 0);
  }
  if(filters.sdg.length > 0){
    toShow.push(member.sdgs.filter((c) => filters.sdg.includes(c)).length > 0);
  }
  if(filters.search.length > 0){
    toShow.push(
      member.name.replace(/[^0-9a-z]/gi, '').toLowerCase().includes(
        filters.search.replace(/[^0-9a-z]/gi, '').toLowerCase()
      )
    );
  }
  return toShow.every((v) => v);
}

export function slugify(text){
  // https://gist.github.com/codeguy/6684588#gistcomment-3243980
  return text
    .toString()                     // Cast to string
    .toLowerCase()                  // Convert the string to lowercase letters
    .normalize('NFD')       // The normalize() method returns the Unicode Normalization Form of a given string.
    .trim()                         // Remove whitespace from both sides of a string
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w-]+/g, '')       // Remove all non-word chars
    .replace(/--+/g, '-');        // Replace multiple - with single -
}