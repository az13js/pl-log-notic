<!-- 占位符设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row v-for="(item, index) in placeholders">
      <v-col cols="3"><v-text-field v-model="item.placeholder" label="占位符" counter="100" clearable></v-text-field></v-col>
      <v-col cols="3"><v-text-field v-model="item.start" label="开始符号" counter="100" clearable></v-text-field></v-col>
      <v-col cols="3"><v-text-field v-model="item.end" label="结束符号" counter="100" clearable></v-text-field></v-col>
      <v-col cols="3"><v-btn color="red darken-4" @click="deletePlaceholder(index)" fab><v-icon>mdi-delete</v-icon></v-btn></v-col>
    </v-row>
    <v-row>
      <v-col cols="1">
        <v-btn color="green" @click="addEmptyPlaceholder()" fab><v-icon>mdi-plus</v-icon></v-btn>
      </v-col>
      <v-col cols="11">
        <p>添加占位符</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-list>
          <v-list-group>
            <template v-slot:activator>
              <v-list-item-title>占位符测试</v-list-item-title>
            </template>
            <v-list-item-content>
              <v-container class="pt-0 mt-0 pb-0 mb-0">
                <v-row>
                  <v-col cols="12">
                    <p><v-textarea label="测试输入" v-model="testInputText" clearable></v-textarea></p>
                    <p><v-textarea label="消息文本模板" counter="1024" v-model="testTemplateText" clearable></v-textarea></p>
                    <v-btn color="orange" @click="testPlaceholders()">运行测试</v-btn>
                    <p><v-textarea label="测试结果" counter="1024" v-model="testOutputText" clearable></v-textarea></p>
                  </v-col>
                </v-row>
              </v-container>
            </v-list-item-content>
          </v-list-group>
        </v-list>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" @click="save()" block>保存此监控任务所有的改动</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Component from "vue-class-component";
  import Placeholder from "./TaskSettingPlaceholder/Placeholder.ts";
  import TemplateParser from "./TaskSettingPlaceholder/TemplateParser.ts";
  import TaskSettingBase from "./TaskSettingBase.ts";

  @Component
  export default class TaskSettingPlaceholder extends TaskSettingBase {
    set placeholders(v: Placeholder[]) {
      let src: any = this.$store.state.taskSettingInfo;
      src.placeholders = v;
      this.$store.commit("setTaskSettingInfo", {taskSettingInfo: src});
    }
    get placeholders(): Placeholder[] {
      console.log("getter返回的数据是");
      console.log(this.$store.state.taskSettingInfo.placeholders);
      return this.$store.state.taskSettingInfo.placeholders;
    }

    public testInputText: string = ""
    public testTemplateText: string = ""
    public testOutputText: string = ""

    public mounted(): void {
      if ("" != this.$store.state.esQueryResult && "" == this.testInputText) {
        this.testInputText = this.$store.state.esQueryResult;
      }
    }

    public addEmptyPlaceholder(): void {
      this.placeholders.push(new Placeholder("", "", ""))
    }
    public deletePlaceholder(index: number): void {
      this.placeholders.splice(index, 1);
    }
    public testPlaceholders(): void {
      // 偶然出现this.placeholders中的元素不存在parse方法的报错，由于找不到原因，这里新建Placeholder对象，尝试避免出错。
      let placeholders: Placeholder[] = this.placeholders;
      let newPlaceholders: Placeholder[] = [];
      for (let p of placeholders) {
        newPlaceholders.push(new Placeholder(p.placeholder, p.start, p.end));
      }
      let parser: TemplateParser = new TemplateParser(newPlaceholders, this.testInputText);
      this.testOutputText = parser.parse(this.testTemplateText);
    }
  }
</script>
