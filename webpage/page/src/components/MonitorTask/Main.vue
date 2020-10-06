<!-- 监控列表页面 -->
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <!-- 交汇处不需要 panding 和 margin -->
        <monitor-task-searcher class="pb-0 mb-0"></monitor-task-searcher>
        <monitor-task-pagination class="pt-0 mt-0 pb-0 mb-0"></monitor-task-pagination>
        <div style="white-space:nowrap"><!-- 表格页面自动换行太丑了，禁用 -->
          <monitor-task-table class="pt-0 mt-0"></monitor-task-table>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import Searcher from "./Searcher.vue";
  import Pagination from "./Pagination.vue";
  import Table from "./Table.vue";

  @Component({
    components: {
       MonitorTaskSearcher: Searcher,
       MonitorTaskPagination: Pagination,
       MonitorTaskTable: Table
    }
  })
  export default class Main extends Vue {
  }
</script>
