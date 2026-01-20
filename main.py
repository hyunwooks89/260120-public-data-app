import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="글로벌 시가총액 TOP 기업",
    page_icon="🌍",
    layout="wide"
)

# CSS 스타일링
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .stApp { background: #0f172a; }
    
    .main-header {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
    }
    
    .update-time {
        text-align: center;
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 30px;
    }
    
    .country-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid #334155;
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .country-card:hover {
        border-color: #3b82f6;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
    }
    
    .country-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #334155;
    }
    
    .country-flag {
        font-size: 2.5rem;
    }
    
    .country-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
    }
    
    .company-section {
        margin-bottom: 15px;
    }
    
    .company-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 5px;
    }
    
    .company-ticker {
        font-size: 0.85rem;
        color: #64748b;
        background: #1e293b;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    .market-cap {
        font-size: 1.8rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 15px;
    }
    
    .stock-price {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .price-value {
        font-size: 1.2rem;
        color: #e2e8f0;
        font-weight: 600;
    }
    
    .price-change {
        font-size: 0.9rem;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 500;
    }
    
    .price-up {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .price-down {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #1e293b;
        font-size: 0.9rem;
    }
    
    .info-label {
        color: #94a3b8;
    }
    
    .info-value {
        color: #e2e8f0;
        font-weight: 500;
    }
    
    .sector-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 10px;
    }
    
    .loading-card {
        background: #1e293b;
        border-radius: 20px;
        padding: 50px;
        text-align: center;
        color: #64748b;
    }
    
    .summary-table {
        background: #1e293b;
        border-radius: 16px;
        padding: 25px;
        margin-top: 30px;
    }
    
    .summary-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        margin-bottom: 20px;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# 국가별 대표 기업 (시가총액 1위 기업들)
TOP_COMPANIES = {
    "미국": {
        "flag": "🇺🇸",
        "ticker": "AAPL",
        "company": "Apple Inc.",
        "currency": "USD"
    },
    "일본": {
        "flag": "🇯🇵",
        "ticker": "7203.T",
        "company": "Toyota Motor Corp.",
        "currency": "JPY"
    },
    "독일": {
        "flag": "🇩🇪",
        "ticker": "SAP.DE",
        "company": "SAP SE",
        "currency": "EUR"
    },
    "영국": {
        "flag": "🇬🇧",
        "ticker": "AZN.L",
        "company": "AstraZeneca PLC",
        "currency": "GBP"
    },
    "프랑스": {
        "flag": "🇫🇷",
        "ticker": "MC.PA",
        "company": "LVMH",
        "currency": "EUR"
    },
    "이탈리아": {
        "flag": "🇮🇹",
        "ticker": "RACE.MI",
        "company": "Ferrari N.V.",
        "currency": "EUR"
    },
    "한국": {
        "flag": "🇰🇷",
        "ticker": "005930.KS",
        "company": "Samsung Electronics",
        "currency": "KRW"
    },
    "중국": {
        "flag": "🇨🇳",
        "ticker": "TCEHY",
        "company": "Tencent Holdings",
        "currency": "USD"
    }
}

def format_market_cap(market_cap):
    """시가총액을 읽기 쉬운 형식으로 변환"""
    if market_cap >= 1e12:
        return "${:.2f}T".format(market_cap/1e12)
    elif market_cap >= 1e9:
        return "${:.2f}B".format(market_cap/1e9)
    elif market_cap >= 1e6:
        return "${:.2f}M".format(market_cap/1e6)
    else:
        return "${:,.0f}".format(market_cap)

def format_number(num):
    """숫자를 읽기 쉬운 형식으로 변환"""
    if num >= 1e9:
        return "{:.2f}B".format(num/1e9)
    elif num >= 1e6:
        return "{:.2f}M".format(num/1e6)
    else:
        return "{:,.0f}".format(num)

@st.cache_data(ttl=3600)
def get_stock_data(ticker):
    """주식 데이터 가져오기"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        
        if len(hist) >= 2:
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2]
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
        else:
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            price_change = 0
            price_change_pct = 0
        
        return {
            'name': info.get('longName', info.get('shortName', 'N/A')),
            'market_cap': info.get('marketCap', 0),
            'price': current_price,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'employees': info.get('fullTimeEmployees', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'volume': info.get('volume', 0),
            'currency': info.get('currency', 'USD')
        }
    except Exception as e:
        return None

def render_country_card(country, data):
    """국가 카드 HTML 생성"""
    change_class = "price-up" if data['price_change'] >= 0 else "price-down"
    change_symbol = "+" if data['price_change'] >= 0 else ""
    change_arrow = "▲" if data['price_change'] >= 0 else "▼"
    
    price_formatted = "{:,.2f}".format(data['price'])
    change_pct_formatted = "{:.2f}".format(data['price_change_pct'])
    pe_formatted = "{:.2f}".format(data['pe_ratio']) if data['pe_ratio'] else 'N/A'
    volume_formatted = format_number(data['volume'])
    market_cap_formatted = format_market_cap(data['market_cap'])
    
    html = """
    <div class="country-card">
        <div class="country-header">
            <span class="country-flag">{flag}</span>
            <span class="country-name">{country}</span>
        </div>
        <div class="company-section">
            <div class="company-name">{name}</div>
            <span class="company-ticker">{ticker}</span>
        </div>
        <div class="market-cap">{market_cap}</div>
        <div class="stock-price">
            <span class="price-value">{currency} {price}</span>
            <span class="price-change {change_class}">{arrow} {symbol}{change_pct}%</span>
        </div>
        <div class="info-row">
            <span class="info-label">P/E 비율</span>
            <span class="info-value">{pe}</span>
        </div>
        <div class="info-row">
            <span class="info-label">거래량</span>
            <span class="info-value">{volume}</span>
        </div>
        <span class="sector-badge">{sector}</span>
    </div>
    """.format(
        flag=data['flag'],
        country=country,
        name=data['name'],
        ticker=data['ticker'],
        market_cap=market_cap_formatted,
        currency=data['currency'],
        price=price_formatted,
        change_class=change_class,
        arrow=change_arrow,
        symbol=change_symbol,
        change_pct=change_pct_formatted,
        pe=pe_formatted,
        volume=volume_formatted,
        sector=data['sector']
    )
    return html

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌍 글로벌 시가총액 TOP 기업</h1>
    <p class="main-subtitle">주요 8개국 시가총액 1위 기업 현황</p>
</div>
""", unsafe_allow_html=True)

update_time = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
st.markdown('<p class="update-time">📅 {} 기준</p>'.format(update_time), unsafe_allow_html=True)

# 데이터 로딩
with st.spinner('🔄 전 세계 주식 데이터를 불러오는 중...'):
    stock_data = {}
    for country, info in TOP_COMPANIES.items():
        data = get_stock_data(info['ticker'])
        if data:
            stock_data[country] = {**info, **data}

# 국가 카드 표시 (2행 4열)
if stock_data:
    # 첫 번째 행
    row1_countries = ["미국", "일본", "독일", "영국"]
    cols1 = st.columns(4)
    
    for i, country in enumerate(row1_countries):
        with cols1[i]:
            if country in stock_data:
                html = render_country_card(country, stock_data[country])
                st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 두 번째 행
    row2_countries = ["프랑스", "이탈리아", "한국", "중국"]
    cols2 = st.columns(4)
    
    for i, country in enumerate(row2_countries):
        with cols2[i]:
            if country in stock_data:
                html = render_country_card(country, stock_data[country])
                st.markdown(html, unsafe_allow_html=True)
    
    # 요약 테이블
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="summary-table">
        <div class="summary-title">📊 시가총액 순위 요약</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터프레임 생성
    summary_data = []
    for country, data in stock_data.items():
        change_symbol = "+" if data['price_change_pct'] >= 0 else ""
        summary_data.append({
            "국가": "{} {}".format(data['flag'], country),
            "기업명": data['name'],
            "티커": data['ticker'],
            "시가총액 (USD)": data['market_cap'],
            "시가총액": format_market_cap(data['market_cap']),
            "주가 변동": "{}{}%".format(change_symbol, round(data['price_change_pct'], 2)),
            "섹터": data['sector']
        })
    
    df = pd.DataFrame(summary_data)
    df = df.sort_values("시가총액 (USD)", ascending=False)
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    
    # 표시할 컬럼만 선택
    display_df = df[["국가", "기업명", "티커", "시가총액", "주가 변동", "섹터"]]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=False
    )

# 푸터
st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #64748b; font-size: 0.85rem;">
    <p>📈 데이터 제공: Yahoo Finance | 실시간 데이터와 차이가 있을 수 있습니다</p>
    <p>💡 시가총액 1위 기업은 시장 상황에 따라 변동될 수 있습니다</p>
</div>
""", unsafe_allow_html=True)
