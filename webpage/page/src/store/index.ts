import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const opts = {
  //strict: true
  state: {
    desserts: [],
    isLoading: true,
    queryColumns: {
      startTime: "",
      endTime: "",
      page: 1
    },
    taskSettingIndex: 0
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
    setTaskSettingIndex(state: any, idx: number): void {
      state.taskSettingIndex = idx;
    }
  }
};

export default new Vuex.Store(opts);
