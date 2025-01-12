<script setup>

import { ref, onMounted } from 'vue';
import ky from 'ky'


defineProps({
  title: {
    type: String,
    required: true,
  },
  province: {
    type: String,
    required: true,
  },
})

function onProvinceChange (selected_value) {
  province = selected_value
}

function onCityChange (selected_value) {
  province = selected_value
}

async function getDistricts(region) {
  let params = new URLSearchParams({
      key: 'e28e8e04218b803aceeffed7d28fd9c9', 
      subdistrict: 1})

  if (region) {
    params.append(keywords, "region")
  }

  const info = await ky.get('https://restapi.amap.com/v3/config/district', 
    {searchParams: params}).json();

  console.log(info)
  return info.districts
}

var provinces = ref([])
var cities = ref(['A', 'B', 'C'])

onMounted(async () => {
  let tmpProvinces = []
  const country = await getDistricts(null)

  console.log(country)

  for (let p of country.districts) {
    tmpProvinces = tmpProvinces.concat(p.districts.map(p => p.name))
  }

  console.log(tmpProvinces)
  provinces.value = tmpProvinces
  });

</script>

<template>
  <div class="Titile">
    <h1>{{ title }}</h1>
  </div>

  <div class="wrapper">
    <h3>{{ province }}</h3>

    <div class="wrapper">
      <v-select label="- 选择省 -"
        v-model="province"
        :items="provinces"
        @update:model-value="onProvinceChange"
        >
      </v-select>
      <v-select label="- 选择市 -"
        v-model="city"
        :items="cities"
        @update:model-value="onCityChange"
        >
      </v-select>
    </div>

    <nav>
      <RouterLink to="/">地图</RouterLink>
      <RouterLink to="/data">数据</RouterLink>
    </nav>

  </div>

</template>

<style scoped>
/* div .Titile {
  display: flex;
    flex-direction: column;
    justify-content: center;
    place-items: center;
} */

div .Tools {
  display: flex;
    flex-direction: row;
    justify-content: center;
    place-items: center;
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}


nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  /* margin-top: 2rem; */
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
  

  nav {
    text-align: left;
    /* margin-left: -1rem; */
    font-size: 1rem;

    /* padding: 1rem 0; */
    /* margin-top: 1rem; */
  }


  .wrapper {
    display: flex;
    flex-direction: row;
    /* flex-wrap: wrap; */
    justify-content: center;
    /* place-items: flex-start; */
    place-items: center;
    width: 100%;
  }

}
</style>
