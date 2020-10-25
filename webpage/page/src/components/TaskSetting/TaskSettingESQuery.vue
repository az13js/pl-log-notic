<!-- 任务ES查询条件设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="12">
        <v-text-field v-model="queryString" :disabled="isLoading" label="查询语句（可以不填）" counter="500" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-text-field v-model="queryType" :disabled="isLoading" label="Index Pattern 设置" counter="500" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn :disabled="isLoading" color="secondary" @click="testQuery()" block>测试查询</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-textarea v-model="queryResult" label="测试查询结果" readonly></v-textarea>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn :disabled="isLoading" color="primary" @click="save()" block>保存此监控任务所有的改动</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Component from "vue-class-component";
  import TaskSettingBase from "./TaskSettingBase.ts";
  import axios, {AxiosResponse, AxiosError} from "axios";
  import "../../defined.ts";

  @Component
  export default class TaskSettingESQuery extends TaskSettingBase {
    set queryType(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.query_type = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get queryType(): string {
      return this.$store.state.taskSettingInfo.query_type;
    }
    set queryString(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.query_string = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get queryString(): string {
      return this.$store.state.taskSettingInfo.query_string;
    }

    set queryResult(v: string) {
      this.$store.commit("setEsQueryResult", {esQueryResult: v});
    }
    get queryResult(): string {
      return this.$store.state.esQueryResult;
    }

    /**
     * 测试ES连接
     *
     * @returns {void}
     */
    public testQuery(): void {
      this.$store.commit("loadStatus", {isLoading: true});
      this.queryResult = "";
      let data: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      for (let key in data) {
        if (data[key] === null) {
          data[key] = "";
        }
      }
      axios.post(window.env.apiHost + "/pl/task-test-es-query", {
        params: data
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          this.queryResult = response.data.data.esQueryResult;
        } else {
          this.$store.commit("showDialog", {message: response.data.message, title: "失败"});
        }
      }).catch((error: AxiosError): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        this.$store.commit("showDialog", {message: error.message, title: "请求错误"});
      });
    }
  }
</script>
