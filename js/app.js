// 生物医学导航网站 JavaScript
// 原生JavaScript实现，无需外部框架依赖

class BioMedNavigator {
    constructor() {
        this.hospitalData = null;
        this.init();
    }

    init() {
        this.setupSearchFunctionality();
        this.setupLinkTracking();
        this.setupKeyboardShortcuts();
        this.addLoadingAnimations();
        this.initializeFavorites();
        this.initializeHospitalRanking();
        this.initializeUserIdentity();
        this.setupDepartmentFilter();
    }

    // 初始化华南专科医院排行榜功能
    async initializeHospitalRanking() {
        try {
            await this.loadHospitalData();
            this.setupHospitalMoreLinks();
        } catch (error) {
            console.error('加载医院数据失败:', error);
        }
    }

    // 加载医院排行榜数据
    async loadHospitalData() {
        try {
            const response = await fetch('华南专科医院排行榜.csv');
            const csvText = await response.text();
            this.hospitalData = this.parseCSV(csvText);
            console.log('医院数据加载成功:', this.hospitalData);
        } catch (error) {
            console.error('无法加载医院数据:', error);
            // 使用内置数据作为备用
            this.hospitalData = this.getBackupHospitalData();
        }
    }

    // 解析CSV数据
    parseCSV(csvText) {
        const lines = csvText.split('\n').filter(line => line.trim());
        const headers = lines[0].split(',');
        const data = {};

        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(',');
            if (values.length >= 3) {
                const department = values[0].trim();
                const rank = values[1].trim();
                const hospital = values[2].trim();
                const url = values[3] ? values[3].trim() : '';

                if (!data[department]) {
                    data[department] = [];
                }

                data[department].push({
                    rank: rank,
                    hospital: hospital,
                    url: url
                });
            }
        }

        return data;
    }

    // 备用医院数据（从CSV中提取的主要科室）
    getBackupHospitalData() {
        return {
            "病理科": [
                {rank: "1", hospital: "南方医科大学南方医院", url: "https://www.nfyy.com/"},
                {rank: "2", hospital: "中山大学附属第一医院", url: "https://www.gzsums.net/"},
                {rank: "3", hospital: "中山大学肿瘤防治中心", url: "https://www.sysucc.org.cn/"},
                {rank: "4", hospital: "广东省人民医院", url: "https://www.gdghospital.org.cn/"},
                {rank: "5", hospital: "广西医科大学第一附属医院", url: "https://www.gxmuyfy.cn/"}
            ],
            "心血管": [
                {rank: "1", hospital: "广东省人民医院", url: "https://www.gdghospital.org.cn/"},
                {rank: "2", hospital: "中山大学附属第一医院", url: "https://www.gzsums.net/"},
                {rank: "3", hospital: "南方医科大学南方医院", url: "https://www.nfyy.com/"},
                {rank: "4", hospital: "广西医科大学第一附属医院", url: "https://www.gxmuyfy.cn/"},
                {rank: "5", hospital: "中山大学孙逸仙纪念医院", url: "https://www.syshospital.com/"}
            ],
            "肿瘤学": [
                {rank: "1", hospital: "中山大学肿瘤防治中心", url: "https://www.sysucc.org.cn/"},
                {rank: "2", hospital: "广东省人民医院", url: "https://www.gdghospital.org.cn/"},
                {rank: "3", hospital: "广西医科大学附属肿瘤医院", url: ""},
                {rank: "4", hospital: "南方医科大学南方医院", url: "https://www.nfyy.com/"},
                {rank: "5", hospital: "中山大学附属第一医院", url: "https://www.gzsums.net/"}
            ]
        };
    }

    // 设置医院排行榜的"更多"链接功能
    setupHospitalMoreLinks() {
        const hospitalSection = document.querySelector('.nav-section h2 .title-text');
        if (hospitalSection && hospitalSection.textContent.includes('华南专科医院排行榜')) {
            const moreLink = hospitalSection.parentElement.querySelector('.more-link');
            if (moreLink) {
                moreLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.showHospitalRankingModal();
                });
            }
        }
    }

    // 显示医院排行榜模态框
    showHospitalRankingModal() {
        const modal = this.createHospitalModal();
        document.body.appendChild(modal);
        
        // 添加显示动画
        setTimeout(() => {
            modal.style.opacity = '1';
            modal.querySelector('.hospital-modal-content').style.transform = 'translate(-50%, -50%) scale(1)';
        }, 10);
    }

    // 创建医院排行榜模态框
    createHospitalModal() {
        const modal = document.createElement('div');
        modal.className = 'hospital-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        const modalContent = document.createElement('div');
        modalContent.className = 'hospital-modal-content';
        modalContent.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.9);
            background: white;
            border-radius: 12px;
            width: 90%;
            max-width: 1200px;
            max-height: 80vh;
            overflow-y: auto;
            padding: 0;
            transition: transform 0.3s ease;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        `;

        // 创建模态框头部
        const header = document.createElement('div');
        header.style.cssText = `
            position: sticky;
            top: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 12px 12px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1;
        `;

        const title = document.createElement('h2');
        title.textContent = '华南专科医院排行榜';
        title.style.cssText = `
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        `;

        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            background: none;
            border: none;
            color: white;
            font-size: 32px;
            cursor: pointer;
            padding: 0;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.3s ease;
        `;

        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.background = 'rgba(255, 255, 255, 0.2)';
        });

        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.background = 'none';
        });

        closeBtn.addEventListener('click', () => {
            this.closeHospitalModal(modal);
        });

        header.appendChild(title);
        header.appendChild(closeBtn);

        // 创建内容区域
        const content = document.createElement('div');
        content.style.cssText = `
            padding: 30px;
        `;

        // 创建科室选择器
        const departmentSelector = this.createDepartmentSelector();
        content.appendChild(departmentSelector);

        // 创建医院列表容器
        const hospitalList = document.createElement('div');
        hospitalList.className = 'hospital-list';
        hospitalList.style.cssText = `
            margin-top: 20px;
        `;
        content.appendChild(hospitalList);

        modalContent.appendChild(header);
        modalContent.appendChild(content);
        modal.appendChild(modalContent);

        // 默认显示第一个科室
        const firstDepartment = Object.keys(this.hospitalData)[0];
        if (firstDepartment) {
            this.displayDepartmentHospitals(firstDepartment, hospitalList);
        }

        // 点击模态框外部关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeHospitalModal(modal);
            }
        });

        return modal;
    }

    // 创建科室选择器
    createDepartmentSelector() {
        const container = document.createElement('div');
        container.style.cssText = `
            margin-bottom: 20px;
        `;

        const label = document.createElement('label');
        label.textContent = '选择科室：';
        label.style.cssText = `
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
            font-size: 16px;
        `;

        const select = document.createElement('select');
        select.style.cssText = `
            width: 100%;
            max-width: 300px;
            padding: 12px 16px;
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s ease;
        `;

        select.addEventListener('focus', () => {
            select.style.borderColor = '#667eea';
        });

        select.addEventListener('blur', () => {
            select.style.borderColor = '#e1e5e9';
        });

        // 添加科室选项
        Object.keys(this.hospitalData).forEach(department => {
            const option = document.createElement('option');
            option.value = department;
            option.textContent = department;
            select.appendChild(option);
        });

        // 选择事件
        select.addEventListener('change', (e) => {
            const hospitalList = document.querySelector('.hospital-list');
            this.displayDepartmentHospitals(e.target.value, hospitalList);
        });

        container.appendChild(label);
        container.appendChild(select);
        return container;
    }

    // 显示指定科室的医院列表
    displayDepartmentHospitals(department, container) {
        const hospitals = this.hospitalData[department] || [];
        
        container.innerHTML = '';

        if (hospitals.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #666; font-size: 16px; padding: 40px;">暂无该科室的医院数据</p>';
            return;
        }

        // 创建科室标题
        const departmentTitle = document.createElement('h3');
        departmentTitle.textContent = `${department} 专科排名`;
        departmentTitle.style.cssText = `
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        `;
        container.appendChild(departmentTitle);

        // 创建医院网格
        const hospitalGrid = document.createElement('div');
        hospitalGrid.style.cssText = `
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 16px;
            margin-top: 20px;
        `;

        hospitals.forEach((hospital, index) => {
            const hospitalCard = this.createHospitalCard(hospital, index);
            hospitalGrid.appendChild(hospitalCard);
        });

        container.appendChild(hospitalGrid);
    }

    // 创建医院卡片
    createHospitalCard(hospital, index) {
        const card = document.createElement('div');
        const isRanked = hospital.rank !== '获提名医院';
        const rankColor = isRanked ? this.getRankColor(hospital.rank) : '#95a5a6';
        
        card.style.cssText = `
            background: white;
            border: 2px solid #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: ${hospital.url ? 'pointer' : 'default'};
            position: relative;
            overflow: hidden;
        `;

        // 悬停效果
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
            card.style.borderColor = '#667eea';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = 'none';
            card.style.borderColor = '#f8f9fa';
        });

        // 排名标识
        const rankBadge = document.createElement('div');
        rankBadge.textContent = isRanked ? `第${hospital.rank}名` : '获提名';
        rankBadge.style.cssText = `
            position: absolute;
            top: 15px;
            right: 15px;
            background: ${rankColor};
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        `;

        // 医院名称
        const hospitalName = document.createElement('h4');
        hospitalName.textContent = hospital.hospital;
        hospitalName.style.cssText = `
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 18px;
            font-weight: 600;
            line-height: 1.4;
            padding-right: 80px;
        `;

        // 链接指示器
        if (hospital.url) {
            const linkIcon = document.createElement('div');
            linkIcon.innerHTML = '🔗';
            linkIcon.style.cssText = `
                position: absolute;
                bottom: 15px;
                right: 15px;
                font-size: 16px;
                opacity: 0.6;
            `;
            card.appendChild(linkIcon);

            // 点击事件
            card.addEventListener('click', () => {
                window.open(hospital.url, '_blank');
                this.trackLinkClick(hospital.hospital, hospital.url);
            });
        }

        card.appendChild(rankBadge);
        card.appendChild(hospitalName);

        return card;
    }

    // 获取排名颜色
    getRankColor(rank) {
        const rankNum = parseInt(rank);
        if (rankNum === 1) return '#f39c12'; // 金色
        if (rankNum === 2) return '#95a5a6'; // 银色
        if (rankNum === 3) return '#cd7f32'; // 铜色
        if (rankNum <= 5) return '#3498db'; // 蓝色
        return '#2ecc71'; // 绿色
    }

    // 关闭医院模态框
    closeHospitalModal(modal) {
        modal.style.opacity = '0';
        modal.querySelector('.hospital-modal-content').style.transform = 'translate(-50%, -50%) scale(0.9)';
        
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        }, 300);
    }

    // 搜索功能
    setupSearchFunctionality() {
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');

        if (searchInput && searchBtn) {
            // 搜索按钮点击事件
            searchBtn.addEventListener('click', () => {
                this.performSearch();
            });

            // 回车键搜索
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch();
                }
            });

            // 搜索建议（可选功能）
            searchInput.addEventListener('input', (e) => {
                this.showSearchSuggestions(e.target.value);
            });
        }
    }

    // 执行搜索
    performSearch() {
        const searchInput = document.getElementById('searchInput');
        const query = searchInput.value.trim();
        
        if (!query) {
            this.showMessage('请输入搜索关键词', 'warning');
            return;
        }

        // 智能搜索重定向
        const searchUrls = {
            'pubmed': 'https://pubmed.ncbi.nlm.nih.gov/?term=',
            'ncbi': 'https://www.ncbi.nlm.nih.gov/search/all/?term=',
            'scholar': 'https://scholar.google.com/scholar?q=',
            'who': 'https://www.who.int/search?query=',
            'mayo': 'https://www.mayoclinic.org/search/search-results?q=',
            'harvard': 'https://news.harvard.edu/search/?s=',
            'nature': 'https://www.nature.com/search?q=',
            'cell': 'https://www.cell.com/action/doSearch?searchText=',
            'lancet': 'https://www.thelancet.com/search?q='
        };

        // 检查是否是特定网站搜索
        const lowerQuery = query.toLowerCase();
        for (const [site, url] of Object.entries(searchUrls)) {
            if (lowerQuery.includes(site)) {
                const searchTerm = query.replace(new RegExp(site, 'i'), '').trim();
                window.open(url + encodeURIComponent(searchTerm || query), '_blank');
                this.trackSearch(site, searchTerm || query);
                return;
            }
        }

        // 默认使用PubMed搜索
        window.open(`https://pubmed.ncbi.nlm.nih.gov/?term=${encodeURIComponent(query)}`, '_blank');
        this.trackSearch('pubmed', query);
    }

    // 搜索建议
    showSearchSuggestions(query) {
        if (!query || query.length < 2) return;

        const suggestions = [
            'COVID-19 vaccine',
            'CRISPR gene editing',
            'Alzheimer disease',
            'cancer therapy',
            'diabetes treatment',
            'machine learning medicine',
            'biomarker discovery',
            'clinical trial',
            'precision medicine',
            'immunotherapy'
        ];

        const filtered = suggestions.filter(s => 
            s.toLowerCase().includes(query.toLowerCase())
        );

        // 这里可以实现搜索建议下拉框
        // 由于是简化版本，暂时只在控制台输出
        if (filtered.length > 0) {
            console.log('搜索建议:', filtered);
        }
    }

    // 链接点击跟踪
    setupLinkTracking() {
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const siteName = link.querySelector('.link-text')?.textContent;
                const url = link.href;
                
                // 跟踪点击统计
                this.trackLinkClick(siteName, url);
                
                // 添加点击反馈效果
                this.addClickFeedback(link);
            });
        });
    }

    // 键盘快捷键
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+K 或 Cmd+K 聚焦搜索框
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.getElementById('searchInput');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }

            // ESC 键清空搜索框
            if (e.key === 'Escape') {
                const searchInput = document.getElementById('searchInput');
                if (searchInput && searchInput === document.activeElement) {
                    searchInput.value = '';
                    searchInput.blur();
                }
            }
        });
    }

    // 加载动画
    addLoadingAnimations() {
        const sections = document.querySelectorAll('.nav-section');
        
        // 使用 Intersection Observer 实现滚动动画
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeIn 0.6s ease-out';
                }
            });
        }, { threshold: 0.1 });

        sections.forEach(section => {
            observer.observe(section);
        });
    }

    // 收藏功能
    initializeFavorites() {
        this.favorites = this.loadFavorites();
        this.addFavoriteButtons();
    }

    loadFavorites() {
        try {
            return JSON.parse(localStorage.getItem('biomedFavorites') || '[]');
        } catch {
            return [];
        }
    }

    saveFavorites() {
        try {
            localStorage.setItem('biomedFavorites', JSON.stringify(this.favorites));
        } catch (e) {
            console.warn('无法保存收藏:', e);
        }
    }

    addFavoriteButtons() {
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const url = link.href;
            const name = link.querySelector('.link-text')?.textContent;
            
            if (url && name) {
                const isFavorited = this.favorites.some(fav => fav.url === url);
                
                // 添加收藏按钮（鼠标悬停时显示）
                link.addEventListener('mouseenter', () => {
                    this.showFavoriteButton(link, { url, name }, isFavorited);
                });
                
                link.addEventListener('mouseleave', () => {
                    this.hideFavoriteButton(link);
                });
            }
        });
    }

    showFavoriteButton(linkElement, item, isFavorited) {
        // 避免重复添加
        if (linkElement.querySelector('.favorite-btn')) return;

        const favoriteBtn = document.createElement('span');
        favoriteBtn.className = 'favorite-btn';
        favoriteBtn.innerHTML = isFavorited ? '⭐' : '☆';
        favoriteBtn.style.cssText = `
            position: absolute;
            right: 5px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            font-size: 12px;
            opacity: 0.7;
            transition: opacity 0.3s;
        `;
        
        favoriteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleFavorite(item, favoriteBtn);
        });

        linkElement.style.position = 'relative';
        linkElement.appendChild(favoriteBtn);
    }

    hideFavoriteButton(linkElement) {
        const favoriteBtn = linkElement.querySelector('.favorite-btn');
        if (favoriteBtn) {
            favoriteBtn.remove();
        }
    }

    toggleFavorite(item, buttonElement) {
        const index = this.favorites.findIndex(fav => fav.url === item.url);
        
        if (index > -1) {
            // 取消收藏
            this.favorites.splice(index, 1);
            buttonElement.innerHTML = '☆';
            this.showMessage(`已取消收藏 ${item.name}`, 'info');
        } else {
            // 添加收藏
            this.favorites.push({
                ...item,
                addedAt: new Date().toISOString()
            });
            buttonElement.innerHTML = '⭐';
            this.showMessage(`已收藏 ${item.name}`, 'success');
        }
        
        this.saveFavorites();
    }

    // 点击反馈效果
    addClickFeedback(element) {
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);
    }

    // 消息提示
    showMessage(message, type = 'info') {
        // 创建消息元素
        const messageEl = document.createElement('div');
        messageEl.className = `message message-${type}`;
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-size: 14px;
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        // 设置颜色
        const colors = {
            info: '#3498db',
            success: '#2ecc71',
            warning: '#f39c12',
            error: '#e74c3c'
        };
        messageEl.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(messageEl);

        // 显示动画
        setTimeout(() => {
            messageEl.style.transform = 'translateX(0)';
        }, 100);

        // 自动隐藏
        setTimeout(() => {
            messageEl.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, 3000);
    }

    // 统计跟踪
    trackSearch(site, query) {
        try {
            const stats = JSON.parse(localStorage.getItem('biomedStats') || '{}');
            stats.searches = stats.searches || {};
            stats.searches[site] = (stats.searches[site] || 0) + 1;
            stats.lastSearch = {
                site,
                query,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('biomedStats', JSON.stringify(stats));
        } catch (e) {
            console.warn('统计跟踪失败:', e);
        }
    }

    trackLinkClick(siteName, url) {
        try {
            const stats = JSON.parse(localStorage.getItem('biomedStats') || '{}');
            stats.clicks = stats.clicks || {};
            stats.clicks[siteName] = (stats.clicks[siteName] || 0) + 1;
            stats.lastClick = {
                siteName,
                url,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('biomedStats', JSON.stringify(stats));
        } catch (e) {
            console.warn('统计跟踪失败:', e);
        }
    }

    // 获取使用统计
    getStats() {
        try {
            return JSON.parse(localStorage.getItem('biomedStats') || '{}');
        } catch {
            return {};
        }
    }

    // 初始化用户身份管理
    initializeUserIdentity() {
        this.currentIdentity = this.loadUserIdentity();
        this.setupIdentityBanner();
        this.setupIdentitySelection();
        
        if (this.currentIdentity) {
            this.hideIdentityBanner();
            this.showCurrentIdentity();
            this.showPersonalizedRecommendations();
        }
    }

    // 加载用户身份
    loadUserIdentity() {
        try {
            return localStorage.getItem('userIdentity');
        } catch {
            return null;
        }
    }

    // 保存用户身份
    saveUserIdentity(identity) {
        try {
            localStorage.setItem('userIdentity', identity);
            this.currentIdentity = identity;
        } catch (e) {
            console.warn('无法保存用户身份:', e);
        }
    }

    // 设置身份选择横幅
    setupIdentityBanner() {
        const closeBanner = document.getElementById('closeBanner');
        const identityBtns = document.querySelectorAll('.identity-btn');

        if (closeBanner) {
            closeBanner.addEventListener('click', () => {
                this.hideIdentityBanner();
            });
        }

        identityBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const identity = btn.dataset.identity;
                this.selectIdentity(identity);
            });
        });
    }

    // 设置身份切换功能
    setupIdentitySelection() {
        const changeIdentityBtn = document.getElementById('changeIdentity');
        if (changeIdentityBtn) {
            changeIdentityBtn.addEventListener('click', () => {
                this.showIdentityBanner();
            });
        }
    }

    // 选择身份
    selectIdentity(identity) {
        // 更新按钮状态
        document.querySelectorAll('.identity-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        document.querySelector(`[data-identity="${identity}"]`).classList.add('selected');

        // 保存身份
        this.saveUserIdentity(identity);

        // 延迟隐藏横幅和显示个性化内容
        setTimeout(() => {
            this.hideIdentityBanner();
            this.showCurrentIdentity();
            this.showPersonalizedRecommendations();
        }, 1000);

        this.showMessage(`已切换到${this.getIdentityName(identity)}模式`, 'success');
    }

    // 获取身份名称
    getIdentityName(identity) {
        const names = {
            student: '学生',
            researcher: '研究员',
            enthusiast: '爱好者',
            patient: '患者'
        };
        return names[identity] || identity;
    }

    // 获取身份图标
    getIdentityIcon(identity) {
        const icons = {
            student: '🎓',
            researcher: '🔬',
            enthusiast: '💡',
            patient: '🏥'
        };
        return icons[identity] || '👤';
    }

    // 隐藏身份横幅
    hideIdentityBanner() {
        const banner = document.getElementById('identityBanner');
        if (banner) {
            banner.style.transform = 'translateY(-100%)';
            setTimeout(() => {
                banner.style.display = 'none';
            }, 300);
        }
    }

    // 显示身份横幅
    showIdentityBanner() {
        const banner = document.getElementById('identityBanner');
        if (banner) {
            banner.style.display = 'block';
            setTimeout(() => {
                banner.style.transform = 'translateY(0)';
            }, 10);
        }
    }

    // 显示当前身份
    showCurrentIdentity() {
        const currentIdentityEl = document.getElementById('currentIdentity');
        const iconEl = currentIdentityEl?.querySelector('.identity-icon-current');
        const textEl = currentIdentityEl?.querySelector('.identity-text-current');

        if (currentIdentityEl && this.currentIdentity) {
            iconEl.textContent = this.getIdentityIcon(this.currentIdentity);
            textEl.textContent = this.getIdentityName(this.currentIdentity);
            currentIdentityEl.style.display = 'flex';
        }
    }

    // 显示个性化推荐
    showPersonalizedRecommendations() {
        const personalizedSection = document.getElementById('personalizedSection');
        const recommendationGrid = document.getElementById('recommendationGrid');

        if (personalizedSection && this.currentIdentity) {
            const recommendations = this.getRecommendationsByIdentity(this.currentIdentity);
            recommendationGrid.innerHTML = '';

            recommendations.forEach(rec => {
                const card = this.createRecommendationCard(rec);
                recommendationGrid.appendChild(card);
            });

            personalizedSection.style.display = 'block';
            setTimeout(() => {
                personalizedSection.style.opacity = '1';
            }, 100);
        }
    }

    // 根据身份获取推荐内容
    getRecommendationsByIdentity(identity) {
        const recommendations = {
            student: [
                {
                    title: '医学教学资源',
                    description: '权威的医学教材和学习资料',
                    links: [
                        { name: 'PubMed Student', url: 'https://pubmed.ncbi.nlm.nih.gov/' },
                        { name: 'Medical Education', url: 'https://www.aamc.org/' }
                    ]
                },
                {
                    title: '实习医院推荐',
                    description: '优质的实习机会和临床学习',
                    links: [
                        { name: '华南实习医院', url: '#' },
                        { name: '临床技能培训', url: '#' }
                    ]
                }
            ],
            researcher: [
                {
                    title: '前沿研究动态',
                    description: '最新的生物医学研究进展',
                    links: [
                        { name: 'Nature Medicine', url: 'https://www.nature.com/nm/' },
                        { name: 'Cell Research', url: 'https://www.nature.com/cr/' }
                    ]
                },
                {
                    title: '研究工具平台',
                    description: '生物信息学分析工具',
                    links: [
                        { name: 'NCBI Tools', url: 'https://www.ncbi.nlm.nih.gov/tools/' },
                        { name: 'Bioconductor', url: 'https://bioconductor.org/' }
                    ]
                }
            ],
            enthusiast: [
                {
                    title: '科普知识',
                    description: '通俗易懂的医学科普内容',
                    links: [
                        { name: 'Mayo Clinic Health', url: 'https://www.mayoclinic.org/healthy-lifestyle' },
                        { name: 'WebMD', url: 'https://www.webmd.com/' }
                    ]
                },
                {
                    title: '健康资讯',
                    description: '最新的健康研究和医疗进展',
                    links: [
                        { name: 'Harvard Health', url: 'https://www.health.harvard.edu/' },
                        { name: 'WHO Health Topics', url: 'https://www.who.int/health-topics' }
                    ]
                }
            ],
            patient: [
                {
                    title: '疾病查询',
                    description: '权威的疾病信息和治疗指南',
                    links: [
                        { name: 'Mayo Clinic Diseases', url: 'https://www.mayoclinic.org/diseases-conditions' },
                        { name: 'MedlinePlus', url: 'https://medlineplus.gov/' }
                    ]
                },
                {
                    title: '就医指导',
                    description: '医院选择和就诊流程指导',
                    links: [
                        { name: '华南专科医院', url: '#' },
                        { name: '预约挂号指南', url: '#' }
                    ]
                }
            ]
        };

        return recommendations[identity] || [];
    }

    // 创建推荐卡片
    createRecommendationCard(recommendation) {
        const card = document.createElement('div');
        card.className = 'recommendation-card';

        const title = document.createElement('h4');
        title.textContent = recommendation.title;
        title.style.cssText = `
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        `;

        const description = document.createElement('p');
        description.textContent = recommendation.description;
        description.style.cssText = `
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 15px;
            line-height: 1.5;
        `;

        const linksContainer = document.createElement('div');
        linksContainer.style.cssText = `
            display: flex;
            flex-direction: column;
            gap: 8px;
        `;

        recommendation.links.forEach(link => {
            const linkEl = document.createElement('a');
            linkEl.href = link.url;
            linkEl.target = '_blank';
            linkEl.textContent = link.name;
            linkEl.style.cssText = `
                color: #667eea;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
                padding: 6px 12px;
                border-radius: 15px;
                border: 1px solid rgba(102, 126, 234, 0.3);
                transition: all 0.3s ease;
                text-align: center;
            `;

            linkEl.addEventListener('mouseenter', () => {
                linkEl.style.background = '#667eea';
                linkEl.style.color = 'white';
            });

            linkEl.addEventListener('mouseleave', () => {
                linkEl.style.background = 'transparent';
                linkEl.style.color = '#667eea';
            });

            linksContainer.appendChild(linkEl);
        });

        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(linksContainer);

        return card;
    }

    // 设置科室筛选功能
    setupDepartmentFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const hospitalGrid = document.getElementById('hospitalLinksGrid');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // 更新按钮状态
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const department = btn.dataset.department;
                this.filterHospitalsByDepartment(department, hospitalGrid);
            });
        });
    }

    // 根据科室筛选医院
    filterHospitalsByDepartment(department, container) {
        const allLinks = container.querySelectorAll('.nav-link');
        
        if (department === 'all') {
            // 显示所有医院
            allLinks.forEach(link => {
                link.style.display = 'flex';
            });
        } else {
            // 根据科室筛选（这里需要根据实际数据结构调整）
            allLinks.forEach(link => {
                const hospitalName = link.querySelector('.link-text').textContent;
                const badge = link.querySelector('.hospital-badge').textContent;
                
                // 简单的筛选逻辑，实际应该基于医院数据
                const shouldShow = badge.includes(department) || 
                                 this.isHospitalInDepartment(hospitalName, department);
                
                link.style.display = shouldShow ? 'flex' : 'none';
            });
        }

        // 添加筛选动画
        container.style.opacity = '0.5';
        setTimeout(() => {
            container.style.opacity = '1';
        }, 200);
    }

    // 判断医院是否在指定科室中排名靠前
    isHospitalInDepartment(hospitalName, department) {
        // 这里应该基于实际的医院数据进行判断
        // 简化的判断逻辑
        const departmentHospitals = {
            '心血管': ['广东省人民医院', '中山大学附属第一医院', '南方医科大学南方医院'],
            '肿瘤学': ['中山大学肿瘤防治中心', '广东省人民医院', '南方医科大学南方医院'],
            '神经外科': ['南方医科大学南方医院', '中山大学附属第一医院'],
            '骨科': ['南方医科大学南方医院', '中山大学附属第一医院', '中山大学孙逸仙纪念医院'],
            '呼吸科': ['广州医科大学附属第一医院', '中山大学附属第一医院', '南方医科大学南方医院'],
            '消化病': ['中山大学附属第一医院', '南方医科大学南方医院'],
            '泌尿外科': ['中山大学孙逸仙纪念医院', '中山大学附属第一医院', '广州医科大学附属第一医院']
        };

        return departmentHospitals[department]?.some(name => hospitalName.includes(name)) || false;
    }
}

// 实用工具函数
const utils = {
    // 复制到剪贴板
    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                navigator.showMessage('已复制到剪贴板', 'success');
            });
        } else {
            // 降级处理
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                navigator.showMessage('已复制到剪贴板', 'success');
            } catch (e) {
                navigator.showMessage('复制失败', 'error');
            }
            document.body.removeChild(textArea);
        }
    },

    // 格式化日期
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    // 初始化导航器
    window.navigator = new BioMedNavigator();
    
    // 绑定工具函数到全局
    window.utils = utils;
    
    // 添加页面加载完成的视觉反馈
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
    
    console.log('🧬 生物医学导航网站已加载完成');
    console.log('💡 按 Ctrl+K (或 Cmd+K) 快速搜索');
    console.log('📊 使用 navigator.getStats() 查看使用统计');
});

// 导出到全局（用于调试）
if (typeof window !== 'undefined') {
    window.BioMedNavigator = BioMedNavigator;
} 