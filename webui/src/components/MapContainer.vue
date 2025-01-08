<script setup>

// const openReadmeInEditor = () => fetch('/__open-in-editor?file=README.md')

import { onMounted, onUnmounted } from "vue";
import AMapLoader from '@amap/amap-jsapi-loader';

onMounted(() => {
  console.log(" === 开始加载地图 ===")

  window._AMapSecurityConfig = {securityJsCode: "[YOUR CODE]",};

  AMapLoader.load({
    key: "[YOUR KEY]",
    version: "2.0",
    plugins: ["AMap.Scale", ], 
    AMapUI: {
        version: '1.1',
        plugins: [],
    },
    Loca: {
        version: '2.0'
    }
  })
    .then((AMap) => {
      // map = new AMap.Map("container", {
      //   viewMode: "3D",
      //   zoom: 11,
      //   center: [116.397428, 39.90923], 
      //   rotateEnable: false,
      //   mapStyle: 'amap://styles/45311ae996a8bea0da10ad5151f72979'
      // });

      init_map()
    })
    .catch((e) => {
      console.log(e);
    });
});

onUnmounted(() => {
  map?.destroy();
});

function init_map (params) {
  // window.movingDraw = true;
  var map = new AMap.Map('map', {
    zoom: 5,
    showLabel: false,
    viewMode: '3D',
    pitch: 55,
    center: [103.594884, 36.964587],
    mapStyle: 'amap://styles/45311ae996a8bea0da10ad5151f72979'
  });

  var loca = new Loca.Container({
    map,
  });

  loca.ambLight = {
    intensity: 0.7,
    color: '#7b7bff',
  };
  loca.dirLight = {
    intensity: 0.8,
    color: '#fff',
    target: [0, 0, 0],
    position: [0, -1, 1],
  };
  loca.pointLight = {
    color: 'rgb(240,88,25)',
    position: [112.028276, 31.58538, 2000000],
    intensity: 3,
    // 距离表示从光源到光照强度为 0 的位置，0 就是光不会消失。
    distance: 5000000,
  };

  var pl = new Loca.PrismLayer({
    zIndex: 10,
    opacity: 1,
    visible: false,
    hasSide: true,
  });

  var geo = new Loca.GeoJSONSource({
    url: 'https://a.amap.com/Loca/static/loca-v2/demos/mock_data/gdp.json',
  });
  pl.setSource(geo);
  // top3 的城市增加文字
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
      pl.addAnimate({
        key: 'rotation',
        value: [0, 1],
        duration: 500,
        easing: 'Linear',
        transform: 2000,
        random: true,
        delay: 8000,
      });
    }, 800);
  });
  loca.animate.start();

  var dat = new Loca.Dat();
  dat.addLayer(pl, 'GDP');

  dat.addLight(loca.ambLight, loca, '环境光');
  dat.addLight(loca.dirLight, loca, '平行光');
  dat.addLight(loca.pointLight, loca, '点光');

  // 事件处理
  var clickInfo = new AMap.Marker({
    anchor: 'bottom-center',
    position: [116.396923, 39.918203, 0],
  });
  clickInfo.setMap(map);
  clickInfo.hide();
  // 鼠标事件
  map.on('mousemove', function (e) {
    var feat = pl.queryFeature(e.pixel.toArray());
    if (feat) {
      clickInfo.show();
      var props = feat.properties;
      var height = Math.max(100, Math.sqrt(props['GDP']) * 9000 - 50000);
      clickInfo.setPosition([feat.coordinates[0], feat.coordinates[1], height]);
      clickInfo.setContent(
        '<div style="text-align: center; height: 20px; width: 150px; color:#fff; font-size: 14px;">' +
        feat.properties['名称'] + ': ' + feat.properties['GDP'] +
        ' 元</div>'
      );
    } else {
      clickInfo.hide();
    }
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