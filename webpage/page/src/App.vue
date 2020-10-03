<template>
  <v-app id="vuetifyapp">
    <com-navigation></com-navigation>
    <v-main>
      <transition name="bounce" mode="out-in">
        <router-view></router-view>
      </transition>
    </v-main>
  </v-app>
</template>

<script lang="ts">
  import Vue from "vue";
  import Navigation from "./components/Navigation.vue"; // 导航栏

  // https://class-component.vuejs.org/guide/property-type-declaration.html
  export default Vue.extend({
    components: {
      ComNavigation: Navigation
    }
  });
</script>

<style lang="sass">
html, body
  font-family: "Arial","文泉驿正黒","微软雅黑","宋体"
</style>

<style>
.bounce-enter-active {
  animation: bounce-in .1s;
}
.bounce-leave-active {
  animation: bounce-in .1s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
