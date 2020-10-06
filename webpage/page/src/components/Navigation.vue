<!-- 导航栏 -->
<template>
  <v-navigation-drawer app class="navigation-common-style" width="170px" mobile-breakpoint="400">
    <v-list dense nav class="py-0">
      <v-list-item>
        <v-list-item-content>
          <h1 class="title">
            <span>pl-log-notic</span>
          </h1>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item v-for="item in items" :key="item.title" link nav>
        <v-list-item-content>
          <v-list-item-title>
            <router-link v-bind:to="item.path">
              <h2 class="body-2 navigation-list-style">{{ item.title }}</h2>
            </router-link>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";

  @Component
  export default class Navigation extends Vue {
    data(): Object {
      let list = {
        items: [
          {title: "监控任务", path:"/"},
          {title: "任务设置", path:"/TaskSetting"}
        ]
      };
      return list;
    }
  }
</script>

<style lang="sass">
.navigation-common-style
  -moz-user-select: "-moz-none"
  -webkit-user-select: none
  -ms-user-select: none
  -khtml-user-select: none
  user-select: none
.navigation-list-style, a, a:hover
  text-decoration: none
  color: white
</style>
