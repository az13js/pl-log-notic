import Vue, { VNode, CreateElement } from "vue";
import App from "./App.vue";
import axios from "axios";
import vuetify from "./plugins/vuetify.ts";
import store from "./store/index.ts";
import VueRouter, { RouteConfig } from "vue-router";

Vue.prototype.$axios = axios;
Vue.use(VueRouter);

const routes: RouteConfig[] = [
  { name: "root", path: "/", component: FileList }
]

new Vue({
  vuetify,
  store,
  router: new VueRouter({routes}),
  el: '#app',
  render: (h: CreateElement): VNode => h(App)
});
