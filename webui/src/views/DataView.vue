<script setup>


import { ref, onMounted } from 'vue';
import wx from 'weixin-js-sdk'
import ky from 'ky'

var url;

onMounted(async () => {
  url = window.location.href

  console.log(` Registrying wechat api. url is: ${url};  signature url: ${url.split('#')[0]}`)

  const auth_params = await ky.post('https://web.cdyhamc.com/endpoints/publicdebt/corpwechat', 
    {
      json: {
        url: url.split('#')[0]
      }
    }).json();

  console.log(auth_params)

  wx.config({
    beta: true,
    debug: true,
    appId: '1000017',
    timestamp: auth_params.timestamp,
    nonceStr: auth_params.nonce,
    signature: auth_params.signature,
    jsApiList: ['previewFile']
  });

  wx.ready(function (){
    console.log('wx.config 验证成功')
  });
  

  wx.error(function (res){
    console.log('wx.config 验证失败，结果 ${res}')
  });
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
