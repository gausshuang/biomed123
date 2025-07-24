# 生物医学导航网站 - BioMed Navigator

🔬 专业的生物医学资源导航平台，为生物医学研究者提供最全面、最便捷的资源导航服务。

## 🌟 项目特色

- **🎯 专业性**：精选22个权威生物医学资源网站
- **📱 响应式**：完美适配桌面端和移动端
- **⚡ 高性能**：基于Vue.js + Element UI，加载速度快
- **🔍 SEO优化**：完整的搜索引擎优化，有利于Google Adsense
- **💰 变现准备**：预留广告位，为Adsense集成做好准备

## 🚀 在线演示

访问网站：[https://yourusername.github.io/biomed123/](https://yourusername.github.io/biomed123/)

## 📦 功能特性

### 核心功能
- **🏷️ 资源分类**：8大类生物医学资源分类
- **🔍 智能搜索**：支持按名称、描述、分类搜索
- **⭐ 收藏系统**：本地存储用户收藏的资源
- **📊 评分系统**：展示资源评分和使用推荐
- **🖼️ 图片集成**：Unsplash API提供高质量相关图片

### 资源分类（共8类22个资源）

1. **医学数据库** (4个)
   - PubMed、Google Scholar、Cochrane Library、Embase

2. **生物信息学工具** (4个)
   - NCBI、UniProt、Ensembl、BLAST

3. **医学期刊** (4个)
   - Nature、The Lancet、Cell、Science

4. **临床试验** (2个)
   - ClinicalTrials.gov、WHO ICTRP

5. **生物技术公司** (2个)
   - Thermo Fisher、Illumina

6. **医学教育** (2个)
   - Khan Academy Medicine、Coursera Medicine

7. **医学影像** (2个)
   - Radiopaedia、ITK-SNAP

8. **药物信息** (2个)
   - DrugBank、ChEMBL

## 🛠️ 技术栈

- **前端框架**：Vue.js 2.6.14
- **UI组件库**：Element UI
- **样式语言**：CSS3 (原生)
- **图片API**：Unsplash API
- **部署平台**：GitHub Pages
- **自动化部署**：GitHub Actions

## 📋 部署指南

### 方法一：GitHub Pages自动部署 (推荐)

1. **Fork 或下载项目**
   ```bash
   git clone https://github.com/yourusername/biomed123.git
   cd biomed123
   ```

2. **推送到你的GitHub仓库**
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **启用GitHub Pages**
   - 进入GitHub仓库 → Settings → Pages
   - Source选择：GitHub Actions
   - 等待自动部署完成

4. **访问网站**
   - 网站将部署到：`https://YOUR_USERNAME.github.io/YOUR_REPO/`

### 方法二：手动部署

1. **下载所有文件**
2. **上传到任何静态网站托管服务**（如Netlify、Vercel等）
3. **确保index.html作为主页**

## ⚙️ 配置说明

### Unsplash API配置 (可选)

1. 注册 [Unsplash Developer](https://unsplash.com/developers)
2. 获取Access Key
3. 修改 `js/app.js` 中的配置：
   ```javascript
   const UNSPLASH_ACCESS_KEY = 'YOUR_UNSPLASH_ACCESS_KEY';
   ```

### Google Adsense配置

1. 申请Google Adsense账号
2. 修改 `index.html` 中的Adsense账号：
   ```html
   <meta name="google-adsense-account" content="ca-pub-YOUR_PUBLISHER_ID">
   ```
3. 在广告位区域添加Adsense代码

### SEO优化配置

1. **修改网站URL**：更新 `robots.txt` 和 `sitemap.xml` 中的域名
2. **Google Analytics**：在 `js/app.js` 中添加GA代码
3. **关键词优化**：根据需要修改meta标签中的关键词

## 📁 项目结构

```
biomed123/
├── index.html              # 主页
├── css/
│   └── style.css          # 样式文件
├── js/
│   └── app.js             # Vue应用逻辑
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions部署配置
├── robots.txt             # 搜索引擎爬虫配置
├── sitemap.xml            # 网站地图
├── log.md                 # 开发日志
└── README.md              # 项目说明
```

## 🎨 自定义指南

### 添加新的资源网站

1. 编辑 `js/app.js`
2. 在对应分类的 `sites` 数组中添加新对象：
   ```javascript
   {
       id: 23,
       name: '网站名称',
       url: 'https://example.com',
       description: '网站描述',
       logo: '图标URL',
       rating: 4.5,
       category: '分类名称',
       categoryType: 'primary'
   }
   ```

### 修改颜色主题

编辑 `css/style.css` 中的颜色变量：
```css
/* 主色调 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 强调色 */
color: #42d885;
```

### 添加新的分类

1. 在 `js/app.js` 的 `categories` 数组中添加新分类
2. 使用Element UI的图标类名

## 🔧 常见问题

### Q: 如何更换图标？
A: 使用Element UI的内置图标，参考：[Element UI Icons](https://element.eleme.io/#/zh-CN/component/icon)

### Q: 如何优化加载速度？
A: 可以使用CDN加速或将第三方库本地化

### Q: 支持多语言吗？
A: 当前版本为中文，可以通过修改HTML和JS中的文本实现多语言

### Q: 如何添加Google Analytics？
A: 在HTML头部添加GA代码，并在 `js/app.js` 中配置事件追踪

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📝 更新日志

查看 [log.md](log.md) 了解详细的开发历程和更新记录。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解更多详情。

## 📞 联系方式

- 项目链接：[https://github.com/yourusername/biomed123](https://github.com/yourusername/biomed123)
- 问题反馈：[Issues](https://github.com/yourusername/biomed123/issues)

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [Element UI](https://element.eleme.io/) - 基于Vue 2.0的桌面端组件库
- [Unsplash](https://unsplash.com/) - 高质量免费图片API
- [GitHub Pages](https://pages.github.com/) - 免费静态网站托管

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！ 