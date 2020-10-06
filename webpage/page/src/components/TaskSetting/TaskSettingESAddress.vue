<!-- 任务ES地址设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row>
      <v-col cols="6">
        <v-text-field label="ES 服务器主机名（如www.example.com）" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field label="IP地址（可不填）" counter="100" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select v-model="sechma" label="ES 访问协议" :items="sechmaList"></v-select>
      </v-col>
      <v-col cols="6">
        <v-select v-model="compress" label="压缩" :items="compressList"></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field label="ES 用户名（如果没有登录认证可不填）" counter="100" clearable></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-text-field label="ES 密码（如果没有登录认证可不填）" counter="100" clearable></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field label="测试结果" readonly clearable></v-text-field>
      </v-col>
      <v-col cols="6">
        <v-btn color="secondary" block>测试连接 ES 服务器</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" block>保存此监控任务所有的改动</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";

  @Component
  export default class TaskSettingESAddress extends Vue {
    sechma: string = "http"
    sechmaList: any = [
      {text:"http",value:"http"},
      {text:"https",value:"https"}
    ]
    compress: string = "No"
    compressList: any = [
      {text:"开启",value:"Yes"},
      {text:"关闭",value:"No"}
    ]
  }
</script>
