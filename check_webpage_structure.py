import requests
from bs4 import BeautifulSoup

def check_webpage_structure(url):
    """
    检查网页结构
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        print(f"状态码: {response.status_code}")
        print(f"编码: {response.encoding}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有div元素
        divs = soup.find_all('div')
        print(f"\n找到 {len(divs)} 个div元素")
        
        # 查找可能的类名
        classes = set()
        for div in divs:
            if div.get('class'):
                classes.update(div.get('class'))
        
        print(f"找到的类名: {classes}")
        
        # 查找主要内容区域
        possible_content_selectors = [
            'div.content',
            'div.main',
            'div.article',
            'div.text',
            'div.body',
            'div#content',
            'div#main',
            'div#article'
        ]
        
        for selector in possible_content_selectors:
            content = soup.select(selector)
            if content:
                print(f"\n找到内容区域: {selector}")
                print(f"内容长度: {len(content[0].get_text())}")
                print(f"前500字符: {content[0].get_text()[:500]}")
                break
        
        # 如果没有找到，尝试查找包含"科"字的div
        medical_divs = []
        for div in divs:
            text = div.get_text()
            if '科' in text and len(text) > 100:
                medical_divs.append(div)
        
        if medical_divs:
            print(f"\n找到 {len(medical_divs)} 个可能包含医疗信息的div")
            for i, div in enumerate(medical_divs[:3]):
                print(f"\n第{i+1}个div的类名: {div.get('class')}")
                print(f"内容前200字符: {div.get_text()[:200]}")
        
        return soup
        
    except Exception as e:
        print(f"检查网页结构时出错: {str(e)}")
        return None

# 检查第一个URL
url = "https://www.fdygs.com/news2023-1-11.aspx"
print(f"检查URL: {url}")
soup = check_webpage_structure(url) 