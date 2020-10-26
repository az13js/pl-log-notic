<!-- 任务ES地址设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="3">
        <v-text-field :disabled="isLoading" v-model="esHost" label="ES 服务器主机名（如www.example.com）" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-text-field :disabled="isLoading" v-model="esAddress" label="IP地址（可不填）" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-text-field :disabled="isLoading" v-model="esAddress" label="IP地址（可不填）" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-text-field :disabled="isLoading" v-model="esPort" label="端口号，可不填" counter="6" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <v-text-field :disabled="isLoading" v-model="urlPrefix" label="ES访问前缀" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="4">
        <v-select :disabled="isLoading" v-model="sechma" label="ES 访问协议" :items="sechmaList"></v-select>
      </v-col>
      <v-col cols="4">
        <v-select :disabled="isLoading" v-model="compressSetting" label="压缩" :items="compressList"></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field :disabled="isLoading" v-model="authUser" label="ES 用户名（如果没有登录认证可不填）" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field :disabled="isLoading" v-model="authPwd" label="ES 密码（如果没有登录认证可不填）" counter="100" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field :disabled="isLoading" v-model="esTestResult" label="测试结果" readonly clearable></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-btn color="secondary" :disabled="isLoading" @click="testLinkES()" block>测试连接 ES 服务器</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" :disabled="isLoading" @click="save()" block>保存此监控任务所有的改动</v-btn>
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
  export default class TaskSettingESAddress extends TaskSettingBase {
    set esHost(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.es_host = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get esHost(): string {
      return this.$store.state.taskSettingInfo.es_host;
    }
    set esAddress(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.es_ip = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get esPort(): string {
      return this.$store.state.taskSettingInfo.es_port;
    }
    set esPort(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.es_port = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get urlPrefix(): string {
      return this.$store.state.taskSettingInfo.url_prefix;
    }
    set urlPrefix(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.url_prefix = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get kbnVersion(): string {
      return this.$store.state.taskSettingInfo.kbn_version;
    }
    set kbnVersion(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.kbn_version = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get esAddress(): string {
      return this.$store.state.taskSettingInfo.es_ip;
    }
    set sechma(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.es_sechma = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get sechma(): string {
      return this.$store.state.taskSettingInfo.es_sechma;
    }
    set compressSetting(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.compress = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get compressSetting(): string {
      return "" + this.$store.state.taskSettingInfo.compress;
    }
    set authUser(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.auth_user = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get authUser(): string {
      return this.$store.state.taskSettingInfo.auth_user;
    }
    set authPwd(v: string) {
      let src: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      src.auth_pwd = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get authPwd(): string {
      return this.$store.state.taskSettingInfo.auth_pwd;
    }
    set esTestResult(v: string) {
      this.$store.commit("setEsTestResult", {esTestResult: v});
    }
    get esTestResult(): string {
      return this.$store.state.esTestResult;
    }

    public sechmaList: any = [
      {text:"http",value:"http"},
      {text:"https",value:"https"}
    ]

    public compressList: any = [
      {text:"开启",value:"1"},
      {text:"关闭",value:"0"}
    ]

    /**
     * 测试ES连接
     *
     * @returns {void}
     */
    public testLinkES(): void {
      this.$store.commit("loadStatus", {isLoading: true});
      this.esTestResult = "";
      let data: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
      for (let key in data) {
        if (data[key] === null) {
          data[key] = "";
        }
      }
      axios.post(window.env.apiHost + "/pl/task-test-es-link", {
        params: data
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          this.esTestResult = JSON.stringify(response.data.data.esTestResult);
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
