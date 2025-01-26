<script setup>

// const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')

import { watch, onMounted, onUnmounted } from "vue";
import { storeToRefs } from 'pinia'

import { useGeoJsonStore } from '@/stores/GeoJson'

import AMapLoader from '@amap/amap-jsapi-loader';


const cached = useGeoJsonStore()
const { geojson } = storeToRefs(cached)

const emit = defineEmits(['change_province', 'change_metropolis'])

var loca = undefined;
var provinceLayer = undefined;

watch(geojson, () => {
  console.log(getjson)
})

onMounted(() => {
  window._AMapSecurityConfig = {securityJsCode: "cf5dba8895ae3f072aa48bc8be4c0db3",};


  AMapLoader.load({
    key: "33300d9b8a904f22b218486056876efa",
    version: "2.0",
    plugins: ["AMap.Scale", ], 
    // AMapUI: {
    //     version: '1.1',
    //     plugins: [],
    // },
    Loca: {
        version: '2.0'
    }
  })
    .then((AMap) => {
      initAMap(AMap)
    })
    .catch((e) => {
      console.log(e);
    });
});

onUnmounted(() => {
  map.destroy();
});


function createPrismLayer(map) {
  loca = new Loca.Container({
    map,
  });

  var geo = new Loca.GeoJSONSource({
    url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/gdp.json',
  });

  loca.ambLight = {
    intensity: 0.7,
    color: '#7b7bff',
    // color: 'lightsteelblue',
  };

  loca.dirLight = {
    intensity: 0.8,
    color: '#fff',
    // color: 'lightsteelblue',
    target: [0, 0, 0],
    position: [0, -1, 1],
  };

  loca.pointLight = {
    color: 'rgb(240,88,25)',
    position: [112.028276, 31.58538, 2000000],
    intensity: 3,
    distance: 5000000,
  };

  var pl = new Loca.PrismLayer({
    zIndex: 10,
    opacity: 0.8,
    visible: false,
    hasSide: true,
  });

  pl.setSource(geo);

  pl.setStyle({
    unit: 'meter',
    sideNumber: 4,
    topColor: (index, f) => {
      var n = f.properties['GDP'];
      return n > 7000 ? '#E97091' : '#2852F1';
    },
    sideTopColor: (index, f) => {
      var n = f.properties['GDP'];
      return n > 7000 ? '#E97091' : '#2852F1';
    },
    sideBottomColor: '#002bb9',
    radius: 15000,
    height: (index, f) => {
      var props = f.properties;
      var height = Math.max(100, Math.sqrt(props['GDP']) * 9000 - 50000);
      return height;
    },
    rotation: 360,
    altitude: 0,
  });
  loca.add(pl)

  return pl;
}



function initAMap(AMap) {

  window.movingDraw = true;
  var colors = {};
  var getColorByAdcode = function (adcode) {
    if (!colors[adcode]) {
      var gb = Math.random() * 155 + 50;
      colors[adcode] = 'rgb(' + gb + ',' + gb + ',255)';
    }

    return colors[adcode];
  };

  var countryLayer = new AMap.DistrictLayer.Country({
      zIndex: 2,
      opacity: 0.6, 
      SOC: 'CHN',
      depth: 2,
      styles: {
        'nation-stroke': '#f09',
        'coastline-stroke': [0.85, 0.63, 0.94, 1],
        'province-stroke': 'white',
        // 'city-stroke': 'rgba(255,255,255,0.15)',//中国特有字段
        'fill': function (props) {//中国特有字段
          return getColorByAdcode(props.adcode_pro)
        }
      }
    })

  var map = new AMap.Map('map', {
    zoom: 5,
    showLabel: false,
    viewMode: '3D',
    visible: false,
    pitch: 45,
    // center: [103.594884, 36.964587],
    center: [108.940174, 34.341568],
    rotateEnable: false,
    layers: [
      // disProvince,
      countryLayer,
    ],
    mapStyle: 'amap://styles/dark'
  });

  var pl = createPrismLayer(map);

  map.on('complete', function () {
    setTimeout(function () {
      pl.show(500);

      pl.addAnimate({
        key: 'height',
        value: [0, 1],
        duration: 500,
        easing: 'Linear',
        transform: 2000,
        random: true,
        delay: 8000,
      });
    }, 
    800);
  });

  map.on('mousemove', function (e) {
    var feat = pl.queryFeature(e.pixel.toArray());
    if (feat) {
      // clickInfo.show();
    } else {
      // clickInfo.hide();
    }
  });

  map.on('click', function (ev) {
      var px = ev.pixel;

      var props = countryLayer.getDistrictByContainerPos(px);
      if (props) {
        if (typeof props.province !== 'undefined' && props.province) {
          props.province = undefined;
        } else {
          provinceLayer = putProvinceLayerOntop(map, props)
          zoomInProvice(pl, provinceLayer, countryLayer, props)
          province.value = props
        }
      }


      // if (props) {
      // var SOC = props.SOC;
      // if(SOC){
      //     // 重置行政区样式
      //     disWorld.setStyles({
      //         // 国境线
      //         //nation-stroke': nationStroke,
      //         // 海岸线
      //         //'coastline-stroke': '',
      //         'fill': function (props) {
      //             return props.SOC == SOC ? nationFill : 'white';
      //         }
      //     });
      //     updateInfo(props);
      // }
  });


  // loca.animate.start();
}


function putProvinceLayerOntop(map, targetProv) {

  var fg = new AMap.DistrictLayer.Province({
    zIndex: 6,
    opacity: 0.6,
    adcode: targetProv.adcode_pro,
    depth: 1,
    styles: {
      'fill': function (properties) {
        var adcode = properties.adcode;
        return getColorByAdcode(adcode);
      },
      'province-stroke': 'cornflowerblue',
      'city-stroke': 'white', // 中国地级市边界
      'county-stroke': 'rgba(255,255,255,0.5)' // 中国区县边界
    }
  });

  fg.setMap(map);

  return fg
}

function zoomInProvice(top, bg, fg, targetProv) {
  top.hide(600)
  bg.hide(1200)
  loca.viewControl.addAnimates(
    [{
        center: {
          value: [targetProv.x, targetProv.y],
          // control: [[121.424503326416, 1.199146851153124], 
          //           [121.46656036376952, 31.245828642661486]],
          timing: [0.3, 0, 0.1, 1],
          duration: 800,
        },
        zoom: {
          value: 9,
          control: [[0.3, 5], [1, 9]],
          timing: [0.3, 0, 0.7, 1],
          duration: 800,
        }
      }], 
    function () {
        fg.show(1000);

        setTimeout((top) => top.show(800), 100);
        console.log('结束');
    });

}


</script>

<template>
  <div id="map"></div>
  <div id="container"></div>
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