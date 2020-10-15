import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const opts = {
  //strict: true
  state: {
    desserts: [],
    isLoading: true,
    queryColumns: {
      page: 1
    },
    taskSettingIndex: 0,
    taskSettingInfo: {}, // 里面的placeholders是Placeholder[]，不是string
    dialog: {
      title: "",
      message: "",
      isShow: false
    },
    esTestResult: "",
    esQueryResult: ""
  },
  mutations: {
    updateDesserts(state: any, playload: any): void {
      state.desserts = playload.desserts;
    },
    loadStatus(state: any, playload: any): void {
      state.isLoading = playload.isLoading;
    },
    setPage(state: any, playload: any): void {
      state.queryColumns.page = playload.page;
    },
    setQueryColumns(state: any, playload: any): void {
      state.queryColumns = playload.queryColumns;
    },
    setTaskSettingInfo(state: any, playload: any): void {
      console.log("store收到的数据是");
      console.log(playload.taskSettingInfo);
      state.taskSettingInfo = playload.taskSettingInfo;
    },
    setEsTestResult(state: any, playload: any): void {
      state.esTestResult = playload.esTestResult;
    },
    setEsQueryResult(state: any, playload: any): void {
      state.esQueryResult = playload.esQueryResult;
    },
    setTaskSettingIndex(state: any, idx: number): void {
      state.taskSettingIndex = idx;
    },
    showDialog(state: any, playload: any): void {
      state.dialog.title = playload.title;
      state.dialog.message = playload.message;
      state.dialog.isShow = true;
    },
    closeDialog(state: any, playload: any): void {
      state.dialog.title = "";
      state.dialog.message = "";
      state.dialog.isShow = false;
    }
  }
};

export default new Vuex.Store(opts);
