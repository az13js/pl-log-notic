<!-- 任务ES查询条件设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="12">
        <v-text-field label="查询语句（可以不填）" counter="500" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-select v-model="queryType" label="查询类型" :items="queryTypeList"></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="secondary" block>测试查询</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-textarea label="测试查询结果" readonly clearable></v-textarea>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" @click="save()" block>保存此监控任务所有的改动</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import TaskSettingBase from "./TaskSettingBase.ts";

  @Component
  export default class TaskSettingESQuery extends TaskSettingBase {
    queryType: string = "http"
    queryTypeList: any = [
      {text:"error",value:"error"},
      {text:"info",value:"info"},
      {text:"warning",value:"warning"}
    ]
    queryString: string = ""
  }
</script>
