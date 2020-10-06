import Vue, { VNode, CreateElement } from "vue";
import App from "./App.vue";
import axios from "axios";
import vuetify from "./plugins/vuetify.ts";
import store from "./store/index.ts";
import VueRouter, { RouteConfig } from "vue-router";

import MonitorTask from "./components/MonitorTask/Main.vue";
import TaskSetting from "./components/TaskSetting/Main.vue"; // 设置页面，下面的是它的子页面
import TaskSettingESAddress from "./components/TaskSetting/TaskSettingESAddress.vue";
import TaskSettingESQuery from "./components/TaskSetting/TaskSettingESQuery.vue";
import TaskSettingBot from "./components/TaskSetting/TaskSettingBot.vue";
import TaskSettingTemplate from "./components/TaskSetting/TaskSettingTemplate.vue";
import TaskSettingPlaceholder from "./components/TaskSetting/TaskSettingPlaceholder.vue";
import TaskSettingFrequency from "./components/TaskSetting/TaskSettingFrequency.vue";

Vue.prototype.$axios = axios;
Vue.use(VueRouter);

const routes: RouteConfig[] = [
  { name: "Root", path: "/", component: MonitorTask },
  { name: "TaskSetting", path: "/TaskSetting", component: TaskSetting, children: [
    { name: "TaskSettingESAddress", path: "/TaskSettingESAddress", component: TaskSettingESAddress },
    { name: "TaskSettingESQuery", path: "/TaskSettingESQuery", component: TaskSettingESQuery },
    { name: "TaskSettingBot", path: "/TaskSettingBot", component: TaskSettingBot },
    { name: "TaskSettingTemplate", path: "/TaskSettingTemplate", component: TaskSettingTemplate },
    { name: "TaskSettingPlaceholder", path: "/TaskSettingPlaceholder", component: TaskSettingPlaceholder },
    { name: "TaskSettingFrequency", path: "/TaskSettingFrequency", component: TaskSettingFrequency }
  ] }
];

new Vue({
  vuetify,
  store,
  router: new VueRouter({routes}),
  el: '#app',
  render: (h: CreateElement): VNode => h(App)
});
