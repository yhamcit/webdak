<script setup>

// const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')

import { watch, onMounted, onUnmounted } from "vue";
import { storeToRefs } from 'pinia'

import { useGeoJsonStore } from '@/stores/GeoJson'

import AMapLoader from '@amap/amap-jsapi-loader';


const store = useGeoJsonStore()
const { geoinfo } = storeToRefs(store)


const emit = defineEmits(['change-region', 'map-ready'])

let {map, chart} = {map: null, chart: null}
// var map = undefined;
var colors = {};
// 定义颜色停止点
const colorStops = [
  { stop: 0, color: hex2rgbColor("#1c6390") }, 
  { stop: 0.5, color: hex2rgbColor("#f4e1e1") }, 
  { stop: 1, color: hex2rgbColor("#9f383d") }, 
]


const status = {ready: false, loaded: false}


// store.$subscribe((mutation, state) => {
//   if (!state.adcode) {
//     console.log('state.adcode is empty')
//   } else {
//     console.log('state.adcode is not empty') 
//   }
// })

store.$onAction(({name, store, args, after, onError }) => {
  console.log('Pinia data store action probed: ', name, "arguments: ", args);

  if (name === 'regionalUpdate') {

    after((result) => {
      if (result) {
        updateChartLayerData()
      }
    });
    onError((error) => {
      console.log('Error happend during regionalUpdate action: ', error)
    });

  } else if (name === 'reset') {

    after((result) => {
      if (result) {
        //updatePrismLayerData()
      }
    });
    onError((error) => {
      console.log('Error happend during reset action: ', error)
    });

  }
})

// watch(province, async (newVal, oldVal) => {
//     console.log('region.province changed:', newVal, oldVal)
//   },
//   { 
//     deep: true 
//   })

function resetMap() {
  if (map) {
    map.destroy();
  }
  map = null
}

onMounted(async () => {
  window._AMapSecurityConfig = {securityJsCode: "cf5dba8895ae3f072aa48bc8be4c0db3",};

  resetMap()

  await AMapLoader.load({
    key: "33300d9b8a904f22b218486056876efa",
    version: "2.0",
    plugins: ["AMap.Scale"],
    Loca: {
        version: '2.0'
    }
  })
  .then((AMap) => {
    map = initAMapWithLayers(AMap);
  })
  .catch((e) => {
    console.log(e);
  });
});

onUnmounted(() => {
  resetMap()
});



function hex2rgbColor(hex) {
  // 去掉 # 号
  hex = hex.replace(/^#/, '');
  // 解析为 R, G, B
  const bigint = parseInt(hex, 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return [r, g, b];
}

function rgbStr2rgbColor(rgb) {
  return rgb.match(/\d+/g).map(Number);
}

function rgbColor2hex(rgb) {
  return '#' + rgb.map(x => {
    const hex = x.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }).join('');
}

function interpolateColor(color1, color2, factor) {
  const result = color1.slice();
  for (let i = 0; i < 3; i++) {
    result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
  }
  return result;
}

function getColorAtPosition(position, colorStops) {
  // 找到最近的两个颜色停止点
  let startIndex = 0;
  for (let i = 0; i < colorStops.length; i++) {
    if (colorStops[i].stop >= position) {
      startIndex = i - 1;
      break;
    }
  }
  if (startIndex < 0) startIndex = 0;

  const startStop = colorStops[startIndex];
  const endStop = colorStops[startIndex + 1];

  // 计算插值因子
  const factor = (position - startStop.stop) / (endStop.stop - startStop.stop);

  // 插值计算颜色
  const interpolatedColor = interpolateColor(startStop.color, endStop.color, factor);

  // return `rgb(${interpolatedColor.join(',')})`;
  return interpolatedColor
}


var getColorByAdcode = function (adcode) {

  if (!colors[adcode]) {
    // 示例：获取 (random)% 处的颜色
    const rgb = getColorAtPosition(Math.random(), colorStops);
    // console.log('Color at 25%:', color); // 输出颜色值
    // var gb = Math.random() * 155 + 50;
    // colors[adcode] = 'rgb(' + gb + ',' + gb + ',255)';
    colors[adcode] = rgbColor2hex(rgb);
  }

  return colors[adcode];
};


function createMapWithAMap(AMap, handlers) {
  window.movingDraw = true;

  var countryLayer = new AMap.DistrictLayer.Country({
      zIndex: 2,
      opacity: 0.6, 
      SOC: 'CHN',
      depth: 1,
      styles: {
        'nation-stroke': '#f09',
        'coastline-stroke': [0.85, 0.63, 0.94, 1],
        'province-stroke': 'white',
        'city-stroke': 'rgba(255,255,255,0.15)',
        'fill': function (props) {
          return getColorByAdcode(props.adcode_pro)
        }
      }
    })

  let map = new AMap.Map('mapContainer', {
    zoom: 5.2,
    showLabel: false,
    viewMode: '3D',
    visible: false,
    pitch: 45,
    center: [108.940174, 34.341568],  // center: [103.594884, 36.964587],
    // center: [120.109233,30.246411],
    showLabel: false,
    rotateEnable: false,
    doubleClickZoom: false, 
    showBuildingBlock: false,
    layers: [
      countryLayer,
    ],
    mapStyle: 'amap://styles/dark',
  });

  Object.entries(handlers).forEach(([event, handler]) => {
    map.on(event, handler);
  });


  return map
}

function createChartLayer(map) {

  // var layer = new Loca.PrismLayer({
  //   zIndex: 10,
  //   opacity: 0.8,
  //   visible: false,
  //   hasSide: true,
  // });

  var layer = new Loca.PolygonLayer({
    // loca,
    zIndex: 10,
    opacity: 0.8,
    // cullface: 'none',
    shininess: 10,
    hasSide: true,
  });

  let container = new Loca.Container({
    map,
  });

  container.ambLight = {
    intensity: 0.7,
    color: '#7b7bff',
    // color: 'lightsteelblue',
  };

  container.dirLight = {
    intensity: 0.8,
    color: '#fff',
    // color: 'lightsteelblue',
    target: [0, 0, 0],
    position: [0, -1, 1],
  };

  container.pointLight = {
    color: 'rgb(240,88,25)',
    position: [112.028276, 31.58538, 2000000],
    intensity: 3,
    distance: 5000000,
  };

  container.add(layer)

  // 图例
  new Loca.Legend({
      loca: container,
      title: {
          label: '债务占比',
          fontColor: '#eee',
      },
      style: {
          backgroundColor: 'rgba(255,255,255,0.1)',
          left: '20px',
          bottom: '40px',
      },
      dataMap: [
          { label: '350%', color: rgbColor2hex(getColorAtPosition(1.0, colorStops)) },
          { label: '300%', color: rgbColor2hex(getColorAtPosition(0.9, colorStops)) },
          { label: '250%', color: rgbColor2hex(getColorAtPosition(0.8, colorStops)) },
          { label: '200%', color: rgbColor2hex(getColorAtPosition(0.7, colorStops)) },
          { label: '250%', color: rgbColor2hex(getColorAtPosition(0.6, colorStops)) },
          { label: '100%', color: rgbColor2hex(getColorAtPosition(0.5, colorStops)) },
          { label: '<90%', color: rgbColor2hex(getColorAtPosition(0.4, colorStops)) },
          { label: '<80%', color: rgbColor2hex(getColorAtPosition(0.3, colorStops)) },
          { label: '<70%', color: rgbColor2hex(getColorAtPosition(0.2, colorStops)) },
          { label: '<60%', color: rgbColor2hex(getColorAtPosition(0.1, colorStops)) },
      ].reverse(),
  });

  return layer;
}

function initAMapWithLayers(AMap) {
  map = createMapWithAMap(AMap, {
    click: 
      (ev) => {
        var px = ev.pixel;

        // var props = countryLayer.getDistrictByContainerPos(px);
        // if (props) {
        //   if (typeof props.province !== 'undefined' && props.province) {
        //     props.province = undefined;
        //   } else {
        //     let provinceLayer = putProvinceLayerOntop(map, props)
        //     zoomInProvice(pl, provinceLayer, countryLayer, props)
        //     region.province = props.NAME_CHN
        //     region.adcode_pro = props.adcode_pro
        //   }
        // }
      }, 
    complete: 
      () => { 
        emit('map-ready', 'amap')
      },
    mousemove:
      () => {}
  })

  chart = createChartLayer(map)
}


function updateChartLayerData() {
  // // if (!status.ready || status.loaded) {
  // //     return
  // // }

  // var geo = new Loca.GeoJSONSource({
  //     url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/hz_gn.json',
  // });

  var geo = new Loca.GeoJSONSource({
    data: geoinfo.value,
  });
  chart.setSource(geo);

  chart.setStyle({
    altitude: 0,
    topColor: (index, f) =>  getColorByAdcode(f.properties.adcode),
    sideTopColor: (index, f) => getColorByAdcode(f.properties.adcode),
    sideBottomColor: (index, f) => getColorByAdcode(f.properties.adcode),
    // radius: 15000,
    height: function (index, feature) {
      return Math.random() * 200000
    },
  });

  // prismlayer.setStyle({
  //   unit: 'meter',
  //   sideNumber: 4,
  //   topColor: (index, f) => {
  //     var n = f.properties['GDP'];
  //     return n > 7000 ? '#E97091' : '#2852F1';
  //   },
  //   sideTopColor: (index, f) => {
  //     var n = f.properties['GDP'];
  //     return n > 7000 ? '#E97091' : '#2852F1';
  //   },
  //   sideBottomColor: '#002bb9',
  //   radius: 15000,
  //   height: (index, f) => {
  //     var props = f.properties;
  //     var height = Math.max(100, Math.sqrt(props['GDP']) * 9000 - 50000);
  //     return height;
  //   },
  //   rotation: 360,
  //   altitude: 0,
  // });

  showPrismLayerAnimations()
}

function showPrismLayerAnimations() {
  setTimeout(function () {
      chart.show(500);

      chart.addAnimate({
          key: 'height',
          value: [0, 1],
          duration: 1000,
          easing: 'CubicInOut',
        }, function () {
          console.log('Map loading completed: Animation done');
      });

      // prismlayer.addAnimate({
      //   key: 'height',
      //   value: [0, 1],
      //   duration: 500,
      //   easing: 'Linear',
      //   transform: 2000,
      //   random: true,
      //   delay: 3000,
      // }, function () {
      //     console.log('Map loading completed: Animation done');
      // });
    }, 
    600);
}

// function putProvinceLayerOntop(map, targetProv) {

//   var fg = new AMap.DistrictLayer.Province({
//     zIndex: 6,
//     opacity: 0.6,
//     adcode: targetProv.adcode_pro,
//     depth: 1,
//     styles: {
//       'fill': function (properties) {
//         var adcode = properties.adcode;
//         return getColorByAdcode(adcode);
//       },
//       'province-stroke': 'cornflowerblue',
//       'city-stroke': 'white', // 中国地级市边界
//       'county-stroke': 'rgba(255,255,255,0.5)' // 中国区县边界
//     }
//   });

//   fg.setMap(map);

//   return fg
// }

function zoomInProvice(top, fg, bg, targetProv) {
  if (top) {
    top.hide(600)
  }

  var loca = window.loca = new Loca.Container({
      map,
    });

  let center = map.getCenter()

  loca.viewControl.addAnimates(
    [{
        center: {
          value: [targetProv.x, targetProv.y],
          control: [[center.lng - 0.005, center.lat - 0.005], 
                    [targetProv.x + 0.001, targetProv.y + 0.001]],
          timing: [0.4, 0, 0.6, 1],   // 贝塞尔曲线参数，控制时间的流速
          duration: 800,
        },
        zoom: {
          value: 6.3,
          control: [0.4, 3.5, 0.6, 7.5],
          timing: [0.4, 0, 0.6, 1],
          duration: 800,
        }
      }], 
    function () {
      if (fg) {
        fg.show(1000);
      }
      if (bg) {
        bg.hide(1000)
      } 
      if (top) {
          setTimeout(() => top.show(800), 100);
        }
    });

  loca.animate.start();
}




</script>

<template>
  <div id="mapContainer"></div>
</template>


<style scoped>

#map {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

#container {
  padding:0px;
  margin: 0px;
  width: 100%;
  height: 90%;
}

</style>