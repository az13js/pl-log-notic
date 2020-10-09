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
    taskSettingInfo: {},
    dialog: {
      title: "",
      message: "",
      isShow: false
    },
    esTestResult: ""
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
      state.taskSettingInfo = playload.taskSettingInfo;
    },
    setEsTestResult(state: any, playload: any): void {
      state.esTestResult = playload.esTestResult;
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
