<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NaviBarView from './components/NaviBarView.vue'


</script>

<template>
  <header>
    <NaviBarView title="地方公共债务" des="省级行政区"></NaviBarView>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  background: lightsteelblue;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    flex-direction: column;
    justify-content: center;
    place-items: center;
    /* padding-right: calc(var(--section-gap) / 2); */
  }

  .logo {
    margin: 0 2rem 0 0;
  }
}
</style>
