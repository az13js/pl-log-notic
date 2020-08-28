import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const opts = {
  //strict: true
  state: {
    fileList: [],
    desserts: [],
    isLoading: true,
    queryColumns: {
      startTime: "",
      endTime: "",
      page: 1
    },
    inprocess: 0,
    isUploading: false
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
    setUploadStatus(state: any, playload: any): void {
      state.inprocess = playload.inprocess;
      state.isUploading = playload.isUploading;
    },
    setFileList(state: any, playload: any): void {
      state.fileList = playload.fileList;
    }
  }
};

export default new Vuex.Store(opts);
