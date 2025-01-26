import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import ky from 'ky'

async function updateGeoRestapi(upper_region) {

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



export const useGeoJsonStore = defineStore('useGeoJsonStore', () => {
  const geojson = ref({
    features: []
  })
  const region = ref({
    province: '',
    metropolis: ''
  })
  const cache = ref({
    l1: new Map(),
    l2: new Map(),
    l3: new Map(),
  })
  const getProvinces = computed(() => {
    return []
  })
  const getMetroPolises = computed(() => {
    return []
  })
  async function updateProvinces() {
    let lst = await updateGeoRestapi(null)

    for (let v of lst) {
      if (! cache.value.l1.has(v.name)) {
        cache.value.l1.set(v.name, v)
      }
    }
  

  }
  async function updateMetropolises(province) {
    let lst = await updateGeoRestapi(null)

  }
  async function updateDistricts() {

  }


  return {geojson, region, cache, getProvinces, getMetroPolises, updateProvinces, updateMetropolises, updateDistricts}
})
