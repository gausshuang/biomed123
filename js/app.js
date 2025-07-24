// 生物医学导航网站 JavaScript
// 原生JavaScript实现，无需外部框架依赖

class BioMedNavigator {
    constructor() {
        this.init();
    }

    init() {
        this.setupSearchFunctionality();
        this.setupLinkTracking();
        this.setupKeyboardShortcuts();
        this.addLoadingAnimations();
        this.initializeFavorites();
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