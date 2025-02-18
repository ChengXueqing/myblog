<template>
  <div id="gitment-container"></div>
</template>

<script>
import Gitment from 'gitment';

export default {
  mounted() {
    const gitment = new Gitment({
      id: this.$route.path, // 用页面路径作为唯一标识
      owner: 'ChengXueqing', // 你的 GitHub 用户名
      repo: 'blog-comments', // 你创建的用于存储评论的仓库名
      oauth: {
        client_id: 'Ov23libLjAo6vTOujxoE', // 从 GitHub 注册的 OAuth 应用获取
        client_secret: '6c7c82ef1d0dbc280fcc7cead414c7f094ee6110', // 从 GitHub 注册的 OAuth 应用获取
      },
    });

    gitment.render('gitment-container');
  },
};
</script>

<style scoped>
/* 可以在这里添加 Gitment 评论框的样式 */
</style>