import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import ky from 'ky'


const defaultRegion = '全国'


async function queryRegionsGeoInfo(exts) {

  let params = new URLSearchParams({
    key: 'e28e8e04218b803aceeffed7d28fd9c9', 
  })

  for (let [k, v] of Object.entries(exts)) {
    params.append(k, v)
  }

  const info = await ky.get('https://restapi.amap.com/v3/config/district', 
    {searchParams: params}).json();

  if (info.status != '1' || info.infocode !== '10000') {
    return null
  }

  return info.districts.shift()
}

async function fetchGeoBoundValues(districts) {

  const info = await ky.post('http://localhost:8086/endpoints/publicdebt/query', 
    {json: {districts: districts}}).json();

  return new Map(districts.map((n) => [n.adcode, Math.random() * 10000]))
}



function newGeoJson(geo, value, polyline) {
  return {
    feature: {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": polyline.split(';').map((d) => d.split(',').map((d) => parseFloat(d)))
      },
      "properties": {
        // "id": id,
        "name": geo.name,
        "adcode": geo.adcode,
        "center" : geo.center.split(',').map((d) => parseFloat(d)),
        // "adcode_n": -1,
        "adcode_p": -1,
        "adcode_c": -1,
        // "point_status": 0,
        // "创建时间": "2021-01-27 14:45:12",
        // "修改时间": "2021-01-27 14:45:12",
        "GDP": value,
      }
    },
  }
}


async function updassembleRegionsGeoJson(regions, caches, fastrefs) {

  if (regions.length > 0) {
    const queries = regions.filter((n) => !caches.has(n.adcode))
    const debtdata = await fetchGeoBoundValues(queries.map((n) => n.adcode))

    for (let target of queries) {

      const info = await queryRegionsGeoInfo({ subdistrict: 0, keywords: target.adcode, extensions: "all" })

      if (info) {
        caches.set(target.adcode, 
          newGeoJson(target, debtdata.get(target.adcode), info.polyline))
      }

    }
  }
}


export const useGeoJsonStore = defineStore('useGeoJsonStore', () => {
  // States
  // Current displaying top-region's adcode
  const adcode = ref([])
  // Current displaying regions's adcodes
  const fastrefs = ref(new Map())
  // Cached districts' geo-info
  const caches = ref(new Map())

  const geoinfo = computed(() => {
  
    return {
      type: "FeatureCollection",
      features: Array.from(fastrefs.value.values()).filter((v) => {
        if (caches.value.has(v.adcode)) {
          return true
        } else {
          console.log(`Missing adcode ${v.adcode}`)
          return false
        }
      }).map((v) => 
          caches.value.get(v.adcode).feature
      )
    }
  })

  // Getters
  const province = computed(() => {
    if (adcode.value.length > 0) {
      return caches.value.get(adcode.value.at(-1)).info.name 
    } else {
      return defaultRegion
    }
  })


  // Actions
  function reset() {
    adcode.value = []

    return true
  }

  async function regionalUpdate({scope}) {

    if (scope) {
      if (!fastrefs.value.has(scope)) {
        throw new Error(`Region ${region} not found`)
      }

      adcode.value.push(fastrefs.value.get(scope).adcode)
    }

    const area = await queryRegionsGeoInfo({subdistrict: 1})
    if (area) {
      fastrefs.value = new Map(
        area.districts.map((n) => [n.name, n]
      ))

      await updassembleRegionsGeoJson(area.districts, caches.value, fastrefs.value)

      return true
    }

    console.log(`Failed to query scope ${scope}`)
    return false
  }

  // expose attributes
  return {fastrefs, geoinfo, province, reset, regionalUpdate}
})
