// SEO增强功能脚本
// 专门为生物医学导航网站优化搜索引擎表现

class SEOEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.addStructuredData();
        this.optimizeImages();
        this.addBreadcrumbs();
        this.setupSocialSharing();
        this.trackUserEngagement();
        this.addPreconnectLinks();
        this.optimizePageSpeed();
    }

    // 添加更多结构化数据
    addStructuredData() {
        // 医院排行榜数据结构化
        const hospitalRankingData = {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "name": "中国医院专科声誉排行榜",
            "description": "涵盖全国7大地区2683家医院的专科声誉排行榜数据，包括华东、华北、华南、西南、华中、西北、东北等地区。",
            "url": "https://gausshuang.github.io/biomed123/",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "creator": {
                "@type": "Organization",
                "name": "生物医学导航团队"
            },
            "distribution": [
                {
                    "@type": "DataDownload",
                    "encodingFormat": "CSV",
                    "contentUrl": "https://gausshuang.github.io/biomed123/complete_hospitals_data.json"
                }
            ],
            "temporalCoverage": "2023",
            "spatialCoverage": {
                "@type": "Place",
                "name": "中国"
            },
            "keywords": ["医院排行榜", "专科医院", "医院评级", "中国医院", "医疗质量"]
        };

        // 组织机构数据
        const organizationData = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "生物医学导航",
            "alternateName": "BioMed Navigator",
            "url": "https://gausshuang.github.io/biomed123/",
            "logo": "https://gausshuang.github.io/biomed123/images/logo.png",
            "sameAs": [],
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "email": "contact@biomednavigator.com"
            },
            "areaServed": "CN",
            "knowsAbout": [
                "生物医学",
                "医院排行榜", 
                "医学数据库",
                "生物信息学",
                "医学期刊",
                "临床试验"
            ]
        };

        // 面包屑导航数据
        const breadcrumbData = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "首页",
                    "item": "https://gausshuang.github.io/biomed123/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "医院排行榜",
                    "item": "https://gausshuang.github.io/biomed123/#hospital-ranking"
                }
            ]
        };

        // FAQ数据
        const faqData = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "如何查询医院专科排行榜？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "您可以通过我们的网站按地区和科室筛选查看全国医院专科排行榜，涵盖华东、华北、华南、西南、华中、西北、东北等7大地区的2683家医院。"
                    }
                },
                {
                    "@type": "Question",
                    "name": "网站提供哪些生物医学资源？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "我们提供PubMed、NCBI、Google Scholar等生物医学数据库，Nature、Cell、Lancet等顶级期刊，以及BLAST、Galaxy等生物信息学工具的导航链接。"
                    }
                },
                {
                    "@type": "Question",
                    "name": "数据来源是什么？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "医院排行榜数据基于2023年度中国医院专科声誉排行榜，由权威医学机构发布，确保数据的可靠性和时效性。"
                    }
                }
            ]
        };

        // 插入结构化数据
        this.insertStructuredData('hospital-ranking-data', hospitalRankingData);
        this.insertStructuredData('organization-data', organizationData);
        this.insertStructuredData('breadcrumb-data', breadcrumbData);
        this.insertStructuredData('faq-data', faqData);
    }

    insertStructuredData(id, data) {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.id = id;
        script.textContent = JSON.stringify(data);
        document.head.appendChild(script);
    }

    // 图片优化
    optimizeImages() {
        // 为图标添加alt属性
        const icons = document.querySelectorAll('.link-icon, [role="img"]');
        icons.forEach(icon => {
            if (!icon.getAttribute('alt') && !icon.getAttribute('aria-label')) {
                const text = icon.textContent || icon.innerText;
                if (text) {
                    icon.setAttribute('aria-label', text + '图标');
                }
            }
        });

        // 懒加载优化
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.getAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }
        });
    }

    // 添加面包屑导航
    addBreadcrumbs() {
        const breadcrumbContainer = document.createElement('nav');
        breadcrumbContainer.className = 'breadcrumb-nav';
        breadcrumbContainer.setAttribute('aria-label', '面包屑导航');
        
        const breadcrumbList = document.createElement('ol');
        breadcrumbList.className = 'breadcrumb-list';
        
        // 首页面包屑
        const homeItem = document.createElement('li');
        homeItem.className = 'breadcrumb-item';
        const homeLink = document.createElement('a');
        homeLink.href = '/biomed123/';
        homeLink.textContent = '首页';
        homeLink.setAttribute('aria-label', '返回首页');
        homeItem.appendChild(homeLink);
        breadcrumbList.appendChild(homeItem);

        // 当前页面面包屑
        const currentItem = document.createElement('li');
        currentItem.className = 'breadcrumb-item current';
        currentItem.setAttribute('aria-current', 'page');
        currentItem.textContent = '生物医学导航';
        breadcrumbList.appendChild(currentItem);

        breadcrumbContainer.appendChild(breadcrumbList);
        
        // 插入到主内容区域前
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.insertBefore(breadcrumbContainer, mainContent.firstChild);
        }

        // 添加面包屑样式
        this.addBreadcrumbStyles();
    }

    addBreadcrumbStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .breadcrumb-nav {
                padding: 10px 0;
                margin-bottom: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            
            .breadcrumb-list {
                display: flex;
                list-style: none;
                margin: 0;
                padding: 0 20px;
                align-items: center;
            }
            
            .breadcrumb-item {
                font-size: 14px;
            }
            
            .breadcrumb-item:not(:last-child)::after {
                content: " › ";
                margin: 0 8px;
                color: #666;
            }
            
            .breadcrumb-item a {
                color: #667eea;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .breadcrumb-item a:hover {
                color: #764ba2;
                text-decoration: underline;
            }
            
            .breadcrumb-item.current {
                color: #333;
                font-weight: 500;
            }
        `;
        document.head.appendChild(style);
    }

    // 社交分享功能
    setupSocialSharing() {
        const shareData = {
            title: '生物医学导航 - 全国医院专科排行榜与生物医学资源导航',
            text: '专业的生物医学导航平台，提供全国医院专科排行榜查询，涵盖7大地区2683家医院排名。',
            url: window.location.href
        };

        // 添加分享按钮（可选）
        if (navigator.share) {
            const shareBtn = document.createElement('button');
            shareBtn.textContent = '分享网站';
            shareBtn.className = 'share-btn';
            shareBtn.addEventListener('click', async () => {
                try {
                    await navigator.share(shareData);
                    console.log('分享成功');
                } catch (err) {
                    console.log('分享取消或失败');
                }
            });
        }
    }

    // 用户参与度跟踪
    trackUserEngagement() {
        // 页面停留时间
        let startTime = Date.now();
        
        window.addEventListener('beforeunload', () => {
            const timeSpent = Math.round((Date.now() - startTime) / 1000);
            // 发送到分析服务（如Google Analytics）
            if (typeof gtag !== 'undefined') {
                gtag('event', 'page_timing', {
                    'time_on_page': timeSpent
                });
            }
        });

        // 滚动深度跟踪
        let maxScroll = 0;
        window.addEventListener('scroll', () => {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
                
                // 发送滚动深度事件
                if (typeof gtag !== 'undefined') {
                    if (maxScroll >= 25 && maxScroll < 50) {
                        gtag('event', 'scroll_depth', { 'depth': '25%' });
                    } else if (maxScroll >= 50 && maxScroll < 75) {
                        gtag('event', 'scroll_depth', { 'depth': '50%' });
                    } else if (maxScroll >= 75 && maxScroll < 90) {
                        gtag('event', 'scroll_depth', { 'depth': '75%' });
                    } else if (maxScroll >= 90) {
                        gtag('event', 'scroll_depth', { 'depth': '90%' });
                    }
                }
            }
        });
    }

    // 添加预连接链接
    addPreconnectLinks() {
        const preconnectUrls = [
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com',
            'https://www.google-analytics.com',
            'https://googleads.g.doubleclick.net'
        ];

        preconnectUrls.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preconnect';
            link.href = url;
            document.head.appendChild(link);
        });
    }

    // 页面速度优化
    optimizePageSpeed() {
        // Critical CSS内联（简化版）
        const criticalCSS = `
            .top-section { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 0;
                color: white;
            }
            .site-logo { 
                font-size: 2.5rem; 
                margin: 0; 
                font-weight: 700; 
            }
            .search-box { 
                display: flex; 
                max-width: 600px; 
                margin: 20px auto 0; 
            }
        `;

        const style = document.createElement('style');
        style.textContent = criticalCSS;
        document.head.insertBefore(style, document.head.firstChild);

        // 延迟加载非关键资源
        this.deferNonCriticalResources();
    }

    deferNonCriticalResources() {
        // 延迟加载Google Analytics
        setTimeout(() => {
            if (typeof gtag === 'undefined') {
                const script = document.createElement('script');
                script.async = true;
                script.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
                document.head.appendChild(script);

                script.onload = () => {
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){dataLayer.push(arguments);}
                    gtag('js', new Date());
                    gtag('config', 'GA_MEASUREMENT_ID');
                    window.gtag = gtag;
                };
            }
        }, 2000);
    }

    // 添加页面质量指标
    addPageQualityMetrics() {
        // Core Web Vitals监控
        if ('web-vital' in window) {
            import('https://unpkg.com/web-vitals@3/dist/web-vitals.js').then(({getCLS, getFID, getFCP, getLCP, getTTFB}) => {
                getCLS(console.log);
                getFID(console.log);
                getFCP(console.log);
                getLCP(console.log);
                getTTFB(console.log);
            });
        }
    }
}

// 页面加载完成后初始化SEO增强
document.addEventListener('DOMContentLoaded', () => {
    new SEOEnhancements();
});

// 导出类以供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SEOEnhancements;
}