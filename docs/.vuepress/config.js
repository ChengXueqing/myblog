module.exports = {
  title: '学庆的博客',
  description: '朝花夕拾 日记不辍',
  head: [ // 注入到当前页面的 HTML <head> 中的标签
    ['link', { rel: 'icon', href: '/images/photo.webp' }],
    ['link', { rel: 'manifest', href: '/images/photo.webp' }],
    ['link', { rel: 'apple-touch-icon', href: '/images/photo.webp' }],
    ['meta', { 'http-quiv': 'pragma', cotent: 'no-cache'}],
    ['meta', { 'http-quiv': 'expires', cotent: '0'}],
    ['meta', { 'http-quiv': 'pragma', cotent: 'no-cache, must-revalidate'}]
  ],
  serviceWorker: true, // 是否开启 PWA
  base: '/', // 部署到github相关的配置
  markdown: {
    lineNumbers: true // 代码块是否显示行号
  },
  // 支持评论
  enhanceApp: ({ app }) => {
    const requireComponent = require.context(
      './components',
      true,
      /\.vue$/
    );
    requireComponent.keys().forEach(fileName => {
      const componentConfig = requireComponent(fileName);
      const componentName = componentConfig.default.name;
      app.component(componentName, componentConfig.default);
    });
  },
  themeConfig: {
    nav:[ // 导航栏配置
      {text: '前端基础', link: '/basic/1.html' },
      {text: '面试题合集', link: '/interview/1.html'},
      {text: '静以修身', link: '/advanced/1.html'},
      {text: '诗和远方', link: '/others/1.html'},
      {text: 'Github', link: 'https://github.com/ChengXueqing'}      
    ],
    sidebar:{ // 侧边栏配置
      '/basic/': [
          {
            title: '前端基础',
            children: [
              '/basic/1.html',
              '/basic/2.html',
              '/basic/3.html',
              '/basic/4.html',
              '/basic/5.html',
              '/basic/6.html',
              '/basic/7.html',
              '/basic/8.html',
              '/basic/9.html',
              '/basic/10.html',
              '/basic/11.html',
              '/basic/12.html',
              '/basic/13.html',
            ]
          }
      ],
      '/advanced/': [
        {
          title: '进阶之路',
          children: [
            '/advanced/1.html',
            '/advanced/2.html'
          ]
        }
      ],
      '/interview/': [
        {
          title: '面试题合集',
          children: [
            '/interview/1.html',
            '/interview/2.html'  
          ]
        }
      ],
      '/others/': [
        {
          title: '诗和远方',
          children: [
            '/others/1.html',
            '/others/2.html',
            '/others/3.html',
            '/others/4.html',
            '/others/5.html',
            '/others/6.html',
            '/others/7.html'
          ]
        }
      ],
    }
  }
};
