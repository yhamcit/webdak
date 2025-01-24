<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, watch, onMounted  } from 'vue'
import NaviBarView from './components/NaviBarView.vue'
import ky from 'ky'


const cached = ref({
  l1: [],
  l2: [],
  l3: [],
})

const uiModel = ref({
  title: '地方公共债务数据',
  province: '',
  metropolis: '', 
  l1: ['A', 'B', 'C'],
  l2: ['1', '2', '3'],
})

const activeRegion = ref({
  province: {name: '', adcode: '', x: null, y: null, metric: 0},
  metropolis: {name: '', adcode: '', x: null, y: null, metric: 0},
})

watch(uiModel.province, () => {
  console.log("  province changed.  ")
})

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

  cached.l2 = await updateGeoData(province.value)

  uiModel.l2 = cached.value.l2_dis_info.map((d) => d.name)
}

async function onCityChange (selected_value) {
  city.value = selected_value

  cached.l3 = await updateGeoData(city.value)
}

// onMounted(async () => {
//   cached.l1 = await updateGeoData(null)

//   uiModel.l1 = cached.l1.map((d) => d.name)
// });


async function onUiReady () {
  var lst = await updateGeoData(null)

  // cache 
  cached.value.l1.splice(0, cached.value.l1.length, ...lst)
  // cached.value.l1.concat(lst)
  // update ui selections
  uiModel.value.l1.splice(0, uiModel.value.l1.length, ...lst.map((d) => d.name))
  // uiModel.value.l1.concat(lst.map((d) => d.name))

  uiModel.value.province = "全国"
}


</script>

<template>
  <header>
    <NaviBarView v-bind="uiModel" @ui-ready="onUiReady"></NaviBarView>
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
