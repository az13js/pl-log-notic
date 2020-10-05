import Placeholder from "./Placeholder.ts";

export default class TemplateParser {

  /** @type {Placeholder[]} 使用到的所有占位符对象 */
  private placeholders: Placeholder[] = [];

  /** @type {string[][]} 每个占位符对应的解析结果 */
  private placeholderResults: string[][] = [];

  /**
   * 利用占位符信息，从原始数据提取信息
   *
   * @param {Placeholder[]} placeholders
   * @param {string} sourceText
   */
  constructor(placeholders: Placeholder[], sourceText: string) {
    this.placeholders = placeholders;
    for (let placeholder of placeholders) {
      this.placeholderResults.push(placeholder.parse(sourceText));
    }
  }

  /**
   * 占位符替换
   *
   * @param {string} templateText
   */
  public parse(templateText: string): string {
    let placeholder: Placeholder;
    let results: string[];
    let replaceString: string = templateText;
    for (let key in this.placeholders) {
      placeholder = this.placeholders[key];
      results = this.placeholderResults[key];
      if (placeholder.placeholder === "") {
        continue;
      }
      replaceString = replaceString.replace(placeholder.placeholder, results.join(","));
    }
    return replaceString;
  }
}