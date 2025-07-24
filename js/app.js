// Unsplash API配置 - 请替换为您的API Key
const UNSPLASH_ACCESS_KEY = 'YOUR_UNSPLASH_ACCESS_KEY';
const UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random';

// Vue应用实例
new Vue({
    el: '#app',
    data: {
        searchQuery: '',
        heroImage: '',
        categoryDialogVisible: false,
        selectedCategory: { name: '', description: '', sites: [] },
        
        // 生物医学资源分类
        categories: [
            {
                id: 1,
                name: '医学数据库',
                description: '权威的医学文献和临床数据库',
                icon: 'el-icon-document-copy',
                sites: [
                    {
                        id: 1,
                        name: 'PubMed',
                        url: 'https://pubmed.ncbi.nlm.nih.gov/',
                        description: '世界最大的生物医学文献数据库，包含超过3400万篇文献引用',
                        logo: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=40&h=40&fit=crop&crop=center',
                        rating: 5,
                        category: '医学数据库',
                        categoryType: 'primary'
                    },
                    {
                        id: 2,
                        name: 'Google Scholar',
                        url: 'https://scholar.google.com/',
                        description: '学术搜索引擎，涵盖各个学科的学术文献',
                        logo: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=40&h=40&fit=crop&crop=center',
                        rating: 4.8,
                        category: '学术搜索',
                        categoryType: 'success'
                    },
                    {
                        id: 3,
                        name: 'Cochrane Library',
                        url: 'https://www.cochranelibrary.com/',
                        description: '系统评价和循证医学的权威资源',
                        logo: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=40&h=40&fit=crop&crop=center',
                        rating: 4.9,
                        category: '循证医学',
                        categoryType: 'warning'
                    },
                    {
                        id: 4,
                        name: 'Embase',
                        url: 'https://www.embase.com/',
                        description: '欧洲生物医学数据库，专注于药理学和医学研究',
                        logo: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=40&h=40&fit=crop&crop=center',
                        rating: 4.7,
                        category: '药理学',
                        categoryType: 'info'
                    }
                ]
            },
            {
                id: 2,
                name: '生物信息学工具',
                description: '基因组学、蛋白质组学分析工具',
                icon: 'el-icon-s-data',
                sites: [
                    {
                        id: 5,
                        name: 'NCBI',
                        url: 'https://www.ncbi.nlm.nih.gov/',
                        description: '美国国家生物技术信息中心，提供基因组和蛋白质数据库',
                        logo: 'https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=40&h=40&fit=crop&crop=center',
                        rating: 5,
                        category: '基因组学',
                        categoryType: 'primary'
                    },
                    {
                        id: 6,
                        name: 'UniProt',
                        url: 'https://www.uniprot.org/',
                        description: '蛋白质序列和功能信息的综合资源',
                        logo: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=40&h=40&fit=crop&crop=center',
                        rating: 4.8,
                        category: '蛋白质组学',
                        categoryType: 'success'
                    },
                    {
                        id: 7,
                        name: 'Ensembl',
                        url: 'https://www.ensembl.org/',
                        description: '基因组浏览器和注释数据库',
                        logo: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=center',
                        rating: 4.7,
                        category: '基因组浏览',
                        categoryType: 'warning'
                    },
                    {
                        id: 8,
                        name: 'BLAST',
                        url: 'https://blast.ncbi.nlm.nih.gov/',
                        description: '基本局部比对搜索工具，用于序列相似性搜索',
                        logo: 'https://images.unsplash.com/photo-1518373714866-3f1478910cc0?w=40&h=40&fit=crop&crop=center',
                        rating: 4.9,
                        category: '序列分析',
                        categoryType: 'info'
                    }
                ]
            },
            {
                id: 3,
                name: '医学期刊',
                description: '顶级医学和生物学期刊',
                icon: 'el-icon-reading',
                sites: [
                    {
                        id: 9,
                        name: 'Nature',
                        url: 'https://www.nature.com/',
                        description: '世界顶级科学期刊，发表各领域重要研究成果',
                        logo: 'https://images.unsplash.com/photo-1495592822108-9e6261896da8?w=40&h=40&fit=crop&crop=center',
                        rating: 5,
                        category: '综合科学',
                        categoryType: 'primary'
                    },
                    {
                        id: 10,
                        name: 'The Lancet',
                        url: 'https://www.thelancet.com/',
                        description: '世界领先的医学期刊之一',
                        logo: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=40&h=40&fit=crop&crop=center',
                        rating: 4.9,
                        category: '临床医学',
                        categoryType: 'danger'
                    },
                    {
                        id: 11,
                        name: 'Cell',
                        url: 'https://www.cell.com/',
                        description: '生命科学领域的顶级期刊',
                        logo: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=40&h=40&fit=crop&crop=center',
                        rating: 4.8,
                        category: '分子生物学',
                        categoryType: 'success'
                    },
                    {
                        id: 12,
                        name: 'Science',
                        url: 'https://www.science.org/',
                        description: '美国科学促进会发布的权威科学期刊',
                        logo: 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=40&h=40&fit=crop&crop=center',
                        rating: 4.9,
                        category: '综合科学',
                        categoryType: 'warning'
                    }
                ]
            },
            {
                id: 4,
                name: '临床试验',
                description: '临床试验注册和数据库',
                icon: 'el-icon-s-marketing',
                sites: [
                    {
                        id: 13,
                        name: 'ClinicalTrials.gov',
                        url: 'https://clinicaltrials.gov/',
                        description: '美国国立卫生研究院维护的临床试验注册数据库',
                        logo: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=40&h=40&fit=crop&crop=center',
                        rating: 4.8,
                        category: '临床试验',
                        categoryType: 'primary'
                    },
                    {
                        id: 14,
                        name: 'WHO ICTRP',
                        url: 'https://www.who.int/ictrp/',
                        description: '世界卫生组织国际临床试验注册平台',
                        logo: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=40&h=40&fit=crop&crop=center',
                        rating: 4.6,
                        category: '国际试验',
                        categoryType: 'info'
                    }
                ]
            },
            {
                id: 5,
                name: '生物技术公司',
                description: '全球领先的生物技术和制药公司',
                icon: 'el-icon-s-shop',
                sites: [
                    {
                        id: 15,
                        name: 'Thermo Fisher',
                        url: 'https://www.thermofisher.com/',
                        description: '全球生命科学解决方案的领导者',
                        logo: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=40&h=40&fit=crop&crop=center',
                        rating: 4.5,
                        category: '生命科学工具',
                        categoryType: 'success'
                    },
                    {
                        id: 16,
                        name: 'Illumina',
                        url: 'https://www.illumina.com/',
                        description: '基因测序技术的全球领导者',
                        logo: 'https://images.unsplash.com/photo-1628595351029-c2bf17511435?w=40&h=40&fit=crop&crop=center',
                        rating: 4.7,
                        category: '基因测序',
                        categoryType: 'primary'
                    }
                ]
            },
            {
                id: 6,
                name: '医学教育',
                description: '医学教育和继续教育资源',
                icon: 'el-icon-school',
                sites: [
                    {
                        id: 17,
                        name: 'Khan Academy Medicine',
                        url: 'https://www.khanacademy.org/science/health-and-medicine',
                        description: '免费的医学教育视频和课程',
                        logo: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=center',
                        rating: 4.4,
                        category: '在线教育',
                        categoryType: 'warning'
                    },
                    {
                        id: 18,
                        name: 'Coursera Medicine',
                        url: 'https://www.coursera.org/browse/health',
                        description: '世界顶级大学的医学在线课程',
                        logo: 'https://images.unsplash.com/photo-1495592822108-9e6261896da8?w=40&h=40&fit=crop&crop=center',
                        rating: 4.3,
                        category: '在线课程',
                        categoryType: 'info'
                    }
                ]
            },
            {
                id: 7,
                name: '医学影像',
                description: '医学影像和诊断工具',
                icon: 'el-icon-camera',
                sites: [
                    {
                        id: 19,
                        name: 'Radiopaedia',
                        url: 'https://radiopaedia.org/',
                        description: '开放获取的放射学资源和病例数据库',
                        logo: 'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=40&h=40&fit=crop&crop=center',
                        rating: 4.6,
                        category: '放射学',
                        categoryType: 'primary'
                    },
                    {
                        id: 20,
                        name: 'ITK-SNAP',
                        url: 'http://www.itksnap.org/',
                        description: '医学图像分割和可视化软件',
                        logo: 'https://images.unsplash.com/photo-1518373714866-3f1478910cc0?w=40&h=40&fit=crop&crop=center',
                        rating: 4.2,
                        category: '图像分析',
                        categoryType: 'success'
                    }
                ]
            },
            {
                id: 8,
                name: '药物信息',
                description: '药物数据库和药理学资源',
                icon: 'el-icon-medicine-box',
                sites: [
                    {
                        id: 21,
                        name: 'DrugBank',
                        url: 'https://go.drugbank.com/',
                        description: '综合的药物和药物靶点数据库',
                        logo: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=40&h=40&fit=crop&crop=center',
                        rating: 4.7,
                        category: '药物数据库',
                        categoryType: 'warning'
                    },
                    {
                        id: 22,
                        name: 'ChEMBL',
                        url: 'https://www.ebi.ac.uk/chembl/',
                        description: '生物活性化合物的数据库',
                        logo: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=40&h=40&fit=crop&crop=center',
                        rating: 4.5,
                        category: '化合物数据',
                        categoryType: 'info'
                    }
                ]
            }
        ],
        
        // 热门资源（从所有分类中筛选）
        popularSites: []
    },
    
    mounted() {
        this.initializePopularSites();
        this.loadHeroImage();
    },
    
    methods: {
        // 初始化热门资源
        initializePopularSites() {
            const allSites = [];
            this.categories.forEach(category => {
                allSites.push(...category.sites);
            });
            
            // 按评分排序，取前6个作为热门资源
            this.popularSites = allSites
                .sort((a, b) => b.rating - a.rating)
                .slice(0, 6);
        },
        
        // 从Unsplash加载英雄图片
        async loadHeroImage() {
            try {
                // 如果没有API Key，使用默认图片
                if (!UNSPLASH_ACCESS_KEY || UNSPLASH_ACCESS_KEY === 'YOUR_UNSPLASH_ACCESS_KEY') {
                    this.heroImage = 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&h=400&fit=crop&crop=center';
                    return;
                }
                
                const response = await axios.get(UNSPLASH_API_URL, {
                    params: {
                        query: 'medical research laboratory microscope',
                        w: 600,
                        h: 400,
                        fit: 'crop',
                        crop: 'center'
                    },
                    headers: {
                        'Authorization': `Client-ID ${UNSPLASH_ACCESS_KEY}`
                    }
                });
                
                this.heroImage = response.data.urls.regular;
            } catch (error) {
                console.error('Failed to load image from Unsplash:', error);
                // 使用默认图片作为备选
                this.heroImage = 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=600&h=400&fit=crop&crop=center';
            }
        },
        
        // 搜索网站
        searchSites() {
            if (!this.searchQuery.trim()) {
                this.$message.warning('请输入搜索关键词');
                return;
            }
            
            const query = this.searchQuery.toLowerCase();
            const results = [];
            
            this.categories.forEach(category => {
                category.sites.forEach(site => {
                    if (site.name.toLowerCase().includes(query) || 
                        site.description.toLowerCase().includes(query) ||
                        site.category.toLowerCase().includes(query)) {
                        results.push(site);
                    }
                });
            });
            
            if (results.length > 0) {
                this.$message.success(`找到 ${results.length} 个相关资源`);
                // 这里可以展示搜索结果页面
                console.log('搜索结果:', results);
            } else {
                this.$message.info('未找到相关资源，请尝试其他关键词');
            }
        },
        
        // 滚动到分类区域
        scrollToCategories() {
            const element = document.getElementById('categories');
            if (element) {
                element.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        },
        
        // 显示分类详情
        showCategoryDetail(category) {
            this.selectedCategory = category;
            this.categoryDialogVisible = true;
        },
        
        // 关闭分类详情对话框
        closeCategoryDialog() {
            this.categoryDialogVisible = false;
            this.selectedCategory = { name: '', description: '', sites: [] };
        },
        
        // 访问网站
        visitSite(url) {
            if (url) {
                window.open(url, '_blank', 'noopener,noreferrer');
                this.$message.success('正在跳转到目标网站...');
            }
        },
        
        // 添加到收藏夹
        addToFavorites(site) {
            // 这里可以实现收藏功能，保存到localStorage或发送到后端
            const favorites = JSON.parse(localStorage.getItem('biomedFavorites') || '[]');
            
            const existingIndex = favorites.findIndex(fav => fav.id === site.id);
            if (existingIndex === -1) {
                favorites.push(site);
                localStorage.setItem('biomedFavorites', JSON.stringify(favorites));
                this.$message.success(`已将 ${site.name} 添加到收藏夹`);
            } else {
                this.$message.info(`${site.name} 已在收藏夹中`);
            }
        },
        
        // 获取收藏夹
        getFavorites() {
            return JSON.parse(localStorage.getItem('biomedFavorites') || '[]');
        },
        
        // 从收藏夹移除
        removeFromFavorites(siteId) {
            const favorites = this.getFavorites();
            const filteredFavorites = favorites.filter(fav => fav.id !== siteId);
            localStorage.setItem('biomedFavorites', JSON.stringify(filteredFavorites));
            this.$message.success('已从收藏夹移除');
        }
    }
});

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 添加页面加载动画
    const cards = document.querySelectorAll('.category-card, .site-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // 添加滚动效果
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.header');
        if (window.scrollY > 100) {
            header.style.backgroundColor = 'rgba(102, 126, 234, 0.95)';
        } else {
            header.style.backgroundColor = '';
        }
    });
    
    // SEO优化：添加结构化数据
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "生物医学导航 - BioMed Navigator",
        "description": "专业的生物医学资源导航网站，提供最全面的生物医学、生物信息学、医学研究资源导航和工具集合",
        "url": window.location.href,
        "potentialAction": {
            "@type": "SearchAction",
            "target": window.location.href + "?search={search_term_string}",
            "query-input": "required name=search_term_string"
        }
    };
    
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(structuredData);
    document.head.appendChild(script);
});

// Google Analytics 集成准备（需要替换为实际的GA ID）
// gtag('config', 'GA_MEASUREMENT_ID');

// 错误处理
window.addEventListener('error', function(e) {
    console.error('页面错误:', e.error);
}); 