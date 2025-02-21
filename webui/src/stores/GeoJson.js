import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import ky from 'ky'


const defaultRegion = '全国'


async function fetchAllGeoRegions(dtlvl, {upper}) {

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
    return []
  }

  return info.districts[0].districts
}

async function fetchGeoBoundValues(districts) {
  let res = new Map()

  const info = await ky.post('http://localhost:8086/endpoints/publicdebt/query', 
    {json: {districts: districts}}).json();


  // TODO: Mock values here
  for (let dst of districts) {
    let {name, adcode, gdp =7894.24} = dst
    res.set(dst.adcode, {name: name, adcode: adcode, gdp: gdp})
  // TODO: Mock values here
  }

  return res
}



function newGeoJson(id, geo, info) {
  return {
    feature: {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": geo.center.split(',').map((d) => parseFloat(d))
      },
      "properties": {
        "id": id,
        "名称": geo.name,
        // "地址": name,
        "adcode_n": -1,
        "adcode_p": -1,
        "adcode_c": -1,
        "adcode_d": -1,
        "point_status": 0,
        "创建时间": "2021-01-27 14:45:12",
        "修改时间": "2021-01-27 14:45:12",
        "GDP": info.gdp,
      }
    },
    info: info,
  }
}


async function updateGeoRegionsJson(collection, cached) {

  if (collection.length  > 0) {
    let queryset = collection.reduce((acc, v) => {
      if (!cached.has(v.adcode)) {
        acc.push(v)
      }
      return acc
    }, [])

    let debtresults = await fetchGeoBoundValues(queryset)

    for (let region of collection) {
      cached.set(region.adcode, 
                 newGeoJson(length, region, debtresults.get(region.adcode)))
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
      features: Array.from(fastrefs.value.values()).map((v) => caches.value.get(v).feature)
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

  function updateRegions(collection) {
    for (let region of collection) {
      fastrefs.value.set(region.name, region.adcode)
    }
  }

  async function regionalUpdate({upper}) {

    if (upper) {
      if (!fastrefs.value.has(upper)) {
        throw new Error(`Region ${region} not found`)
      }

      targets.push(fastrefs.value.get(upper))

      adcode.value.push(targets.at(-1))
    }

    let collection = await fetchAllGeoRegions(1, {upper})

    fastrefs.value = new Map(collection.map((item) => [item.name, item.adcode]))

    await updateGeoRegionsJson(collection, caches.value)

    return true
  }

  // expose attributes
  return {fastrefs, geoinfo, province, reset, regionalUpdate}
})
