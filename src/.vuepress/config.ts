import { defineUserConfig } from "vuepress";

import theme from "./theme.js";

export default defineUserConfig({
  base: "/",

  lang: "zh-CN",
  title: "愢曦的博客",
  description: "分享日常，品悟人生。",

  theme,

  // 和 PWA 一起启用
  // shouldPrefetch: false,
});
