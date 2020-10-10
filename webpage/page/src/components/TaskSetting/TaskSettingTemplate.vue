<!-- 企业微信文本模板设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="12">
        <v-textarea v-model="template" label="消息文本模板" counter="1024" clearable></v-textarea>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="secondary" @click="testSendTemplate()" block>推送测试</v-btn>
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
  import axios, {AxiosResponse, AxiosError} from "axios";
  import "../../defined.ts";

  @Component
  export default class TaskSettingTemplate extends TaskSettingBase {
    set template(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.template = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get template(): string {
      return this.$store.state.taskSettingInfo.template;
    }

    /**
     * 测试发送模板
     *
     * @returns {void}
     */
    public testSendTemplate(): void {
      this.$store.commit("loadStatus", {isLoading: true});
      let data: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      for (let key in data) {
        if (data[key] === null) {
          data[key] = "";
        }
      }
      axios.post(window.env.apiHost + "/pl/task-test-send-template", {
        params: data
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          this.$store.commit("showDialog", {message: JSON.stringify(response.data.data.sendResult), title: "请求结束"});
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
