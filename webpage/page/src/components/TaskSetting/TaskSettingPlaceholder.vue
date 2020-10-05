<!-- 占位符设置页面 -->
<template>
  <v-container class="pt-0 mt-0">
    <v-row v-for="(item, index) in placeholders">
      <v-col cols="3"><v-text-field v-model="item.placeholder" label="占位符" counter="100" clearable></v-text-field></v-col>
      <v-col cols="3"><v-text-field v-model="item.start" label="开始符号" counter="100" clearable></v-text-field></v-col>
      <v-col cols="3"><v-text-field v-model="item.end" label="结束符号" counter="100" clearable></v-text-field></v-col>
      <v-col cols="3"><v-btn color="red" @click="deletePlaceholder(index)" fab><v-icon>mdi-delete</v-icon></v-btn></v-col>
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
              <v-card>
                <v-card-text>
                  <p><v-textarea label="测试输入" v-model="testInputText" clearable></v-textarea></p>
                  <p><v-textarea label="消息文本模板" counter="1024" v-model="testTemplateText" clearable></v-textarea></p>
                </v-card-text>
                <v-card-actions><v-btn color="orange" @click="testPlaceholders()">运行测试</v-btn></v-card-actions>
                <v-card-text>
                  <p><v-textarea label="测试结果" counter="1024" v-model="testOutputText" clearable></v-textarea></p>
                </v-card-text>
              </v-card>
            </v-list-item-content>
          </v-list-group>
        </v-list>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" block>保存此监控任务所有的改动</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import Placeholder from "./TaskSettingPlaceholder/Placeholder.ts";
  import TemplateParser from "./TaskSettingPlaceholder/TemplateParser.ts";

  @Component
  export default class TaskSettingPlaceholder extends Vue {
    public placeholders: Placeholder[] = [
      new Placeholder("a", "b", "c"),
      new Placeholder("d", "e", "f"),
      new Placeholder("g", "h", "i")
    ]
    public testInputText: string = ""
    public testTemplateText: string = ""
    public testOutputText: string = ""
    public addEmptyPlaceholder(): void {
      this.placeholders.push(new Placeholder("", "", ""))
    }
    public deletePlaceholder(index: number): void {
      this.placeholders.splice(index, 1);
    }
    public testPlaceholders(): void {
      let parser: TemplateParser = new TemplateParser(this.placeholders, this.testInputText);
      this.testOutputText = parser.parse(this.testTemplateText);
    }
  }
</script>
