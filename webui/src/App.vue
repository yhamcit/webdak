<script setup>
import { RouterView } from 'vue-router'
import { ref, watch, isRef, isProxy } from 'vue'
import { storeToRefs } from 'pinia'

import { useGeoJsonStore } from '@/stores/GeoJson'
import NaviBarView from '@/components/NaviBarView.vue'



const defaultTitle = '地方公共债务数据'

const store = useGeoJsonStore()
const { fastrefs, province } = storeToRefs(store)


// Data used by navi bar UI Component
const naviBarUiModel = ref({
  title: defaultTitle,
  l1: [],
})

// resetRegion()

async function onRegionChange (upper) {
  if (upper) {
    await store.regionalUpdate({upper})
  }
}


function resetRegion() {
  store.reset()

  // update ui selections
  naviBarUiModel.value.l1.splice(0, naviBarUiModel.value.length, 
    ...Array.from(fastrefs.value.keys()))
}


async function onUiReady() {
  // udpate data store
  await store.regionalUpdate({})

  resetRegion()
}


function onReturnUpper() {
  resetRegion()
}


</script>

<template>
  <header>
    <NaviBarView v-bind="naviBarUiModel" :province="province" 
      @returnUpper="onReturnUpper" 
      @ui-ready="onUiReady"
      @changeRegion="onRegionChange"
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
