<!-- 任务设置页面 -->
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-bottom-navigation :value="taskSettingIndex" color="primary" background-color="rgba(255, 255, 255, 0.04)" horizontal>
          <v-btn v-for="item in buttonList" v-bind:to="item.path" :disabled="isLoading">
            <span>{{ item.name }}</span><v-icon>{{ item.icon }}</v-icon>
          </v-btn>
        </v-bottom-navigation>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <transition name="chilbounce" mode="out-in">
          <router-view></router-view>
        </transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import axios, {AxiosResponse} from "axios";
  import "../../defined.ts";
  import Placeholder from "./TaskSettingPlaceholder/Placeholder.ts";

  @Component
  export default class Main extends Vue {
    set taskSettingIndex(idx: number) {
      this.$store.state.taskSettingIndex = idx;
      this.$store.commit("setTaskSettingIndex", idx);
    }
    get taskSettingIndex() {
      return this.$store.state.taskSettingIndex;
    }
    get isLoading() {
      return this.$store.state.isLoading;
    }
    set isLoading(value: boolean) {
      this.$store.commit("loadStatus", {isLoading: value});
    }
    buttonList: any[] = [
      {name: "ES 地址", path: "TaskSettingESAddress", icon: "mdi-dns"},
      {name: "ES 查询条件", path: "TaskSettingESQuery", icon: "mdi-home"},
      {name: "企业微信机器人", path: "TaskSettingBot", icon: "mdi-chat"},
      {name: "推送文本", path: "TaskSettingTemplate", icon: "mdi-comment"},
      {name: "占位符", path: "TaskSettingPlaceholder", icon: "mdi-details"},
      {name: "检测和推送频率", path: "TaskSettingFrequency", icon: "mdi-timer"},
      {name: "数据导出", path: "TaskSettingExport", icon: "mdi-download"}
    ]

    /**
     * 加载数据
     *
     * @return void
     */
    mounted(): void {
      if (!this.$route.params.id) {
        this.$router.push("/");
        return;
      }
      let host: string = window.env.apiHost;
      this.$store.commit("loadStatus", {isLoading: true});
      axios.get(host + "/pl/task-info", {
        params: {id: this.$route.params.id}
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          /* 需要注意，这个地方设置 setTaskSettingInfo 前需要把JSON字符串转换成对应的Placeholder对象 */
          let placeholders: Placeholder[] = [];
          if ("" != response.data.data.task.placeholders) {
            for (let placeholder of JSON.parse(response.data.data.task.placeholders)) {
              placeholders.push(new Placeholder(placeholder.placeholder, placeholder.start, placeholder.end));
            }
          }
          let saveData: any = JSON.parse(JSON.stringify(response.data.data.task));
          saveData.placeholders = placeholders;
          console.log("传递给store的数据是");
          console.log(saveData);
          this.$store.commit("setTaskSettingInfo", {taskSettingInfo: saveData});
          this.$router.push(this.buttonList[this.taskSettingIndex].path);
        } else {
          this.$store.commit("showDialog", {message: response.data.message, title: "获取配置信息失败"});
        }
      });
    }
  }
</script>

<style>
.chilbounce-enter-active {
  animation: bounce-in .1s;
}
.chilbounce-leave-active {
  animation: bounce-in .1s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
