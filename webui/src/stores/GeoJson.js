import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import ky from 'ky'


const defaultRegion = '全国'

/**
 * Douglas-Peucker 抽稀算法（支持闭合环）
 * @param {Array<[number, number]>} points 原始坐标点数组
 * @param {number} epsilon 容差（单位：经纬度差值）
 * @returns {Array<[number, number]>} 抽稀后的坐标点数组
 */
function douglasPeucker(points, epsilon) {
  if (points.length <= 2) return points;

  // 处理闭合环：将闭合点临时移除，抽稀后再闭合
  const isClosed = JSON.stringify(points[0]) === JSON.stringify(points[points.length - 1]);
  const workPoints = isClosed ? points.slice(0, -1) : points;

  // 递归抽稀
  const simplified = [];
  let maxDist = 0;
  let index = 0;

  // 计算点到基线的最大垂直距离
  const [start, end] = [workPoints[0], workPoints[workPoints.length - 1]];
  for (let i = 1; i < workPoints.length - 1; i++) {
      const dist = perpendicularDistance(workPoints[i], start, end);
      if (dist > maxDist) {
          maxDist = dist;
          index = i;
      }
  }

  // 递归处理
  if (maxDist > epsilon) {
      const left = douglasPeucker(workPoints.slice(0, index + 1), epsilon);
      const right = douglasPeucker(workPoints.slice(index), epsilon);
      simplified.push(...left.slice(0, -1), ...right);
  } else {
      simplified.push(start, end);
  }

  // 重新闭合环
  return isClosed ? [...simplified, simplified[0]] : simplified;
}

// 计算点到线段的最短垂直距离
function perpendicularDistance(point, lineStart, lineEnd) {
  const [x, y] = point;
  const [x1, y1] = lineStart;
  const [x2, y2] = lineEnd;

  const area = Math.abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1);
  const lineLength = Math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2);
  return lineLength === 0 ? 0 : area / lineLength;
}

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


async function fetchStaticGeoPolygons(adcode, level) {

  const info = await ky.get(`http://localhost:8086/static/adcode-${adcode}-${level}.gz`, 
    { headers: {
      'Accept-Encoding': 'gzip', 
      'content-type': 'application/json'
    }}).json();

  return info
}

function geoProperties(geo, value) {
  return {
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
}

function newGeoJson(geo, value, polyline) {
  return {
    feature: {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": polyline.split(';').map((d) => d.split(',').map((d) => parseFloat(d)))
      },
      "properties": geoProperties(geo, value),
    },
  }
}


async function updassembleRegionsGeoJson(regions, caches, fastrefs) {

  if (regions.length > 0) {
    const debtdata = await fetchGeoBoundValues(regions.map((n) => n.adcode))

    const queries = regions.filter((n) => !caches.has(n.adcode))

    for (let target of queries) {
      if (caches.has(target.adcode)) {
        geo = caches.get(target.adcode)
        geo.properties = geoProperties(target, debtdata.get(target.adcode))
        continue
      }

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
  const showLowerLevel = ref(false)
  // Current displaying top-region's adcode
  const adcode = ref(['100000'])
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
      }).map((v) => {
          let item = caches.value.get(v.adcode)

          item.geometry = {type: "Polygon", coordinates: [douglasPeucker(item.geometry.coordinates[0], 0.001)]}
          return item
      })
    }
  })

  // Getters
  const province = computed(() => {
    if (adcode.value.length > 1) {
      return caches.value.get(adcode.value[adcode.value.length - 1]).info.name 
    } else {
      return defaultRegion
    }
  })

  const dislevel = computed(() => {
    if (showLowerLevel.value) {
      return 2
    } else {
      return 1
    }
  })


  // Actions
  async function reset() {

    adcode.value.splice(1, adcode.value.length - 1)

    let geos = await fetchStaticGeoPolygons(adcode.value[adcode.value.length - 1], dislevel.value)

    caches.value = new Map(
      geos.features.map((n) => [n.properties.adcode, n])
    )

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
