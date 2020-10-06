export default class Placeholder {

  /** @type {string} 占位符 */
  public placeholder: string = "";

  /** @type {string} 匹配的开始字符 */
  public start: string = "";

  /** @type {string} 匹配的结束字符 */
  public end: string = "";

  /**
   * 设置占位符信息
   *
   * @param {string} placeholder 占位符
   * @param {string} start 匹配的开始字符
   * @param {string} end 匹配的结束字符
   */
  constructor(placeholder: string, start: string, end: string) {
    this.placeholder = placeholder;
    this.start = start;
    this.end = end;
  }

  /**
   * 根据设置的占位符信息解析字符串，返回匹配的结果
   *
   * 当开始符号和结束符号之间没有任何字符时，匹配到空的字符串，""
   *
   * @param {string} contents 原始数据
   * @returns {string[]} 数组形式返回符合规则的所有结果
   */
  public parse(contents: string): string[] {
    if ("" === this.placeholder) { // 没有 placeholder 那么不匹配任何东西
      return [];
    }
    if ("" === this.start && "" === this.end) { // 没有写开始和结束符号那么匹配整个字符串
      return [contents];
    }
    if ("" === this.start && "" !== this.end) { // 没有开始只有结束那么匹配从一开始到结束符号的中间子串
      let endOffset = contents.indexOf(this.end);
      if (endOffset < 0) {
        return [];
      }
      if (endOffset == 0) {
        return [""];
      }
      return [contents.substring(0, endOffset)];
    }
    if ("" !== this.start && "" === this.end) { // 有开始没有结束那么匹配开始字符到结束之间的子串
      let startOffset = contents.indexOf(this.end);
      if (startOffset < 0) {
        return [];
      }
      return [contents.substring(startOffset + this.start.length)];
    }
    // 下面处理给出了开始和结束字符时的计算
    let matchs: string[] = [];
    let startOffset: number = 0;
    let endOffset: number = 0;
    // 从上次匹配到的内容后面开始寻找开始字符。找到开始字符时进入 while 循环体
    while ((startOffset = contents.indexOf(this.start, endOffset)) >= 0) {
      // 从找到的开始字符之后开始寻找结束字符
      endOffset = contents.indexOf(this.end, startOffset + this.start.length);
      if (endOffset < 0) { // 没有结束字符则匹配完成
        break;
      }
      matchs.push(contents.substring(startOffset + this.start.length, endOffset));
    }
    return matchs;
  }
}