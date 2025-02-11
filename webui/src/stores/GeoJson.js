import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import ky from 'ky'

async function fetchGeoRegions(parent) {
  let lst = []
  let params = new URLSearchParams({
      key: 'e28e8e04218b803aceeffed7d28fd9c9', 
      subdistrict: 1})

  if (parent) {
    params.append('keywords', parent)
  }

  const info = await ky.get('https://restapi.amap.com/v3/config/district', 
    {searchParams: params}).json();

  for (let d of info.districts) {
    lst = lst.concat(d.districts)
  }

  return lst
}

async function updateGeoBindValues() {
  let lst = []
  // let params = new URLSearchParams({
  //     key: 'e28e8e04218b803aceeffed7d28fd9c9', 
  //     subdistrict: 1})

  // if (upper_region) {
  //   params.append('keywords', upper_region)
  // }

  // const info = await ky.get('https://restapi.amap.com/v3/config/district', 
  //   {searchParams: params}).json();

  // for (let d of info.districts) {
  //   lst = lst.concat(d.districts)
  // }

  return lst
}

function newGeoJson(id, name, geo) {
  return {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [
        geo.center.split(',').map((d) => parseFloat(d))
      ]
    },
    "properties": {
      "id": id,
      "名称": name,
      // "地址": name,
      "adcode_n": geo.adcode,
      "adcode_p": geo.province,
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

}

async function updateGeoRegions(parent, dset, vals) {
  let regions = await fetchGeoRegions(parent)

  for (let region of regions) {
    if (dset.has(region.name)) {
      continue
    }

    let geoPoint = newGeoJson(length, region.name, region)
    dset.set(region.name, geoPoint)
  }

  vals.splice(0, vals.length)

  let values = await updateGeoBindValues()

  for (let value of values) {
    if (dset.has(value.name)) {
      continue
    }

    let geoPoint = dset.get(value.name)
    setGeoJsonValue(geoPoint, value)

    vals.push(geoPoint)
  } 

}

function setGeoJsonValue(geo, value) {

}


export const useGeoJsonStore = defineStore('useGeoJsonStore', () => {
  // States
  const geojson = ref({
    features: []
  })

  const region = ref({
    province: ''
  })

  const cached = ref({
    l1: new Map(),
    l2: new Map(),
    l3: new Map(),
  })

  // Getters
  const adcode = computed(() => {
    if (cached.value.l1.has(region.province)) {
      return cached.value.l1[region.province].adcode
    } else {
      return null
    }
  })

  const metropolis = computed(() => {
    return region.adcode
  })

  // Actions
  async function updateProvinces() {
    await updateGeoRegions(null, cached.value.l1, geojson.value.features)
  }

  async function updateMetropolises(province) {
    await updateGeoRegions(province, cached.value.l2, geojson.value.features)
  }

  async function updateDistricts(metropolis) {
    await updateGeoRegions(metropolis, cached.value.l3, geojson.value.features)
  }

  // expose attributes
  return {geojson, region, cached, adcode, metropolis, updateProvinces, updateMetropolises, updateDistricts}
})
