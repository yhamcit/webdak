<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NaviBarView from './components/NaviBarView.vue'
import ky from 'ky'


const cached = ref({
  l1_dis_info: [],
  l2_dis_info: [],
  l3_dis_info: []
})

const selectedRegion = ref({
  province: {name: undefined, adcode: '', x: null, y, metric: 0},
  metropolis: {name: undefined, adcode: '', x: null, y, metric: 0},
})

watch(selectedRegion, () => console.log(selectedRegion))



async function updateGeoData(upper_region) {

  let tmpList = []
  let params = new URLSearchParams({
      key: 'e28e8e04218b803aceeffed7d28fd9c9', 
      subdistrict: 1})

  if (upper_region) {
    params.append('keywords', upper_region)
  }

  const info = await ky.get('https://restapi.amap.com/v3/config/district', 
    {searchParams: params}).json();

  for (let d of info.districts) {
    tmpList = tmpList.concat(d.districts)
  }

  return tmpList
}


async function onProvinceChange (selected_value) {
  province.value = selected_value

  cached.value.l2_dis_info = await updateGeoData(province.value)

  cities.value = cached.value.l2_dis_info.map((d) => d.name)
}

async function onCityChange (selected_value) {
  city.value = selected_value

  cached.value.l3_dis_info = await updateGeoData(city.value)
}

onMounted(async () => {
  cached.value.l1_dis_info = await updateGeoData(null)

  provinces.value = cached.value.l1_dis_info.map((d) => d.name)
});


</script>

<template>
  <header>
    <NaviBarView title="地方公共债务" v-model="selectedRegion.province + selectedRegion.metropolis"></NaviBarView>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  background: lightsteelblue;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    flex-direction: column;
    justify-content: center;
    place-items: center;
    /* padding-right: calc(var(--section-gap) / 2); */
  }

  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>
