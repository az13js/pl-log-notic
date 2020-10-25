<!-- 表格，任务列表 -->
<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-data-table item-key="id" :loading="isLoading" loading-text="正在加载数据……" mobile-breakpoint="400" :headers="headers" :items="desserts" calculate-widths disable-pagination disable-sort hide-default-footer>
          <template v-slot:item.actions="{ item }">
            <v-icon @click="locationTaskSetting(item)">mdi-pencil</v-icon>
          </template>
          <template v-slot:item.enable="{ item }">
            <v-btn v-if="item.status == 1" color="blue" :disabled="isLoading" @click="statusChange(item)" text>已开启</v-btn>
            <v-btn v-if="item.status == 0" color="red" :disabled="isLoading" @click="statusChange(item)" text>已关闭</v-btn>
          </template>
          <template v-slot:item.delete="{ item }">
            <v-icon @click="showDeleteTaskDialog(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
        <!-- 对话框，删除任务时用于确认 -->
        <v-dialog v-model="deleteTaskDialog" max-width="600px" persistent>
          <v-card>
            <v-card-title><span class="headline">删除任务</span></v-card-title>
            <v-card-text>
              <p>确定要删除任务“{{ deleteTaskName }}”吗？</p>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="teal" :disabled="isLoading" @click="deleteTaskNo()" text>取消</v-btn>
              <v-btn color="teal" :disabled="isLoading" @click="deleteTaskYes()" text>确定</v-btn>
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
  export default class Table extends Vue {
    get isLoading() {
      return this.$store.state.isLoading;
    }
    set isLoading(value: boolean) {
      this.$store.commit("loadStatus", {isLoading: value});
    }
    // 数据表中的数据
    get desserts() {
      return this.$store.state.desserts;
    }
    // 设置数据表中的数据
    set desserts(value: any) {
      this.$store.commit("updateDesserts", {desserts: value});
    }

    /** @type {object[]} 按钮 */
    public headers: object[] = [
      {text: '配置', value: 'actions'},
      {text: '开/关', value: 'enable'},
      {text: "任务名称", value: "name"},
      {text: "导出进度", value: "process"},
      {text: '删除', value: 'delete'}
    ]

    /** @type {boolean} 显示删除任务确认对话框 */
    public deleteTaskDialog: boolean = false

    /** @type {string} 删除的任务名称 */
    public deleteTaskName: string = ""

    /** @type {number} 删除的任务ID */
    private deleteTaskId: number = 0

    /**
     * 加载后执行，load首页数据
     *
     * @return {void}
     */
    public mounted(): void {
      let host: string = window.env.apiHost;
      this.$store.commit("loadStatus", {isLoading: true});
      axios.get(host + "/pl/task-list", {
        params: this.$store.state.queryColumns
      }).then((response: AxiosResponse): void => {
        let dataTable: any = JSON.parse(JSON.stringify(response.data.data.list));
        for (let job of dataTable) {
          job.process = "";
        }
        this.$store.commit("updateDesserts", {desserts: dataTable});
        this.$store.commit("loadStatus", {isLoading: false});
      });
      if (!this.$store.state.init) {
        this.$store.commit("initSuccess", {});
        // 每间隔2秒钟自动更新当前表格显示的JOB的状态
        setInterval((): void => {
          let ids: number[] = [];
          for (let task of this.$store.state.desserts) {
            ids.push(task.id);
          }
          if (ids.length <= 0) {
            return;
          }
          let host: string = window.env.apiHost;
          axios.get(host + "/pl/export-job-info", {
            params: {ids:ids.join(",")}
          }).then((response: AxiosResponse): void => {
            if (response.data.code == 0) {
              let dataTable: any = JSON.parse(JSON.stringify(this.$store.state.desserts));
              for (let exportJob of response.data.data.exportJobs) {
                for (let job of dataTable) {
                  if (job.id == exportJob.task_setting_id) {
                    job.process = parseInt(100 * exportJob.process + "") + "%";
                    if (this.$store.state.taskSettingInfo.id && this.$store.state.taskSettingInfo.id == exportJob.task_setting_id) {
                      this.$store.commit("setExportInfo", {
                        workerName: exportJob.worker_name,
                        downloadAddress: exportJob.download_addr,
                        status: exportJob.status,
                        reqStop: exportJob.req_stop,
                        process: exportJob.process
                      });
                    }
                    break;
                  }
                }
              }
              this.$store.commit("updateDesserts", {desserts: dataTable});
            }
          });
        }, 2000);
      }
    }

    /**
     * 点击按钮到配置监控任务的页面
     *
     * @param {any} item
     * @return {void}
     */
    public locationTaskSetting(item: any): void {
      this.$router.push({
        name: "TaskSetting",
        params: {
          id: item.id
        }
      });
    }

    /**
     * 关闭失败对话框
     *
     * @returns {void}
     */
    public closeFailDialog(): void {
      this.$store.commit("closeDialog", {});
    }

    /**
     * 显示删除任务对话框
     *
     * @param {any} item
     * @return {void}
     */
    public showDeleteTaskDialog(item: any): void {
      this.deleteTaskName = item.name;
      this.deleteTaskId = item.id;
      this.deleteTaskDialog = true;
    }

    /**
     * 关闭删除任务对话框
     *
     * @returns {void}
     */
    public deleteTaskNo(): void {
      this.deleteTaskDialog = false;
      this.deleteTaskName = "";
      this.deleteTaskId = 0;
    }

    /**
     * 确定删除任务
     *
     * @returns {void}
     */
    public deleteTaskYes(): void {
      this.$store.commit("loadStatus", {isLoading: true});
      let host: string = window.env.apiHost;
      axios.post(host + "/pl/task-delete", {
        params: {id: this.deleteTaskId}
      }).then((response: AxiosResponse): void => {
        this.deleteTaskDialog = false;
        this.deleteTaskName = "";
        this.deleteTaskId = 0;
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          this.$store.commit("loadStatus", {isLoading: true});
          axios.get(window.env.apiHost + "/pl/task-list", {
            params: this.$store.state.queryColumns
          }).then((response: AxiosResponse): void => {
            this.$store.commit("updateDesserts", {desserts: response.data.data.list});
            this.$store.commit("loadStatus", {isLoading: false});
          });
        } else {
          this.$store.commit("showDialog", {message: response.data.message, title: "删除任务失败"});
        }
      });
    }

    /**
     * 确定删除任务
     *
     * @returns {void}
     */
    public statusChange(task: any): void {
      this.isLoading = true;
      axios.post(window.env.apiHost + "/pl/task-set-status", {
        params: {id: task.id, status: 1 - task.status}
      }).then((response: AxiosResponse): void => {
        this.$store.commit("loadStatus", {isLoading: false});
        if (0 == response.data.code) {
          task.status = 1 - task.status;
        } else {
          this.$store.commit("showDialog", {message: response.data.message, title: "修改状态失败"});
        }
      });
    }
  }
</script>
