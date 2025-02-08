<script setup>

import { watch, onMounted } from 'vue';

const emit = defineEmits(['uiReady', 'retTop', 'changeProvince', 'changeMetropolis'])

// const region = defineProps('region')

const props = defineProps({
  region: {}, 
  title: String, 
  l1: Array,
  l2: Array,
  l3: Array
})

const { region, title, l1, l2 } = props


onMounted(() => {
  emit('uiReady', 'navibar')
})


</script>

<template>
  <div class="Titile">
    <h1>{{ title }}</h1>
  </div>
  <div>
    <h3>{{ `${region.province} ${region.metropolis}` }}</h3>
  </div>
  <div class="wrapper">
    <div class="wrapper">
      <v-select label="- 选择省 -"
        v-model="region.province"
        :items="l1"
        @update:modelValue="emit('changeProvince', $event)"
        >
      </v-select>
      <v-select label="- 选择市 -"
        v-model="region.metropolis"
        :items="l2"
        @update:modelValue="emit('changeMetropolis', $event)"
        >
      </v-select>
    </div>

    <div class="input-card" style="width: auto;">
      <div class="input-item">
        <button id="top-layer-btn" @click="$emit('retTop')" class="btn">回顶层</button>
        <button id="upper-layer-btn" class="btn">回上层</button>
      </div>
    </div>

    <nav>
      <RouterLink to="/">地图</RouterLink>
      <RouterLink to="/data">数据</RouterLink>
    </nav>

  </div>

</template>

<style scoped>
/* div .Titile {
  display: flex;
    flex-direction: column;
    justify-content: center;
    place-items: center;
} */

div .Tools {
  display: flex;
    flex-direction: row;
    justify-content: center;
    place-items: center;
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}


nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  /* margin-top: 2rem; */
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
  

  nav {
    text-align: left;
    /* margin-left: -1rem; */
    font-size: 1rem;

    /* padding: 1rem 0; */
    /* margin-top: 1rem; */
  }


  .wrapper {
    display: flex;
    flex-direction: row;
    /* flex-wrap: wrap; */
    justify-content: center;
    /* place-items: flex-start; */
    place-items: center;
    width: 100%;
  }

  .btn {
    display: inline-block;
    font-weight: 400;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    user-select: none;
    border: 1px solid transparent;
    transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
    background-color: transparent;
    background-image: none;
    color: #25A5F7;
    border-color: #25A5F7;
    padding: .25rem .5rem;
    line-height: 1.5;
    border-radius: 1rem;
    -webkit-appearance: button;
    cursor: pointer;
  }

  .btn:hover {
    color: #fff;
    background-color: #25A5F7;
    border-color: #25A5F7;
    text-decoration: none;
  }

  .input-item {
    position: relative;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
  }

  .input-item:last-child {
    margin-bottom: 0;
  }

  .input-item>select, .input-item>input[type=text], .input-item>input[type=date] {
    position: relative;
    -ms-flex: 1 1 auto;
    flex: 1 1 auto;
    width: 1%;
    margin-bottom: 0;
  }

  .input-item>select:not(:last-child), .input-item>input[type=text]:not(:last-child), .input-item>input[type=date]:not(:last-child) {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0
  }

  .input-item>select:not(:first-child), .input-item>input[type=text]:not(:first-child), .input-item>input[type=date]:not(:first-child) {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0
  }

  .input-item-prepend {
    margin-right: -1px;
  }

  .input-item-text, input[type=text],input[type=date], select {
    height: calc(2.2rem + 2px);
  }

  .input-item-text {
    width: 6rem;
    text-align: justify;
    padding: 0.4rem 0.7rem;
    display: inline-block;
    text-justify: distribute-all-lines;
    /*ie6-8*/
    text-align-last: justify;
    /* ie9*/
    -moz-text-align-last: justify;
    /*ff*/
    -webkit-text-align-last: justify;
    /*chrome 20+*/
    -ms-flex-align: center;
    align-items: center;
    margin-bottom: 0;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #495057;
    text-align: center;
    white-space: nowrap;
    background-color: #e9ecef;
    border: 1px solid #ced4da;
    border-radius: .25rem;
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;
  }

  .input-item-text input[type=checkbox], .input-item-text input[type=radio] {
    margin-top: 0
  }

  .input-card {
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border-radius: .25rem;
    width: 22rem;
    border-width: 0;
    border-radius: 0.4rem;
    box-shadow: 0 2px 6px 0 rgba(114, 124, 245, .5);
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    -ms-flex: 1 1 auto;
    flex: 1 1 auto;
    padding: 0.75rem 1.25rem;
  }


}
</style>
