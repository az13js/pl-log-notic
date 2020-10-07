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
                    <v-text-field :disabled="isLoading" v-model="newTaskName" label="任务名称" counter="64" :rules="newTaskRules" required></v-text-field>
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
        <!-- 对话框，创建任务失败时弹出 -->
        <v-dialog v-model="createFailDialog" max-width="600px">
          <v-card>
            <v-card-title><span class="headline">创建失败</span></v-card-title>
            <v-card-text>
              <p>{{ errorMessage }}</p>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="teal" :disabled="isLoading" @click="closeFailDialog()" text>关闭</v-btn>
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

    /** @type {boolean} 当这个值为true则显示新建任务对话框 */
    public dialog: boolean = false

    /** @type {string} 填写的新建的任务名称 */
    public newTaskName: string = ""

    /** @type {any[]} 任务名称规则 */
    public newTaskRules: any[] = [
      (value: string): any => !/^\s*$/.test(value) || "任务名称不能为空"
    ]

    /** @type {boolean} 当这个值为true则显示创建任务失败对话框 */
    public createFailDialog: boolean = false

    /** @type {string} 创建任务失败的提示信息 */
    public errorMessage: string = ""

    /**
     * 执行新建任务的操作
     *
     * @returns {void}
     */
    public createEmptyTask(): void {
      let host: string = window.env.apiHost;
      this.$store.commit("loadStatus", {isLoading: true});
      this.dialog = false;

      if (/^\s*$/.test(this.newTaskName)) {
        this.doAddTaskFail("任务名称不能为空");
        return;
      }

      axios.post(host + "/pl/task-add", {
        params: {taskName: this.newTaskName}
      }).then((response: AxiosResponse): void => {
        if (0 == response.data.code) {
          this.doAddTaskSuccess("" + response.data.data.id); // string
        } else {
          this.doAddTaskFail(response.data.message);
        }
      });
    }

    /**
     * 关闭取消任务对话框
     *
     * @returns {void}
     */
    public cancelCreateDialog(): void {
      this.dialog = false;
      this.newTaskName = "";
    }

    /**
     * 关闭创建任务失败对话框
     *
     * @returns {void}
     */
    public closeFailDialog(): void {
      this.createFailDialog = false;
      this.errorMessage = "";
    }

    /**
     * 执行新建任务后成功的操作
     *
     * @param {string} taskId 任务ID，会用此ID跳转到配置任务的页面
     * @returns {void}
     */
    private doAddTaskSuccess(taskId: string): void {
      this.$store.commit("loadStatus", {isLoading: false});
      this.newTaskName = "";
      this.$router.push({
        name: "TaskSetting",
        params: {
          id: taskId
        }
      });
    }

    /**
     * 执行新建任务后失败的操作
     *
     * @param {string} message 错误的消息提示
     * @returns {void}
     */
    private doAddTaskFail(message: string): void {
      this.$store.commit("loadStatus", {isLoading: false});
      this.errorMessage = message;
      this.createFailDialog = true;
    }
  }
</script>
