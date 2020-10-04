<!-- 表格，任务列表 -->
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-data-table item-key="id" :loading="isLoading" loading-text="正在加载数据……" mobile-breakpoint="400" :headers="headers" :items="desserts" calculate-widths disable-pagination disable-sort hide-default-footer>
          <template v-slot:item.actions="{ item }">
            <v-icon @click="locationTaskSetting(item)">mdi-open-in-new</v-icon>
          </template>
        </v-data-table>
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
  export default class Table extends Vue {
    headers: object[] = [
      {text: '配置', value: 'actions'},
      {text: "任务名称", value: "name"}
    ]
    get isLoading() {
      return this.$store.state.isLoading;
    }
    set isLoading(value: boolean) {
      this.$store.commit("loadStatus", {isLoading: value});
    }
    // 数据表中的数据
    get desserts() {
      return this.$store.state.desserts;
    }
    // 设置数据表中的数据
    set desserts(value: any) {
      this.$store.commit("updateDesserts", {desserts: value});
    }

    /**
     * 加载后执行，load首页数据
     *
     * @return void
     */
    mounted(): void {
      let host: string = window.env.apiHost;
      this.$store.commit("loadStatus", {isLoading: true});
      axios.get(host + "/monitor-task", {
        params: this.$store.state.queryColumns
      }).then((response: AxiosResponse): void => {
        this.$store.commit("updateDesserts", {desserts: response.data.list});
        this.$store.commit("loadStatus", {isLoading: false});
      });
    }

    /**
     * 点击按钮到配置监控任务的页面
     *
     * @param item any
     * @return void
     */
    locationTaskSetting(item: any): void {
      this.$router.push({
        name: "TaskSetting",
        params: {
          id: item.id
        }
      });
    }
  }
</script>
