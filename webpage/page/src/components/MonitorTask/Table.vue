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
        <!-- 对话框，删除任务失败时弹出 -->
        <v-dialog v-model="deleteFailDialog" max-width="600px">
          <v-card>
            <v-card-title><span class="headline">删除失败</span></v-card-title>
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
      {text: '删除', value: 'delete'}
    ]

    /** @type {boolean} 删除任务失败对话框 */
    public deleteFailDialog: boolean = false

    /** @type {string} 错误消息 */
    public errorMessage: string = ""

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
        this.$store.commit("updateDesserts", {desserts: response.data.data.list});
        this.$store.commit("loadStatus", {isLoading: false});
      });
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
      this.deleteFailDialog = false;
      this.errorMessage = "";
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
          this.errorMessage = response.data.message;
          this.deleteFailDialog = true;
        }
      });
    }

    /**
     * 确定删除任务
     *
     * @returns {void}
     */
    public statusChange(task: any): void {
      if (1 == task.status) {
        task.status = 0;
      } else if (0 == task.status) {
        task.status = 1;
      }
    }
  }
</script>
