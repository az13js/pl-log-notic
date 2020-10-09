<!-- 查询和推送频率设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="4">
        <v-text-field label="每隔多少秒查询一次 ES 服务器" counter="10" placeholder="最小值是1，不能小于1" clearable></v-text-field>
      </v-col>
      <v-col cols="4">
        <v-text-field label="查询到多少条结果就触发推送" counter="10" placeholder="最小值是0，不能小于0" clearable></v-text-field>
      </v-col>
      <v-col cols="4">
        <v-text-field label="每小时最多推送多少条" counter="10" placeholder="可以是小数但必须大于0" clearable></v-text-field>
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
  export default class TaskSettingFrequency extends TaskSettingBase {
  }
</script>
