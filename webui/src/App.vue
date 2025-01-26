<script setup>
import { RouterView } from 'vue-router'
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'

import { useGeoJsonStore } from '@/stores/GeoJson'
import NaviBarView from './components/NaviBarView.vue'



const defaultTitle = '地方公共债务数据'
const defaultRegion = '全国区域'

const cached = useGeoJsonStore()
const { region, cache } = storeToRefs(cached)

region.province = defaultRegion
region.metropolis = ''

// Data used by navi bar UI Component
const naviBarUiModel = ref({
  title: defaultTitle,
  // region: {
  //   province: defaultRegion,
  //   metropolis: '', 
  // },
  l1: [],
  l2: [],
  l3: []
})


watch(naviBarUiModel.value.region, () => {

  if (naviBarUiModel.value.region.province !== activeRegion.value.province.name) {
      onProvinceChange(naviBarUiModel.value.region.province)
      activeRegion.value.province.name = naviBarUiModel.value.region.province
      findProvinceInCache()
      updateMapDataSource()

  }
})

function updateMapDataSource() {
  mapGeoJsonSource.value.features.splice(0, mapGeoJsonSource.value.features.length)

  for (let [k, v] of cached.value.l1) {
    let geoPoint = 
    {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": [
          v.center.split(',').map((d) => {return d.parseFloat()})
				]
			},
			"properties": {
				"id": 1,
				"名称": k,
				// "地址": k,
				"adcode_n": v.adcode,
				"adcode_p": v.province,
				"adcode_c": -1,
				"adcode_d": -1,
				"point_status": 0,
				"创建时间": "2021-01-27 14:45:12",
				"修改时间": "2021-01-27 14:45:12",
				// "人口": 2884.62,
				"GDP": 7894.24,
				// "人均GDP": 27367,
				// "人均折美元": 4043
			}
		}

    mapGeoJsonSource.value.features.push(geoPoint)
  } 

}


async function updateGeoData(upper_region) {

  let lst = []
  let params = new URLSearchParams({
      key: 'e28e8e04218b803aceeffed7d28fd9c9', 
      subdistrict: 1})

  if (upper_region) {
    params.append('keywords', upper_region)
  }

  const info = await ky.get('https://restapi.amap.com/v3/config/district', 
    {searchParams: params}).json();

  for (let d of info.districts) {
    lst = lst.concat(d.districts)
  }

  return lst
}


async function onProvinceChange (selected_value) {

  await cached.updateProvinces()

  naviBarUiModel.l2 = cached.value.l2_dis_info.map((d) => d.name)
}

async function onCityChange (selected_value) {
  
  cached.l3 = await updateGeoData(city.value)
}


async function onUiReady () {
  var lst = await updateGeoData(null)

  // cache 
  for (let v of lst) {
    if (! cached.value.l1.has(v.name)) {
      cached.value.l1.set(v.name, v)
    }
  }

  // update ui selections
  naviBarUiModel.value.l1.splice(0, naviBarUiModel.value.l1.length, ...lst.map((d) => d.name))
}


</script>

<template>
  <header>
    <NaviBarView v-bind="naviBarUiModel" v-model:region="region" @ui-ready="onUiReady"></NaviBarView>
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
