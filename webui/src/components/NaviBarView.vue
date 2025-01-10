<script setup>

import { ref } from 'vue';



defineProps({
  title: {
    type: String,
    required: true,
  },
  des: {
    type: String,
    required: true,
  },
})

var onProvinceChange = function (event) {
    console.log(event.target.value)
}

var onCityChange =  function (event) {
  console.log(event.target.value)
}

const province = ref('');
const city = ref('');

var provinces = ref(['1', '2', '3'])
var cities = ref(['A', 'B', 'C'])


</script>

<template>
  <div class="Titile">
    <h1>{{ title }}</h1>
  </div>

  <div class="wrapper">
    <h3>{{ des }}</h3>

    <div class="wrapper">
      <v-select label="- 选择省 -"
        :items="provinces"
        @input="onProvinceChange"
        >
      </v-select>
      <v-select label="- 选择市 -"
        :items="cities"
        @input="onCityChange"
        >
      </v-select>
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

}
</style>
