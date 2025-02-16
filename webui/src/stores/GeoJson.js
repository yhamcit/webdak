import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import ky from 'ky'


const defaultRegion = '全国'


async function* fetchGeoRegions(dtlvl, ...parents) {

  if (parents.length == 0) {
    parents = [null]
  }

  for (let upper of parents) {
    let params = new URLSearchParams({
      key: 'e28e8e04218b803aceeffed7d28fd9c9', 
      subdistrict: dtlvl,
    })

    if (upper) {
      params.append('keywords', upper)
    }

    const info = await ky.get('https://restapi.amap.com/v3/config/district', 
      {searchParams: params}).json();

    if (info.status != '1' || info.infocode !== '10000') {
      break
    }

    yield info.districts[0].districts
  }
}

async function updateGeoBoundValues(districts) {
  let res = new Map()

  const info = await ky.post('https://web.cdyhamc.com/endpoints/publicdebt/query', 
    {json: {districts: districts}}).json();

  for (let dst of districts) {
    res[dst] = 7894.24
  }

  return res
}


function newGeoJson(id, geo, gdp) {
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
      "名称": geo.name,
      // "地址": name,
      "adcode_n": geo.adcode,
      "adcode_p": geo.province,
      "adcode_c": -1,
      "adcode_d": -1,
      "point_status": 0,
      "创建时间": "2021-01-27 14:45:12",
      "修改时间": "2021-01-27 14:45:12",
      // "人口": 2884.62,
      "GDP": gpd,
      // "人均GDP": 27367,
      // "人均折美元": 4043
    }
  }

}

async function updateGeoRegions(parent, dset) {
  let dst_lst = []

  for await (const regions of fetchGeoRegions(1, parent)) {

    for (let region of regions) {

      if (dset.has(region.adcode)) {
        continue
      }

      dst_lst.push(region.name)
    }
  }

  if (dst_lst.length > 0) {
    let debts = await updateGeoBoundValues(dst_lst)
    for (let [key, value] of debts) {

      dset.set(region.adcode, newGeoJson(length, key, value))
    }
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
    province: defaultRegion
  })

  const cached = ref(new Map())

  // Getters
  const adcode = computed(() => {
    if (cached.value.has(region.province)) {
      return cached.value[region.province].adcode
    } else {
      return null
    }
  })

  function reset() {
    region.value.province = defaultRegion
  }

  // Actions
  async function initTopRegions() {
    await updateGeoRegions(null, cached.value)
  }

  async function updateMetropolises(province) {

    geojson.value.features.splice(0, vals.length)

    // await updateGeoRegions(province, cached.value.l2, geojson.value.features)
  }

  // expose attributes
  return {geojson, region, cached, adcode, reset, initTopRegions, updateMetropolises}
})
