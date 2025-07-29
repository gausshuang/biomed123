// 生物医学导航网站 JavaScript
// 原生JavaScript实现，无需外部框架依赖

class BioMedNavigator {
    constructor() {
        this.hospitalData = null;
        this.currentView = 'department'; // 'department' 或 'list'
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.setupSearchFunctionality();
        this.setupLinkTracking();
        this.setupKeyboardShortcuts();
        this.addLoadingAnimations();
        this.initializeFavorites();
        this.initializeHospitalRanking();
    }

    // 初始化华南专科医院排行榜功能
    async initializeHospitalRanking() {
        try {
            await this.loadHospitalData();
            this.setupHospitalControls();
            this.setupDepartmentFilter();
            this.displayHospitalData();
        } catch (error) {
            console.error('加载医院数据失败:', error);
            this.showMessage('医院数据加载失败，请刷新页面重试', 'error');
        }
    }

    // 加载医院排行榜数据
    async loadHospitalData() {
        try {
            // 尝试加载完整的医院数据
            const response = await fetch('complete_hospitals_data.json');
            if (response.ok) {
                const jsonData = await response.text();
                this.hospitalData = JSON.parse(jsonData);
                console.log('完整医院数据加载成功:', Object.keys(this.hospitalData).length, '个科室');
                return;
            }
        } catch (error) {
            console.log('无法加载完整医院数据，尝试备用数据源:', error);
        }
        
        try {
            // 备用：尝试加载华南区数据
            const response = await fetch('华南专科医院排行榜.csv');
            const csvText = await response.text();
            this.hospitalData = this.parseCSV(csvText);
            console.log('华南区医院数据加载成功:', this.hospitalData);
        } catch (error) {
            console.error('无法加载医院数据:', error);
            // 使用内置数据作为最后备用
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

    // 备用医院数据
    getBackupHospitalData() {
        return {
            "病理科": [
                {rank: "1", hospital: "南方医科大学南方医院", url: "https://www.nfyy.com/"},
                {rank: "2", hospital: "中山大学附属第一医院", url: "https://www.gzsums.net/"},
                {rank: "3", hospital: "中山大学肿瘤防治中心", url: "https://www.sysucc.org.cn/"},
                {rank: "4", hospital: "广东省人民医院", url: "https://www.gdghospital.org.cn/"},
                {rank: "5", hospital: "广西医科大学第一附属医院", url: "https://www.gxmuyfy.cn/"}
            ]
        };
    }

    // 设置医院控制按钮
    setupHospitalControls() {
        const viewToggleBtn = document.getElementById('viewToggleBtn');
        const hospitalMoreLink = document.getElementById('hospitalMoreLink');

        if (viewToggleBtn) {
            viewToggleBtn.addEventListener('click', () => {
                this.toggleView();
            });
        }

        if (hospitalMoreLink) {
            hospitalMoreLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.showHospitalRankingModal();
            });
        }
    }

    // 切换视图
    toggleView() {
        this.currentView = this.currentView === 'department' ? 'list' : 'department';
        const viewToggleBtn = document.getElementById('viewToggleBtn');
        
        if (viewToggleBtn) {
            viewToggleBtn.textContent = this.currentView === 'department' ? '列表视图' : '科室视图';
        }
        
        this.displayHospitalData();
        this.showMessage(`已切换到${this.currentView === 'department' ? '科室' : '列表'}视图`, 'info');
    }

    // 设置科室筛选功能
    setupDepartmentFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');

        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // 更新按钮状态
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                this.currentFilter = btn.dataset.department;
                this.displayHospitalData();
            });
        });
    }

    // 显示医院数据
    displayHospitalData() {
        const displayArea = document.getElementById('hospitalDisplayArea');
        if (!displayArea || !this.hospitalData) return;

        displayArea.innerHTML = '';

        if (this.currentView === 'department') {
            this.displayByDepartment(displayArea);
        } else {
            this.displayByList(displayArea);
        }
    }

    // 按科室分组显示
    displayByDepartment(container) {
        const departments = this.currentFilter === 'all' 
            ? Object.keys(this.hospitalData) 
            : Object.keys(this.hospitalData).filter(dept => 
                dept.includes(this.currentFilter) || this.currentFilter === 'all'
            );

        departments.forEach(department => {
            const hospitals = this.hospitalData[department];
            if (!hospitals || hospitals.length === 0) return;

            const departmentGroup = document.createElement('div');
            departmentGroup.className = 'department-group';

            const departmentTitle = document.createElement('h3');
            departmentTitle.className = 'department-title';
            departmentTitle.innerHTML = `
                <span>${this.getDepartmentIcon(department)}</span>
                <span>${department}</span>
            `;

            const departmentStats = document.createElement('div');
            departmentStats.className = 'department-stats';
            const rankedCount = hospitals.filter(h => h.rank !== '获提名医院').length;
            const nominatedCount = hospitals.filter(h => h.rank === '获提名医院').length;
            departmentStats.textContent = `排名医院 ${rankedCount} 家，获提名医院 ${nominatedCount} 家`;

            departmentGroup.appendChild(departmentTitle);
            departmentGroup.appendChild(departmentStats);

            // 按排名排序
            const sortedHospitals = [...hospitals].sort((a, b) => {
                if (a.rank === '获提名医院' && b.rank !== '获提名医院') return 1;
                if (a.rank !== '获提名医院' && b.rank === '获提名医院') return -1;
                if (a.rank === '获提名医院' && b.rank === '获提名医院') return 0;
                return parseInt(a.rank) - parseInt(b.rank);
            });

            sortedHospitals.forEach(hospital => {
                const hospitalCard = this.createHospitalCard(hospital, department);
                departmentGroup.appendChild(hospitalCard);
            });

            container.appendChild(departmentGroup);
        });
    }

    // 按列表显示
    displayByList(container) {
        const allHospitals = [];
        
        Object.keys(this.hospitalData).forEach(department => {
            if (this.currentFilter === 'all' || department.includes(this.currentFilter)) {
                this.hospitalData[department].forEach(hospital => {
                    allHospitals.push({
                        ...hospital,
                        department: department
                    });
                });
            }
        });

        // 按医院名称排序
        allHospitals.sort((a, b) => a.hospital.localeCompare(b.hospital, 'zh-CN'));

        allHospitals.forEach(hospital => {
            const hospitalCard = this.createHospitalCard(hospital, hospital.department);
            container.appendChild(hospitalCard);
        });
    }

    // 创建医院卡片
    createHospitalCard(hospital, department) {
        const card = document.createElement('div');
        const isRanked = hospital.rank !== '获提名医院' && hospital.rank !== '获提名';
        const rankNum = isRanked ? parseInt(hospital.rank) : 0;
        
        card.className = 'hospital-card';
        if (rankNum <= 3 && isRanked) {
            card.classList.add('top-rank');
        } else if (!isRanked) {
            card.classList.add('nominated');
        }

        // 排名标识
        const rankBadge = document.createElement('div');
        rankBadge.className = 'hospital-rank';
        if (isRanked) {
            rankBadge.textContent = `第${hospital.rank}名`;
            if (rankNum === 1) rankBadge.classList.add('rank-1');
            else if (rankNum === 2) rankBadge.classList.add('rank-2');
            else if (rankNum === 3) rankBadge.classList.add('rank-3');
        } else {
            rankBadge.textContent = '获提名';
            rankBadge.classList.add('nominated');
        }

        // 医院名称
        const hospitalName = document.createElement('div');
        hospitalName.className = 'hospital-name';
        hospitalName.textContent = hospital.hospital;

        // 科室信息
        const hospitalDepartment = document.createElement('div');
        hospitalDepartment.className = 'hospital-department';
        hospitalDepartment.textContent = `${department}专科`;

        // 地理位置信息
        const locationInfo = document.createElement('div');
        locationInfo.className = 'hospital-location';
        let locationText = '';
        
        if (hospital.region) {
            locationText += hospital.region;
        }
        if (hospital.province && hospital.province !== hospital.region) {
            locationText += (locationText ? ' · ' : '') + hospital.province;
        }
        if (hospital.city && hospital.city !== hospital.province) {
            locationText += (locationText ? ' · ' : '') + hospital.city;
        }
        
        if (locationText) {
            locationInfo.textContent = `📍 ${locationText}`;
        } else {
            locationInfo.textContent = '📍 位置信息待完善';
            locationInfo.style.color = '#999';
        }

        // 官网链接
        const hospitalUrl = document.createElement('a');
        hospitalUrl.className = 'hospital-url';
        
        if (hospital.url && hospital.url.trim() && hospital.url !== 'nan') {
            hospitalUrl.href = hospital.url;
            hospitalUrl.target = '_blank';
            hospitalUrl.textContent = '🌐 访问官网';
            hospitalUrl.addEventListener('click', () => {
                this.trackLinkClick(hospital.hospital, hospital.url);
            });
        } else {
            hospitalUrl.href = '#';
            hospitalUrl.textContent = '🌐 暂无官网';
            hospitalUrl.style.color = '#999';
            hospitalUrl.style.cursor = 'not-allowed';
            hospitalUrl.addEventListener('click', (e) => {
                e.preventDefault();
            });
        }

        card.appendChild(rankBadge);
        card.appendChild(hospitalName);
        card.appendChild(hospitalDepartment);
        card.appendChild(locationInfo);
        card.appendChild(hospitalUrl);

        return card;
    }

    // 获取科室图标
    getDepartmentIcon(department) {
        const icons = {
            '病理科': '🔬',
            '传染感染': '🦠',
            '耳鼻喉科': '👂',
            '放射科': '📡',
            '呼吸科': '🫁',
            '风湿病': '🦴',
            '妇产科': '👶',
            '骨科': '🦴',
            '精神医学': '🧠',
            '口腔科': '🦷',
            '麻醉科': '💉',
            '泌尿外科': '🫘',
            '内分泌': '⚗️',
            '皮肤科': '🧴',
            '普通外科': '🔪',
            '神经内科': '🧠',
            '肾脏病': '🫘',
            '神经外科': '🧠',
            '消化病': '🍽️',
            '小儿内科': '👶',
            '小儿外科': '👶',
            '心血管': '❤️',
            '心外科': '❤️',
            '胸外科': '🫁',
            '血液学': '🩸',
            '眼科': '👁️',
            '整形外科': '✨',
            '肿瘤学': '🎗️',
            '老年医学': '👴',
            '康复医学': '🏃',
            '检验医学': '🔬',
            '烧伤科': '🔥',
            '核医学': '☢️',
            '超声医学': '📊',
            '急诊医学': '🚑',
            '重症医学': '🏥',
            '临床药学': '💊',
            '生殖医学': '👶',
            '变态反应': '🤧',
            '健康管理': '📋',
            '结核病': '🦠',
            '全科医学': '👩‍⚕️',
            '疼痛学': '😣',
            '运动医学': '🏃',
            '罕见病': '🔍'
        };
        return icons[department] || '🏥';
    }

    // 显示医院排行榜模态框
    showHospitalRankingModal() {
        const modal = this.createHospitalModal();
        document.body.appendChild(modal);
        
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
            width: 95%;
            max-width: 1400px;
            max-height: 85vh;
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
        title.textContent = '华南专科医院排行榜 - 完整版';
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

        // 默认显示所有科室
        this.displayModalHospitalData('all', hospitalList);

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

        // 添加"全部科室"选项
        const allOption = document.createElement('option');
        allOption.value = 'all';
        allOption.textContent = '全部科室';
        select.appendChild(allOption);

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
            this.displayModalHospitalData(e.target.value, hospitalList);
        });

        container.appendChild(label);
        container.appendChild(select);
        return container;
    }

    // 在模态框中显示医院数据
    displayModalHospitalData(selectedDepartment, container) {
        container.innerHTML = '';

        if (selectedDepartment === 'all') {
            // 显示所有科室
            Object.keys(this.hospitalData).forEach(department => {
                this.createDepartmentSection(department, container);
            });
        } else {
            // 显示选定科室
            this.createDepartmentSection(selectedDepartment, container);
        }
    }

    // 创建科室区块
    createDepartmentSection(department, container) {
        const hospitals = this.hospitalData[department] || [];
        
        if (hospitals.length === 0) return;

        // 创建科室标题
        const departmentTitle = document.createElement('h3');
        departmentTitle.innerHTML = `
            <span style="margin-right: 10px;">${this.getDepartmentIcon(department)}</span>
            ${department} 专科排名
        `;
        departmentTitle.style.cssText = `
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
        `;
        container.appendChild(departmentTitle);

        // 创建医院网格
        const hospitalGrid = document.createElement('div');
        hospitalGrid.style.cssText = `
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 16px;
            margin-top: 20px;
            margin-bottom: 40px;
        `;

        // 按排名排序
        const sortedHospitals = [...hospitals].sort((a, b) => {
            if (a.rank === '获提名医院' && b.rank !== '获提名医院') return 1;
            if (a.rank !== '获提名医院' && b.rank === '获提名医院') return -1;
            if (a.rank === '获提名医院' && b.rank === '获提名医院') return 0;
            return parseInt(a.rank) - parseInt(b.rank);
        });

        sortedHospitals.forEach((hospital, index) => {
            const hospitalCard = this.createModalHospitalCard(hospital);
            hospitalGrid.appendChild(hospitalCard);
        });

        container.appendChild(hospitalGrid);
    }

    // 创建模态框医院卡片
    createModalHospitalCard(hospital) {
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