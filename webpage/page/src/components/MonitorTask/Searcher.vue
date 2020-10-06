<template>
  <v-container>
    <v-row>
      <v-col cols="10">
        <v-text-field :disabled="isLoading" v-model="taskName" label="任务名称" counter="64" clearable ></v-text-field>
      </v-col>
      <v-col cols="1">
        <v-btn :disabled="isLoading" color="primary" fab>搜索</v-btn>
      </v-col>
      <v-col cols="1">
        <!-- 对话框，点击新建按钮弹出，用于填写新建的任务名称 -->
        <v-dialog v-model="dialog" persistent max-width="600px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn :disabled="isLoading" color="green" v-bind="attrs" v-on="on" fab>新建</v-btn>
          </template>
          <v-card>
            <v-card-title><span class="headline">新建任务</span></v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field :disabled="isLoading" v-model="newTaskName" label="任务名称" counter="64" required></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="teal" :disabled="isLoading" @click="cancelCreateDialog()" text>取消</v-btn>
              <v-btn color="teal" :disabled="isLoading" @click="createEmptyTask()" text>确定</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!-- 对话框结束 -->
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
  export default class Searcher extends Vue {
    set taskName(v: string) {
      let columns: any = JSON.parse(JSON.stringify(this.$store.state.queryColumns));
      columns.taskName = v;
      this.$store.commit("setQueryColumns", {queryColumns: columns});
    }
    get taskName() {
      if (this.$store.state.queryColumns.taskName) {
        return this.$store.state.queryColumns.taskName;
      }
      return "";
    }
    get isLoading() {
      return this.$store.state.isLoading;
    }
    set isLoading(value: boolean) {
      this.$store.commit("loadStatus", {isLoading: value});
    }

    dialog: boolean = false
    newTaskName: string = ""
    createEmptyTask(): void {
      let host: string = window.env.apiHost;
      this.$store.commit("loadStatus", {isLoading: true});
      this.dialog = false;
      axios.get(host + "/monitor-task", {
        params: {taskName: this.newTaskName}
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        this.newTaskName = "";
        this.$router.push({
          name: "TaskSetting",
          params: {
            id: "1"
          }
        });
      });
    }
    cancelCreateDialog(): void {
      this.dialog = false;
      this.newTaskName = "";
    }
  }
</script>
