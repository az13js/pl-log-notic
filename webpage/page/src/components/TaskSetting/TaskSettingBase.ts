import Vue from "vue";
import Component from "vue-class-component";
import axios, {AxiosResponse} from "axios";
import "../../defined.ts";

/**
 * 基类。配置修改各选项卡的公共类
 */
@Component
export default class TaskSettingBase extends Vue {
  get isLoading() {
    return this.$store.state.isLoading;
  }
  set isLoading(value: boolean) {
    this.$store.commit("loadStatus", {isLoading: value});
  }

  public save(): void {
    this.$store.commit("loadStatus", {isLoading: true});
    let data: any = JSON.parse(JSON.stringify(this.$store.state.taskSettingInfo));
    for (let key in data) {
      if (data[key] === null) {
        data[key] = "";
      }
    }
    data.placeholders = JSON.stringify(data.placeholders); // placeholders需要转成JSON字符串再存起来
    axios.post(window.env.apiHost + "/pl/task-save-info", {
      params: data
    }).then((response: AxiosResponse): void => {
      this.$store.commit("loadStatus", {isLoading: false});
      if (0 == response.data.code) {
        this.$store.commit("showDialog", {message: response.data.message, title: "保存成功"});
      } else {
        this.$store.commit("showDialog", {message: response.data.message, title: "保存失败"});
      }
    });
  }
}