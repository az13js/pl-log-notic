<!-- 企业微信机器人设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="12">
        <v-text-field :disabled="isLoading" v-model="botAddress" label="企业微信机器人地址" counter="1024" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn :disabled="isLoading" color="secondary" @click="testLinkWX()" block>推送测试</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-textarea v-model="wxTestResult" abel="企业微信服务器返回值" readonly clearable></v-textarea>
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
  export default class TaskSettingBot extends TaskSettingBase {
    set botAddress(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.wx_bot_addr = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get botAddress(): string {
      return this.$store.state.taskSettingInfo.wx_bot_addr;
    }

    /** @type {string} */
    public wxTestResult: string = ""

    /**
     * 测试企业微信连接
     *
     * @returns {void}
     */
    public testLinkWX(): void {
      this.$store.commit("loadStatus", {isLoading: true});
      this.wxTestResult = "";
      let data: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      for (let key in data) {
        if (data[key] === null) {
          data[key] = "";
        }
      }
      axios.post(window.env.apiHost + "/pl/task-test-wxbot-address", {
        params: data
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          this.wxTestResult = JSON.stringify(response.data.data.wxTestResult);
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
