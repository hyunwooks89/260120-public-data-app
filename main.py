import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="📈 US Stock Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #0d1b2a 100%);
    }
    
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf, #ff006e, #fb5607);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 4s ease infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        color: #9ca3af;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
    }
    
    .positive { color: #10b981 !important; }
    .negative { color: #ef4444 !important; }
    
    .stock-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 30px;
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border-radius: 25px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stock-symbol {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00d4ff;
    }
    
    .stock-name {
        font-size: 1.2rem;
        color: #9ca3af;
    }
    
    .stock-price {
        font-size: 3rem;
        font-weight: 800;
        color: white;
    }
    
    .price-change {
        font-size: 1.3rem;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 12px;
    }
    
    .price-up {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }
    
    .price-down {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }
    
    .period-btn {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 12px 24px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .period-btn:hover, .period-btn.active {
        background: linear-gradient(135deg, #00d4ff, #7b2cbf);
        border-color: transparent;
    }
    
    .info-section {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 20px;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.05) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 15px 20px !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 12px 24px;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff, #7b2cbf) !important;
        border: none;
    }
    
    .popular-stocks {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    
    .popular-chip {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 8px 16px;
        color: #9ca3af;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .popular-chip:hover {
        background: rgba(0, 212, 255, 0.2);
        border-color: #00d4ff;
        color: #00d4ff;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #e0e0e0;
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        color: #6b7280;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# 인기 종목 리스트
POPULAR_STOCKS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Google",
    "AMZN": "Amazon",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "META": "Meta",
    "NFLX": "Netflix",
    "AMD": "AMD",
    "INTC": "Intel"
}

# 메인 타이틀
st.markdown('<h1 class="main-title">📈 US Stock Tracker</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">실시간 미국 주식 시세 및 차트 분석</p>', unsafe_allow_html=True)

# 검색 섹션
col_search, col_btn = st.columns([4, 1])

with col_search:
    ticker = st.text_input(
        "주식 티커 입력",
        placeholder="예: AAPL, TSLA, NVDA...",
        label_visibility="collapsed"
    )

with col_btn:
    search_clicked = st.button("🔍 검색", use_container_width=True)

# 인기 종목 버튼
st.markdown("**🔥 인기 종목:**")
popular_cols = st.columns(10)
for i, (symbol, name) in enumerate(POPULAR_STOCKS.items()):
    with popular_cols[i]:
        if st.button(symbol, key=f"pop_{symbol}", use_container_width=True):
            ticker = symbol
            search_clicked = True

# 주식 데이터 가져오기 함수
@st.cache_data(ttl=300)
def get_stock_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except Exception as e:
        return None, None

def create_candlestick_chart(df, title, color_up='#10b981', color_down='#ef4444'):
    fig = go.Figure()
    
    # 캔들스틱 차트
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color=color_up,
        decreasing_line_color=color_down,
        increasing_fillcolor=color_up,
        decreasing_fillcolor=color_down,
        name='Price'
    ))
    
    # 이동평균선
    if len(df) >= 20:
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA20'],
            mode='lines',
            name='MA20',
            line=dict(color='#fbbf24', width=2)
        ))
    
    if len(df) >= 5:
        df['MA5'] = df['Close'].rolling(window=5).mean()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['MA5'],
            mode='lines',
            name='MA5',
            line=dict(color='#00d4ff', width=2)
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#9ca3af'),
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#9ca3af'),
            tickprefix='$'
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        ),
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_volume_chart(df):
    colors = ['#10b981' if row['Close'] >= row['Open'] else '#ef4444' for _, row in df.iterrows()]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        marker_color=colors,
        name='Volume'
    ))
    
    fig.update_layout(
        title=dict(text='📊 거래량', font=dict(size=16, color='white')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#9ca3af')
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#9ca3af')
        ),
        height=200,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    
    return fig

# 검색 실행
if ticker:
    ticker = ticker.upper().strip()
    
    with st.spinner(f'📡 {ticker} 데이터를 불러오는 중...'):
        # 1개월 데이터로 기본 정보 가져오기
        hist_1m, info = get_stock_data(ticker, "1mo")
        
        if hist_1m is not None and len(hist_1m) > 0 and info:
            # 주식 헤더 정보
            current_price = hist_1m['Close'].iloc[-1]
            prev_close = hist_1m['Close'].iloc[-2] if len(hist_1m) > 1 else current_price
            price_change = current_price - prev_close
            price_change_pct = (price_change / prev_close) * 100
            
            company_name = info.get('longName', info.get('shortName', ticker))
            
            # 가격 변화에 따른 스타일
            change_class = "price-up" if price_change >= 0 else "price-down"
            change_symbol = "+" if price_change >= 0 else ""
            change_arrow = "▲" if price_change >= 0 else "▼"
            
            st.markdown(f"""
            <div class="stock-header">
                <div>
                    <div class="stock-symbol">{ticker}</div>
                    <div class="stock-name">{company_name}</div>
                </div>
                <div style="margin-left: auto; text-align: right;">
                    <div class="stock-price">${current_price:,.2f}</div>
                    <span class="price-change {change_class}">
                        {change_arrow} {change_symbol}{price_change:,.2f} ({change_symbol}{price_change_pct:.2f}%)
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 주요 지표 카드
            col1, col2, col3, col4, col5 = st.columns(5)
            
            metrics = [
                ("📈 시가", f"${hist_1m['Open'].iloc[-1]:,.2f}"),
                ("📊 고가", f"${hist_1m['High'].iloc[-1]:,.2f}"),
                ("📉 저가", f"${hist_1m['Low'].iloc[-1]:,.2f}"),
                ("💹 거래량", f"{hist_1m['Volume'].iloc[-1]:,.0f}"),
                ("💰 시가총액", f"${info.get('marketCap', 0)/1e9:,.1f}B" if info.get('marketCap') else "N/A")
            ]
            
            for col, (label, value) in zip([col1, col2, col3, col4, col5], metrics):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 기간별 차트 탭
            tab_daily, tab_weekly, tab_monthly = st.tabs(["📅 일별 (1개월)", "📆 주별 (6개월)", "🗓️ 월별 (1년)"])
            
            with tab_daily:
                hist_daily, _ = get_stock_data(ticker, "1mo")
                if hist_daily is not None and len(hist_daily) > 0:
                    fig_daily = create_candlestick_chart(hist_daily, f"📅 {ticker} 일별 차트 (최근 1개월)")
                    st.plotly_chart(fig_daily, use_container_width=True)
                    
                    fig_vol_daily = create_volume_chart(hist_daily)
                    st.plotly_chart(fig_vol_daily, use_container_width=True)
            
            with tab_weekly:
                hist_6m, _ = get_stock_data(ticker, "6mo")
                if hist_6m is not None and len(hist_6m) > 0:
                    # 주별 데이터로 리샘플링
                    hist_weekly = hist_6m.resample('W').agg({
                        'Open': 'first',
                        'High': 'max',
                        'Low': 'min',
                        'Close': 'last',
                        'Volume': 'sum'
                    }).dropna()
                    
                    fig_weekly = create_candlestick_chart(hist_weekly, f"📆 {ticker} 주별 차트 (최근 6개월)")
                    st.plotly_chart(fig_weekly, use_container_width=True)
                    
                    fig_vol_weekly = create_volume_chart(hist_weekly)
                    st.plotly_chart(fig_vol_weekly, use_container_width=True)
            
            with tab_monthly:
                hist_1y, _ = get_stock_data(ticker, "1y")
                if hist_1y is not None and len(hist_1y) > 0:
                    # 월별 데이터로 리샘플링
                    hist_monthly = hist_1y.resample('ME').agg({
                        'Open': 'first',
                        'High': 'max',
                        'Low': 'min',
                        'Close': 'last',
                        'Volume': 'sum'
                    }).dropna()
                    
                    fig_monthly = create_candlestick_chart(hist_monthly, f"🗓️ {ticker} 월별 차트 (최근 1년)")
                    st.plotly_chart(fig_monthly, use_container_width=True)
                    
                    fig_vol_monthly = create_volume_chart(hist_monthly)
                    st.plotly_chart(fig_vol_monthly, use_container_width=True)
            
            # 추가 정보 섹션
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("""
                <div class="info-section">
                    <div class="section-title">📋 기업 정보</div>
                </div>
                """, unsafe_allow_html=True)
                
                info_data = {
                    "섹터": info.get('sector', 'N/A'),
                    "산업": info.get('industry', 'N/A'),
                    "국가": info.get('country', 'N/A'),
                    "직원 수": f"{info.get('fullTimeEmployees', 0):,}" if info.get('fullTimeEmployees') else 'N/A',
                    "웹사이트": info.get('website', 'N/A')
                }
                
                for key, value in info_data.items():
                    st.markdown(f"**{key}:** {value}")
            
            with col_info2:
                st.markdown("""
                <div class="info-section">
                    <div class="section-title">📊 투자 지표</div>
                </div>
                """, unsafe_allow_html=True)
                
                investment_data = {
                    "P/E 비율": f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else 'N/A',
                    "EPS": f"${info.get('trailingEps', 0):.2f}" if info.get('trailingEps') else 'N/A',
                    "52주 최고가": f"${info.get('fiftyTwoWeekHigh', 0):,.2f}" if info.get('fiftyTwoWeekHigh') else 'N/A',
                    "52주 최저가": f"${info.get('fiftyTwoWeekLow', 0):,.2f}" if info.get('fiftyTwoWeekLow') else 'N/A',
                    "배당 수익률": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A'
                }
                
                for key, value in investment_data.items():
                    st.markdown(f"**{key}:** {value}")
            
            # 기업 설명
            if info.get('longBusinessSummary'):
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("📝 기업 소개 (영문)"):
                    st.write(info.get('longBusinessSummary'))
        
        else:
            st.error(f"❌ '{ticker}' 티커를 찾을 수 없습니다. 올바른 티커 심볼을 입력해주세요.")
            st.info("💡 예시: AAPL (Apple), TSLA (Tesla), NVDA (NVIDIA), GOOGL (Google)")

else:
    # 안내 메시지
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 5rem; margin-bottom: 20px;">🔍</div>
        <h2 style="color: white; margin-bottom: 15px;">주식 티커를 검색해보세요</h2>
        <p style="color: #9ca3af; font-size: 1.1rem;">
            상단 검색창에 미국 주식 티커 심볼을 입력하거나<br>
            인기 종목 버튼을 클릭하세요
        </p>
    </div>
    """, unsafe_allow_html=True)

# 푸터
st.markdown("""
<div class="footer">
    <p>📊 Data provided by Yahoo Finance | 💡 Investment decisions should be made carefully</p>
    <p style="font-size: 0.8rem; margin-top: 10px;">※ 본 서비스는 투자 권유가 아니며, 투자 책임은 본인에게 있습니다.</p>
</div>
""", unsafe_allow_html=True)
