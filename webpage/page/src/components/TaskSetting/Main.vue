<!-- 任务设置页面 -->
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-bottom-navigation :value="taskSettingIndex" color="primary" background-color="rgba(0,0,0,0.04)" horizontal>
          <v-btn v-for="item in buttonList" v-bind:to="item.path">
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
      {name: "ES 地址", path: "TaskSettingESAddress", icon: "mdi-history"},
      {name: "ES 查询条件", path: "TaskSettingESQuery", icon: "mdi-history"},
      {name: "企业微信机器人", path: "TaskSettingBot", icon: "mdi-history"},
      {name: "推送文本", path: "TaskSettingTemplate", icon: "mdi-history"},
      {name: "占位符", path: "TaskSettingPlaceholder", icon: "mdi-history"},
      {name: "检测和推送频率", path: "TaskSettingFrequency", icon: "mdi-history"},
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
      axios.get(host + "/monitor-task", {
        params: {id: this.$route.params.id}
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        this.$router.push(this.buttonList[this.taskSettingIndex].path);
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
