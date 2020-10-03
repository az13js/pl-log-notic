<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-text-field :disabled="isLoading" v-model="taskName" label="任务名称" counter="64" clearable ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import axios, {AxiosResponse} from "axios";

  @Component
  export default class Searcher extends Vue {
    set taskName(v: string) {
      let columns: any = JSON.parse(JSON.stringify(this.$store.state.queryColumns));
      columns.taskName = v;
      this.$store.commit("setQueryColumns", {queryColumns: columns});
    }
    get taskName() {
      if (this.$store.state.queryColumns.taskName) {
        return this.$store.state.queryColumns.taskName;
      }
      return "";
    }
    get isLoading() {
      return this.$store.state.isLoading;
    }
    set isLoading(value: boolean) {
      this.$store.commit("loadStatus", {isLoading: value});
    }
  }
</script>
