<script setup>

import MapContainer from '@/components/MapContainer.vue';

const emit = defineEmits(['mapReady']);

function onMapReady() {
  // 继续向外层抛出
  emit('map-ready', 'amap')
}

</script>

<template>
  <MapContainer @map-ready="onMapReady" />
</template>

<style scoped>
h1 {
  margin: 0;
  color: #ACB3BB;
}

h3 {
  font-weight: normal;
  /* margin-top: 5px; */
  color: #8E939D;
}
</style>

