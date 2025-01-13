<script setup>

import { ref, onMounted } from 'vue';
import ky from 'ky'


defineProps({
  title: {
    type: String,
    required: true,
  },
  // des: {
  //   type: String,
  //   required: true,
  // },
})


const provinces = ref([])
const cities = ref([])

const l1_dis_info = ref([])
const l2_dis_info = ref([])
const l3_dis_info = ref([])

const province = ref('')
const city = ref('')

// var { province, city } = defineModel()
async function getDistricts(region) {
  let params = new URLSearchParams({
      key: 'e28e8e04218b803aceeffed7d28fd9c9', 
      subdistrict: 1})

  if (region) {
    params.append('keywords', region)
  }

  const info = await ky.get('https://restapi.amap.com/v3/config/district', 
    {searchParams: params}).json();

  return info.districts
}


async function onProvinceChange (selected_value) {
  province.value = selected_value

  l2_dis_info.value = await updateDistricts(province.value)

  cities.value = l2_dis_info.value.map((d) => d.name)
}

async function onCityChange (selected_value) {
  city.value = selected_value

  l3_dis_info.value = await updateDistricts(city.value)
}

async function updateDistricts(upper_region) {

  let tmpList = []
  const districts = await getDistricts(upper_region)

  console.log(districts)

  for (let d of districts) {
    tmpList = tmpList.concat(d.districts)
  }

  console.log(tmpList)
  return tmpList
}

onMounted(async () => {
  l1_dis_info.value = await updateDistricts(null)

  provinces.value = l1_dis_info.value.map((d) => d.name)
});

</script>

<template>
  <div class="Titile">
    <h1>{{ title }}</h1>
  </div>

  <div class="wrapper">
    <h3>{{ `${province} ${city}` }}</h3>

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
