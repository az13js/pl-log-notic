<!-- 导出页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row><!--- 开始时间和结束时间 -->
      <v-col cols="12">
        <v-list>
          <v-list-group>
            <template v-slot:activator>
              <v-list-item-title>设置导出规则</v-list-item-title>
            </template>
            <v-list-item-content>
              <v-container class="pt-0 mt-0 pb-0 mb-0">
                <v-row><!--- 开始时间和结束时间 -->
                  <v-col cols="3">
                    <v-menu v-model="startPicker" :close-on-content-click="false" :elevation="0" transition="scale-transition" offset-y>
                      <template v-slot:activator="{ on }">
                        <v-text-field :disabled="isLoading" v-model="startDate" label="开始日期" clearable v-on="on"></v-text-field>
                      </template>
                      <v-date-picker locale="zh-cn" v-model="startDate" @input="startPicker = false"></v-date-picker>
                    </v-menu>
                  </v-col>
                  <v-col cols="3">
                    <v-menu v-model="startTimePicker" :close-on-content-click="false" :elevation="0" transition="scale-transition" offset-y>
                      <template v-slot:activator="{ on }">
                        <v-text-field :disabled="isLoading" v-model="startTime" label="开始时间" clearable v-on="on"></v-text-field>
                      </template>
                      <v-time-picker format="24hr" @input="startTimePicker = false" v-model="startTime" scrollable use-seconds></v-time-picker>
                    </v-menu>
                  </v-col>
                  <v-col cols="3">
                    <v-menu v-model="endPicker" :close-on-content-click="false" :elevation="0" transition="scale-transition" offset-y>
                      <template v-slot:activator="{ on }">
                        <v-text-field :disabled="isLoading" v-model="endDate" label="结束日期" clearable v-on="on"></v-text-field>
                      </template>
                      <v-date-picker locale="zh-cn" v-model="endDate" @input="endPicker = false"></v-date-picker>
                    </v-menu>
                  </v-col>
                  <v-col cols="3">
                    <v-menu v-model="endTimePicker" :close-on-content-click="false" :elevation="0" transition="scale-transition" offset-y>
                      <template v-slot:activator="{ on }">
                        <v-text-field :disabled="isLoading" v-model="endTime" label="结束时间" clearable v-on="on"></v-text-field>
                      </template>
                      <v-time-picker format="24hr" @input="endTimePicker = false" v-model="endTime" scrollable use-seconds></v-time-picker>
                    </v-menu>
                  </v-col>
                </v-row>
                <v-row><!--- 文本模板 -->
                  <v-col cols="12">
                    <v-textarea :disabled="isLoading" v-model="template" label="导出文件模板" counter="1024" clearable></v-textarea>
                  </v-col>
                </v-row>
                <v-row><!--- 测试导出 -->
                  <v-col cols="12"><v-btn :disabled="isLoading" color="orange" @click="exportTest()" block>导出测试</v-btn></v-col>
                </v-row>
                <v-row>
                  <v-col cols="12">
                    <v-textarea :disabled="isLoading" v-model="testExportResult" label="测试导出结果" clearable></v-textarea>
                  </v-col>
                </v-row>
              </v-container>
            </v-list-item-content>
          </v-list-group>
        </v-list>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12"><p>当前导出任务的状态：</p></v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="do-not-select-text">
        <v-progress-linear v-model="inprocess" :value="inprocess" color="blue-grey" height="30px" bottom striped>
          <strong>{{ parseInt(inprocess * 100) / 100 }} %</strong>
        </v-progress-linear>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6"><v-btn :disabled="isLoading" @click="commitExportJob()" color="primary" block>提交导出</v-btn></v-col>
      <v-col cols="6"><v-btn :disabled="isLoading" color="red" block>终止导出</v-btn></v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Component from "vue-class-component";
  import TaskSettingBase from "./TaskSettingBase.ts";
  import axios, {AxiosResponse, AxiosError} from "axios";
  import "../../defined.ts";

  @Component
  export default class TaskSettingExport extends TaskSettingBase {
    public startPicker: boolean = false
    get startDate(): string {
      return this.$store.state.exportSetting.startDate;
    }
    set startDate(v: string) {
      this.$store.commit("setExportSetting", {
        startDate: v,
        startTime: this.startTime,
        endDate: this.endDate,
        endTime: this.endTime,
        template: this.template
      });
    }

    public startTimePicker: boolean = false
    get startTime(): string {
      return this.$store.state.exportSetting.startTime;
    }
    set startTime(v: string) {
      this.$store.commit("setExportSetting", {
        startDate: this.startDate,
        startTime: v,
        endDate: this.endDate,
        endTime: this.endTime,
        template: this.template
      });
    }

    public endPicker: boolean = false
    get endDate(): string {
      return this.$store.state.exportSetting.endDate;
    }
    set endDate(v: string) {
      this.$store.commit("setExportSetting", {
        startDate: this.startDate,
        startTime: this.startTime,
        endDate: v,
        endTime: this.endTime,
        template: this.template
      });
    }

    public endTimePicker: boolean = false
    get endTime(): string {
      return this.$store.state.exportSetting.endTime;
    }
    set endTime(v: string) {
      this.$store.commit("setExportSetting", {
        startDate: this.startDate,
        startTime: this.startTime,
        endDate: this.endDate,
        endTime: v,
        template: this.template
      });
    }

    set template(v: string) {
      this.$store.commit("setExportSetting", {
        startDate: this.startDate,
        startTime: this.startTime,
        endDate: this.endDate,
        endTime: this.endTime,
        template: v
      });
    }
    get template(): string {
      return this.$store.state.exportSetting.template;
    }

    public testExportResult: string = ""
    public inprocess: number = 0

    public exportTest(): void {
      this.isLoading = true;
      axios.post(window.env.apiHost + "/pl/task-export-test", {
        params: {
          id: this.$store.state.taskSettingInfo.id,
          setting: this.$store.state.exportSetting
        }
      }).then((response: AxiosResponse): void => {
        this.isLoading = false;
        if (0 == response.data.code) {
          // SUCCESS
          this.testExportResult = response.data.data.result;
        } else {
          this.$store.commit("showDialog", {message: response.data.message, title: "失败"});
        }
      }).catch((error: AxiosError): void => {
        this.isLoading = false;
        this.$store.commit("showDialog", {message: error.message, title: "请求错误"});
      });
    }

    public commitExportJob(): void {
      this.isLoading = true;
      axios.post(window.env.apiHost + "/pl/task-export-commit", {
        params: {
          id: this.$store.state.taskSettingInfo.id,
          setting: this.$store.state.exportSetting
        }
      }).then((response: AxiosResponse): void => {
        this.isLoading = false;
        if (0 == response.data.code) {
          this.$store.commit("showDialog", {message: response.data.message, title: "成功"});
        } else {
          this.$store.commit("showDialog", {message: response.data.message, title: "失败"});
        }
      }).catch((error: AxiosError): void => {
        this.isLoading = false;
        this.$store.commit("showDialog", {message: error.message, title: "请求错误"});
      });
    }
  }
</script>

<style lang="sass">
.do-not-select-text
  -moz-user-select: "-moz-none"
  -webkit-user-select: none
  -ms-user-select: none
  -khtml-user-select: none
  user-select: none
</style>
