<script setup>
import { RouterView } from 'vue-router'
import { ref, watch, isRef, isProxy } from 'vue'
import { storeToRefs } from 'pinia'

import { useGeoJsonStore } from '@/stores/GeoJson'
import NaviBarView from '@/components/NaviBarView.vue'



const defaultTitle = '地方公共债务数据'
const defaultRegion = '全国区域'

const store = useGeoJsonStore()
const { region, cached } = storeToRefs(store)

region.value.province = defaultRegion
region.value.metropolis = ''

// Data used by navi bar UI Component
const naviBarUiModel = ref({
  title: defaultTitle,
  l1: [],
  // l2: [],
})


async function onProvinceChange (selected_value) {

  if (selected_value) {

    region.value.province = selected_value

    // udpate data store
    await store.updateMetropolises (selected_value)
  
    // update ui selections
    naviBarUiModel.value.l2.splice (0, naviBarUiModel.value.l2.length, ...[...cached.value.l2.keys()])
  }
}


async function onMetropolisChange (selected_value) {
}


async function onUiReady () {
  // udpate data store
  await store.updateProvinces()

  // update ui selections
  naviBarUiModel.value.l1.splice(0, naviBarUiModel.value.l1.length, ...[...cached.value.l1.keys()])
}

function onRetTop () {
}


</script>

<template>
  <header>
    <NaviBarView v-bind="naviBarUiModel" :region="region" 
      @retTop="onRetTop" 
      @ui-ready="onUiReady"
      @changeProvince="onProvinceChange"
      @changeMetropolis="onMetropolisChange"></NaviBarView>
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
