import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import feedparser
import requests
from xml.etree import ElementTree as ET

# 페이지 설정
st.set_page_config(
    page_title="글로벌 마켓 뉴스",
    page_icon="📰",
    layout="wide"
)

# CSS 스타일링
css_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .stApp { background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%); }
    
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px 20px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1));
        border-radius: 30px;
        margin-bottom: 40px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 30px;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }
    
    .section-icon {
        font-size: 1.8rem;
    }
    
    .news-card {
        background: linear-gradient(145deg, rgba(30,41,59,0.8), rgba(15,23,42,0.8));
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        border-color: rgba(96, 165, 250, 0.3);
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }
    
    .news-source {
        display: inline-block;
        font-size: 0.75rem;
        color: #60a5fa;
        background: rgba(96, 165, 250, 0.15);
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
        font-weight: 500;
    }
    
    .news-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    
    .news-summary {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.7;
        margin-bottom: 12px;
    }
    
    .news-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.8rem;
        color: #64748b;
    }
    
    .news-time {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .news-link {
        color: #60a5fa;
        text-decoration: none;
        font-weight: 500;
    }
    
    .news-link:hover {
        text-decoration: underline;
    }
    
    .market-card {
        background: linear-gradient(145deg, rgba(30,41,59,0.6), rgba(15,23,42,0.6));
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        height: 100%;
    }
    
    .market-name {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 8px;
    }
    
    .market-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 5px;
    }
    
    .market-up { color: #22c55e; }
    .market-down { color: #ef4444; }
    
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: #ef4444;
        border-radius: 50%;
    }
    
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #475569;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 50px;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #cbd5e1;
    }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# 주요 지수 티커
MAJOR_INDICES = {
    "S&P 500": "^GSPC",
    "나스닥": "^IXIC",
    "다우존스": "^DJI",
    "니케이 225": "^N225",
    "항셍": "^HSI",
    "코스피": "^KS11"
}

@st.cache_data(ttl=300)
def get_index_data(ticker):
    """지수 데이터 가져오기"""
    try:
        index = yf.Ticker(ticker)
        hist = index.history(period="2d")
        if len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = current - prev
            change_pct = (change / prev) * 100
            return {
                'price': current,
                'change': change,
                'change_pct': change_pct
            }
        return None
    except:
        return None

@st.cache_data(ttl=300)
def get_mk_news():
    """매일경제 RSS에서 뉴스 가져오기"""
    try:
        rss_url = "https://www.mk.co.kr/rss/50200011/"
        feed = feedparser.parse(rss_url)
        
        news_list = []
        for entry in feed.entries[:15]:
            # pubDate 파싱
            pub_date = entry.get('published', '')
            
            news_item = {
                'title': entry.get('title', '제목 없음'),
                'link': entry.get('link', '#'),
                'summary': entry.get('summary', entry.get('description', '')),
                'published': pub_date,
                'source': '매일경제'
            }
            news_list.append(news_item)
        
        return news_list
    except Exception as e:
        st.error("뉴스를 불러오는 중 오류가 발생했습니다: " + str(e))
        return []

def format_pub_date(pub_date_str):
    """발행일을 한국어 형식으로 변환"""
    try:
        # RSS 날짜 형식 파싱 시도
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(pub_date_str)
        return dt.strftime('%m월 %d일 %H:%M')
    except:
        try:
            # 다른 형식 시도
            dt = datetime.strptime(pub_date_str[:19], '%Y-%m-%dT%H:%M:%S')
            return dt.strftime('%m월 %d일 %H:%M')
        except:
            return pub_date_str[:16] if pub_date_str else ""

def clean_html(text):
    """HTML 태그 제거"""
    import re
    clean = re.sub('<[^<]+?>', '', text)
    clean = clean.replace('&nbsp;', ' ')
    clean = clean.replace('&quot;', '"')
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&gt;', '>')
    return clean.strip()

def render_market_card(name, data):
    """마켓 카드 HTML 생성"""
    if data is None:
        return ""
    
    change_class = "market-up" if data['change'] >= 0 else "market-down"
    change_symbol = "+" if data['change'] >= 0 else ""
    arrow = "▲" if data['change'] >= 0 else "▼"
    
    price_str = "{:,.2f}".format(data['price'])
    change_pct_str = "{:.2f}".format(data['change_pct'])
    
    html = '''
    <div class="market-card">
        <div class="market-name">''' + name + '''</div>
        <div class="market-price">''' + price_str + '''</div>
        <div class="''' + change_class + '''" style="font-size: 1rem; font-weight: 600;">''' + arrow + " " + change_symbol + change_pct_str + '''%</div>
    </div>
    '''
    return html

def render_news_card(title, summary, pub_date, link, source):
    """뉴스 카드 HTML 생성"""
    # HTML 태그 제거
    clean_title = clean_html(title)
    clean_summary = clean_html(summary)
    
    # 요약 길이 제한
    if len(clean_summary) > 150:
        clean_summary = clean_summary[:150] + "..."
    
    formatted_date = format_pub_date(pub_date)
    
    html = '''
    <div class="news-card">
        <span class="news-source">''' + source + '''</span>
        <div class="news-title">''' + clean_title + '''</div>
        <div class="news-summary">''' + clean_summary + '''</div>
        <div class="news-meta">
            <span class="news-time">🕐 ''' + formatted_date + '''</span>
            <a href="''' + link + '''" target="_blank" class="news-link">자세히 보기 →</a>
        </div>
    </div>
    '''
    return html

def render_stock_card(name, ticker, data):
    """주식 카드 HTML 생성"""
    if data is None:
        return ""
    
    change_class = "market-up" if data['change'] >= 0 else "market-down"
    change_symbol = "+" if data['change'] >= 0 else ""
    arrow = "▲" if data['change'] >= 0 else "▼"
    
    price_str = "{:,.2f}".format(data['price'])
    change_pct_str = "{:.2f}".format(data['change_pct'])
    
    html = '''
    <div class="market-card" style="margin-bottom: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-weight: 600; color: white;">''' + name + '''</div>
                <div style="font-size: 0.8rem; color: #64748b;">''' + ticker + '''</div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 600; color: white;">$''' + price_str + '''</div>
                <div class="''' + change_class + '''" style="font-size: 0.9rem;">''' + arrow + " " + change_symbol + change_pct_str + '''%</div>
            </div>
        </div>
    </div>
    '''
    return html

# 히어로 섹션
st.markdown('''
<div class="hero-section">
    <h1 class="hero-title">📰 글로벌 마켓 뉴스</h1>
    <p class="hero-subtitle">전 세계 주식시장의 최신 뉴스와 동향을 한눈에</p>
    <span class="live-badge"><span class="live-dot"></span> LIVE</span>
</div>
''', unsafe_allow_html=True)

# 주요 지수 현황
st.markdown('''
<div class="section-header">
    <span class="section-icon">📊</span>
    <span class="section-title">주요 지수 현황</span>
</div>
''', unsafe_allow_html=True)

index_cols = st.columns(6)

for i, (name, ticker) in enumerate(MAJOR_INDICES.items()):
    with index_cols[i]:
        data = get_index_data(ticker)
        html = render_market_card(name, data)
        if html:
            st.markdown(html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 뉴스 섹션
news_col1, news_col2 = st.columns([2, 1])

with news_col1:
    st.markdown('''
    <div class="section-header">
        <span class="section-icon">🌍</span>
        <span class="section-title">글로벌 시장 뉴스</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # 매일경제 RSS에서 뉴스 가져오기
    with st.spinner("최신 뉴스를 불러오는 중..."):
        news_list = get_mk_news()
    
    if news_list:
        for news in news_list[:10]:
            html = render_news_card(
                news['title'],
                news['summary'],
                news['published'],
                news['link'],
                news['source']
            )
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.warning("뉴스를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")

with news_col2:
    st.markdown('''
    <div class="section-header">
        <span class="section-icon">🔥</span>
        <span class="section-title">주목할 종목</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # 주요 기업들
    hot_stocks = {
        "NVDA": "NVIDIA",
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "TSLA": "Tesla",
        "GOOGL": "Google",
        "AMZN": "Amazon"
    }
    
    for ticker, name in hot_stocks.items():
        data = get_index_data(ticker)
        html = render_stock_card(name, ticker, data)
        if html:
            st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 시장 요약
    st.markdown('''
    <div class="section-header">
        <span class="section-icon">📈</span>
        <span class="section-title">오늘의 시장</span>
    </div>
    ''', unsafe_allow_html=True)
    
    today = datetime.now().strftime('%Y년 %m월 %d일')
    
    market_summary = '''
    <div class="market-card">
        <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 15px;">📅 ''' + today + '''</div>
        <div style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.8;">
            글로벌 증시가 혼조세를 보이고 있습니다. 
            미국 연준의 금리 정책과 기업 실적 발표에 
            투자자들의 관심이 집중되고 있습니다.
        </div>
    </div>
    '''
    st.markdown(market_summary, unsafe_allow_html=True)

# 푸터
update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
footer_html = '''
<div class="footer">
    <p>📊 지수 데이터: Yahoo Finance | 📰 뉴스 제공: 매일경제</p>
    <p>마지막 업데이트: ''' + update_time + '''</p>
    <p style="margin-top: 15px; font-size: 0.75rem;">
        ⚠️ 본 서비스는 투자 권유가 아니며, 투자의 책임은 본인에게 있습니다.
    </p>
</div>
'''
st.markdown(footer_html, unsafe_allow_html=True)
