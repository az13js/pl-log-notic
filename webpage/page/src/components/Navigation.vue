<!-- 导航栏 -->
<template>
  <v-navigation-drawer app class="navigation-common-style" width="170px" mobile-breakpoint="400">
    <v-list dense nav class="py-0">
      <v-list-item>
        <v-list-item-content>
          <h1 class="title">
            <span>pl-log-notic</span>
          </h1>
          <!-- 对话框，失败时弹出，可以全局使用 -->
          <v-dialog v-model="failDialog" max-width="600px">
            <v-card>
              <v-card-title><span class="headline">{{ dialogTitle }}</span></v-card-title>
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
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item v-for="item in items" :key="item.title" link nav>
        <v-list-item-content>
          <v-list-item-title>
            <router-link v-bind:to="item.path">
              <h2 class="body-2 navigation-list-style">{{ item.title }}</h2>
            </router-link>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";

  @Component
  export default class Navigation extends Vue {
    get failDialog(): boolean {
      return this.$store.state.dialog.isShow;
    }
    get dialogTitle(): string {
      return this.$store.state.dialog.title;
    }
    get errorMessage(): string {
      return this.$store.state.dialog.message;
    }
    set failDialog(v: boolean) {
      let data: any = JSON.parse(JSON.stringify(this.$store.state.dialog));
      if (!v) {
        this.$store.commit("closeDialog", {});
      } else {
        this.$store.commit("showDialog", data);
      }
    }
    set dialogTitle(v: string) {
      let data: any = JSON.parse(JSON.stringify(this.$store.state.dialog));
      data.title = v;
      if (!data.isShow) {
        this.$store.commit("closeDialog", {});
      } else {
        this.$store.commit("showDialog", data);
      }
    }
    set errorMessage(v: string) {
      let data: any = JSON.parse(JSON.stringify(this.$store.state.dialog));
      data.message = v;
      if (!data.isShow) {
        this.$store.commit("closeDialog", {});
      } else {
        this.$store.commit("showDialog", data);
      }
    }

    public items: any[] = [
      {title: "监控任务", path:"/"}
    ]

    /**
     * 关闭失败对话框
     *
     * @returns {void}
     */
    public closeFailDialog(): void {
      this.$store.commit("closeDialog", {});
    }
  }
</script>

<style lang="sass">
.navigation-common-style
  -moz-user-select: "-moz-none"
  -webkit-user-select: none
  -ms-user-select: none
  -khtml-user-select: none
  user-select: none
.navigation-list-style, a, a:hover
  text-decoration: none
  color: white
</style>
