<!-- 企业微信机器人设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="12">
        <v-text-field v-model="botAddress" label="企业微信机器人地址" counter="1024" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="secondary" block>推送测试</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-textarea label="企业微信服务器返回值" readonly clearable></v-textarea>
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
  export default class TaskSettingBot extends TaskSettingBase {
    set botAddress(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.wx_bot_addr = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get botAddress(): string {
      return this.$store.state.taskSettingInfo.wx_bot_addr;
    }
  }
</script>
