<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-pagination v-on:input="clickPageNumber" class="pagination-common-style" prev-icon="mdi-menu-left" next-icon="mdi-menu-right" v-model="page" length="100" :disabled="isDisable"></v-pagination>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import axios, {AxiosResponse} from "axios";
  import "../../defined.ts";

  @Component
  export default class Pagination extends Vue {
    get isDisable() {
      return this.$store.state.isLoading;
    }
    set isDisable(val: boolean) {
      this.$store.commit("loadStatus", {isLoading: val});
    }
    get page() {
      return this.$store.state.queryColumns.page;
    }
    set page(val: number) {
      this.$store.commit("setPage", {page: val});
    }
    clickPageNumber(num: number) {
      let host: string = window.env.apiHost;
      this.$store.commit("loadStatus", {isLoading: true});
      axios.get(host + "/monitor-task", {
        params: this.$store.state.queryColumns
      }).then((response: AxiosResponse): void => {
        this.$store.commit("updateDesserts", {desserts: response.data.list});
        this.$store.commit("loadStatus", {isLoading: false});
      });
    }
  }
</script>

<style lang="sass">
.pagination-common-style
  -moz-user-select: "-moz-none"
  -webkit-user-select: none
  -ms-user-select: none
  -khtml-user-select: none
  user-select: none
</style>