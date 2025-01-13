<script setup>


import { ref, onMounted } from 'vue';
// import { wx } from "https://res.wx.qq.com/open/js/jweixin-1.2.0.js"
import ky from 'ky'

var url;

onMounted(async () => {
  url = window.location.href

  // let params = new URLSearchParams({
  //     beta: true,
  //     debug: true,
  //     appId: '',
  //     key: 'e28e8e04218b803aceeffed7d28fd9c9', 
  //     subdistrict: 1})

  // if (region) {
  //   params.append('keywords', region)
  // }

  const auth_params = await ky.post('https://web.cdyhamc.com/endpoints/publicdebt/corpwechat', 
    {json: {url: url.split('#')[0]}}).json();

  return info.districts
});



</script>


<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
