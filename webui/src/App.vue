<script setup>
import { RouterView } from 'vue-router'
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia'

import { useGeoJsonStore } from '@/stores/GeoJson'
import NaviBarView from './components/NaviBarView.vue'



const defaultTitle = '地方公共债务数据'
const defaultRegion = '全国区域'

const store = useGeoJsonStore()
const { region, cached } = storeToRefs(store)

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


watch(region.province, () => {

  if (region.province !== activeRegion.value.province.name) {
      onProvinceChange(region.province)

      
      updateMapDataSource()
  }
})


async function onProvinceChange (selected_value) {
  // udpate data store
  await store.updateMetropolises()

  // update ui selections
  naviBarUiModel.value.l2.splice(0, naviBarUiModel.value.l2.length, ...[...cached.value.l2.values()])
}


async function onCityChange (selected_value) {
  // udpate data store
  await store.updateDistricts()

  // update ui selections
  naviBarUiModel.value.l3.splice(0, naviBarUiModel.value.l3.length, ...[...cached.value.l3.values()])
}


async function onUiReady () {
  // udpate data store
  await store.updateProvinces()

  // update ui selections
  naviBarUiModel.value.l1.splice(0, naviBarUiModel.value.l1.length, ...[...cached.value.l1.keys()])
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
