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
    esQueryResult: "",
    exportSetting: {
      startDate: "",
      startTime: "",
      endDate: "",
      endTime: "",
      template: ""
    },
    exportInfo: {
      workerName: "",
      downloadAddress: "",
      status: 0,
      reqStop: 0,
      process: 0
    },
    init: false,
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
    },
    setExportSetting(state: any, playload: any): void {
      state.exportSetting.startDate = playload.startDate;
      state.exportSetting.startTime = playload.startTime;
      state.exportSetting.endDate = playload.endDate;
      state.exportSetting.endTime = playload.endTime;
      state.exportSetting.template = playload.template;
    },
    initSuccess(state: any, playload: any): void {
      state.init = true;
    },
    setExportInfo(state: any, playload: any): void {
      state.exportInfo.workerName = playload.workerName;
      state.exportInfo.downloadAddress = playload.downloadAddress;
      state.exportInfo.status = playload.status;
      state.exportInfo.reqStop = playload.reqStop;
      state.exportInfo.process = playload.process;
    }
  }
};

export default new Vuex.Store(opts);
