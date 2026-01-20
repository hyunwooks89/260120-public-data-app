import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="✨ MBTI 진로 탐색기 ✨",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    * {
        font-family: 'Noto Sans KR', 'Gowun Dodum', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }
    
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 5s ease infinite;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255,255,255,0.3);
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #a0a0a0;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    .mbti-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .mbti-btn {
        background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border: 2px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(10px);
    }
    
    .mbti-btn:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.1);
        border-color: rgba(255,255,255,0.3);
    }
    
    .mbti-type {
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 5px;
    }
    
    .mbti-emoji {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .mbti-name {
        font-size: 0.85rem;
        color: #888;
    }
    
    /* MBTI 타입별 색상 */
    .analyst { color: #a855f7; border-color: rgba(168, 85, 247, 0.3); }
    .analyst:hover { box-shadow: 0 20px 40px rgba(168, 85, 247, 0.3); }
    
    .diplomat { color: #22c55e; border-color: rgba(34, 197, 94, 0.3); }
    .diplomat:hover { box-shadow: 0 20px 40px rgba(34, 197, 94, 0.3); }
    
    .sentinel { color: #3b82f6; border-color: rgba(59, 130, 246, 0.3); }
    .sentinel:hover { box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3); }
    
    .explorer { color: #f59e0b; border-color: rgba(245, 158, 11, 0.3); }
    .explorer:hover { box-shadow: 0 20px 40px rgba(245, 158, 11, 0.3); }
    
    .result-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        border-radius: 30px;
        padding: 40px;
        margin: 20px auto;
        max-width: 900px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    .result-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .result-emoji {
        font-size: 5rem;
        margin-bottom: 15px;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    .result-type {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 10px;
    }
    
    .result-nickname {
        font-size: 1.5rem;
        color: #feca57;
        margin-bottom: 20px;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 30px 0 15px 0;
        padding-left: 15px;
        border-left: 4px solid;
        color: white;
    }
    
    .trait-box {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .trait-item {
        display: flex;
        align-items: center;
        padding: 10px 0;
        color: #e0e0e0;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .career-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    
    .career-item {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.03));
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .career-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    .career-emoji {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .career-name {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .compatibility-section {
        margin-top: 30px;
        padding: 25px;
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
    }
    
    .compat-row {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 15px;
    }
    
    .compat-item {
        text-align: center;
        padding: 15px 25px;
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
    }
    
    .good-match { border: 2px solid rgba(34, 197, 94, 0.5); }
    .challenge-match { border: 2px solid rgba(239, 68, 68, 0.5); }
    
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        color: #666;
        font-size: 0.9rem;
    }
    
    .sparkle {
        position: fixed;
        pointer-events: none;
        animation: sparkle-fade 1s ease-out forwards;
    }
    
    @keyframes sparkle-fade {
        0% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(0); }
    }
    
    /* Streamlit 기본 스타일 오버라이드 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        color: white;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #e0e0e0;
    }
    
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# MBTI 데이터
mbti_data = {
    "INTJ": {
        "emoji": "🧠",
        "nickname": "전략가 (The Architect)",
        "group": "analyst",
        "color": "#a855f7",
        "description": "독립적이고 전략적인 사고를 하는 INTJ는 세상을 체스판처럼 바라봅니다. 항상 큰 그림을 보며, 복잡한 문제를 해결하는 데 탁월한 능력을 발휘합니다.",
        "traits": [
            "🎯 목표 지향적이며 장기적 비전을 가짐",
            "🔬 분석적이고 논리적인 사고력",
            "📚 지식에 대한 강한 열망",
            "🏔️ 높은 기준과 완벽주의 성향",
            "🤔 독립적이며 혼자 일하는 것을 선호"
        ],
        "careers": [
            ("👨‍🔬", "과학자"),
            ("💻", "소프트웨어 개발자"),
            ("📊", "전략 컨설턴트"),
            ("⚖️", "변호사"),
            ("🏛️", "건축가"),
            ("📈", "투자 분석가")
        ],
        "good_match": ["ENFP", "ENTP"],
        "challenge_match": ["ESFP", "ISFP"]
    },
    "INTP": {
        "emoji": "🔬",
        "nickname": "논리술사 (The Logician)",
        "group": "analyst",
        "color": "#a855f7",
        "description": "끝없는 호기심을 가진 INTP는 이론과 아이디어의 세계에서 살아갑니다. 복잡한 문제를 분석하고 혁신적인 해결책을 찾는 것을 즐깁니다.",
        "traits": [
            "💡 창의적이고 혁신적인 사고",
            "🧩 복잡한 문제 해결 능력",
            "📖 이론적이고 추상적인 개념에 관심",
            "🎨 독창적인 아이디어 생성",
            "🔍 끊임없는 분석과 탐구"
        ],
        "careers": [
            ("🔬", "연구원"),
            ("💻", "프로그래머"),
            ("🧮", "수학자"),
            ("🎮", "게임 개발자"),
            ("📐", "시스템 분석가"),
            ("🤖", "AI 엔지니어")
        ],
        "good_match": ["ENTJ", "ENFJ"],
        "challenge_match": ["ESFJ", "ISFJ"]
    },
    "ENTJ": {
        "emoji": "👑",
        "nickname": "통솔자 (The Commander)",
        "group": "analyst",
        "color": "#a855f7",
        "description": "타고난 리더인 ENTJ는 카리스마와 자신감으로 사람들을 이끕니다. 효율성을 추구하며, 목표 달성을 위해 체계적으로 계획하고 실행합니다.",
        "traits": [
            "👔 강력한 리더십과 추진력",
            "📋 체계적이고 조직적인 성향",
            "🎤 설득력 있는 의사소통 능력",
            "⚡ 결단력과 빠른 의사결정",
            "🏆 성취 지향적이며 야망이 큼"
        ],
        "careers": [
            ("👔", "CEO/경영자"),
            ("📊", "경영 컨설턴트"),
            ("⚖️", "판사/검사"),
            ("🏛️", "정치인"),
            ("💼", "사업가"),
            ("🎬", "영화 감독")
        ],
        "good_match": ["INTP", "INFP"],
        "challenge_match": ["ISFP", "INFP"]
    },
    "ENTP": {
        "emoji": "💡",
        "nickname": "변론가 (The Debater)",
        "group": "analyst",
        "color": "#a855f7",
        "description": "기발한 아이디어와 날카로운 재치를 가진 ENTP는 토론을 즐기고 관습에 도전합니다. 새로운 가능성을 탐구하며 창의적인 해결책을 찾습니다.",
        "traits": [
            "🗣️ 뛰어난 토론 및 설득 능력",
            "🌟 창의적이고 혁신적인 사고",
            "🎢 새로운 도전을 즐김",
            "🧠 빠른 두뇌 회전과 재치",
            "🔄 유연하고 적응력이 뛰어남"
        ],
        "careers": [
            ("💼", "기업가"),
            ("📰", "저널리스트"),
            ("🎤", "방송인"),
            ("⚖️", "변호사"),
            ("🎨", "광고 기획자"),
            ("🚀", "스타트업 창업자")
        ],
        "good_match": ["INFJ", "INTJ"],
        "challenge_match": ["ISFJ", "ISTJ"]
    },
    "INFJ": {
        "emoji": "🔮",
        "nickname": "옹호자 (The Advocate)",
        "group": "diplomat",
        "color": "#22c55e",
        "description": "이상주의적이고 원칙적인 INFJ는 깊은 통찰력으로 사람들의 마음을 읽습니다. 조용하지만 강한 신념을 가지고 세상을 더 나은 곳으로 만들고자 합니다.",
        "traits": [
            "💫 깊은 통찰력과 직관",
            "❤️ 타인에 대한 공감 능력",
            "🌍 이상주의적이며 가치 지향적",
            "✍️ 창의적인 표현력",
            "🤝 의미 있는 관계 추구"
        ],
        "careers": [
            ("🩺", "상담사/심리치료사"),
            ("✍️", "작가"),
            ("🎨", "예술가"),
            ("👨‍🏫", "교사"),
            ("🏥", "의료인"),
            ("🌱", "사회복지사")
        ],
        "good_match": ["ENTP", "ENFP"],
        "challenge_match": ["ESTP", "ISTP"]
    },
    "INFP": {
        "emoji": "🦋",
        "nickname": "중재자 (The Mediator)",
        "group": "diplomat",
        "color": "#22c55e",
        "description": "시적인 영혼을 가진 INFP는 자신만의 내면 세계에서 살아갑니다. 진정성과 창의성을 중요시하며, 이상적인 세상을 꿈꿉니다.",
        "traits": [
            "🌈 풍부한 상상력과 창의성",
            "💝 깊은 감정과 공감 능력",
            "📝 자기표현에 대한 욕구",
            "🕊️ 평화를 추구하며 갈등 회피",
            "✨ 진정성과 개성 중시"
        ],
        "careers": [
            ("✍️", "작가/시인"),
            ("🎨", "그래픽 디자이너"),
            ("🎵", "음악가"),
            ("📸", "사진작가"),
            ("🎭", "배우"),
            ("🧘", "요가 강사")
        ],
        "good_match": ["ENFJ", "ENTJ"],
        "challenge_match": ["ESTJ", "ISTJ"]
    },
    "ENFJ": {
        "emoji": "🌟",
        "nickname": "선도자 (The Protagonist)",
        "group": "diplomat",
        "color": "#22c55e",
        "description": "따뜻한 카리스마를 가진 ENFJ는 타인의 성장을 돕는 것에서 기쁨을 느낍니다. 영감을 주는 리더로서 사람들을 하나로 모읍니다.",
        "traits": [
            "🤗 뛰어난 대인관계 능력",
            "🎯 타인의 잠재력을 발견",
            "💬 설득력 있는 소통 능력",
            "🌺 이타적이며 헌신적",
            "🎪 조직력과 리더십"
        ],
        "careers": [
            ("👨‍🏫", "교사/교수"),
            ("🎤", "코치/멘토"),
            ("📢", "인사담당자"),
            ("🏛️", "비영리단체 리더"),
            ("🎬", "이벤트 플래너"),
            ("📺", "방송인")
        ],
        "good_match": ["INFP", "INTP"],
        "challenge_match": ["ISTP", "ESTP"]
    },
    "ENFP": {
        "emoji": "🎪",
        "nickname": "활동가 (The Campaigner)",
        "group": "diplomat",
        "color": "#22c55e",
        "description": "열정적이고 창의적인 ENFP는 어디서든 가능성을 발견합니다. 사람들에게 영감을 주고, 새로운 아이디어로 세상을 밝게 만듭니다.",
        "traits": [
            "🎉 열정적이고 에너지 넘침",
            "🌈 창의적이고 상상력이 풍부",
            "🤝 사교적이며 친화력이 높음",
            "🎨 다양한 관심사와 재능",
            "💫 낙관적이며 긍정적"
        ],
        "careers": [
            ("🎨", "크리에이티브 디렉터"),
            ("📰", "기자/작가"),
            ("🎭", "배우/연예인"),
            ("💼", "마케터"),
            ("🧑‍🏫", "강연가"),
            ("🎬", "콘텐츠 크리에이터")
        ],
        "good_match": ["INTJ", "INFJ"],
        "challenge_match": ["ISTJ", "ESTJ"]
    },
    "ISTJ": {
        "emoji": "📋",
        "nickname": "현실주의자 (The Logistician)",
        "group": "sentinel",
        "color": "#3b82f6",
        "description": "신뢰할 수 있고 책임감 있는 ISTJ는 전통과 규칙을 존중합니다. 꼼꼼하고 체계적으로 일을 처리하며, 맡은 일은 반드시 완수합니다.",
        "traits": [
            "📌 책임감이 강하고 신뢰할 수 있음",
            "📊 체계적이고 꼼꼼함",
            "⚖️ 공정하고 논리적",
            "🏆 끈기와 인내심",
            "🔒 전통과 규칙 존중"
        ],
        "careers": [
            ("💰", "회계사"),
            ("⚖️", "법률가"),
            ("🏦", "은행원"),
            ("🔍", "감사관"),
            ("🏗️", "프로젝트 매니저"),
            ("👮", "경찰관")
        ],
        "good_match": ["ESFP", "ESTP"],
        "challenge_match": ["ENFP", "INFP"]
    },
    "ISFJ": {
        "emoji": "🛡️",
        "nickname": "수호자 (The Defender)",
        "group": "sentinel",
        "color": "#3b82f6",
        "description": "헌신적이고 따뜻한 ISFJ는 조용히 타인을 돌봅니다. 세심한 배려와 성실함으로 주변 사람들에게 안정감을 줍니다.",
        "traits": [
            "🤗 헌신적이고 배려심이 깊음",
            "📝 세심하고 꼼꼼함",
            "🏠 가정과 전통 중시",
            "🤝 협조적이며 팀워크 중시",
            "💪 책임감과 인내심"
        ],
        "careers": [
            ("👩‍⚕️", "간호사"),
            ("👨‍🏫", "초등학교 교사"),
            ("📚", "도서관 사서"),
            ("🏥", "사회복지사"),
            ("💼", "행정 담당자"),
            ("👶", "보육교사")
        ],
        "good_match": ["ESFP", "ESTP"],
        "challenge_match": ["ENTP", "INTP"]
    },
    "ESTJ": {
        "emoji": "🎖️",
        "nickname": "경영자 (The Executive)",
        "group": "sentinel",
        "color": "#3b82f6",
        "description": "질서와 전통을 수호하는 ESTJ는 타고난 조직 관리자입니다. 명확한 규칙 아래서 효율적으로 일하며, 팀을 이끄는 데 능숙합니다.",
        "traits": [
            "👔 강한 리더십과 조직력",
            "📋 체계적이고 효율적",
            "⚡ 결단력이 있고 실행력이 강함",
            "🎯 목표 지향적이며 성과 중시",
            "⚖️ 공정함과 정직함"
        ],
        "careers": [
            ("👔", "경영자/관리자"),
            ("👮", "군인/경찰"),
            ("⚖️", "판사"),
            ("🏦", "은행 지점장"),
            ("🏭", "공장 관리자"),
            ("📊", "재무 관리자")
        ],
        "good_match": ["ISTP", "ISFP"],
        "challenge_match": ["INFP", "ENFP"]
    },
    "ESFJ": {
        "emoji": "💝",
        "nickname": "집정관 (The Consul)",
        "group": "sentinel",
        "color": "#3b82f6",
        "description": "따뜻하고 사교적인 ESFJ는 타인을 돌보는 것에서 기쁨을 찾습니다. 조화로운 환경을 만들고, 사람들을 하나로 모으는 능력이 있습니다.",
        "traits": [
            "🤝 사교적이고 친화력이 높음",
            "💕 타인에 대한 배려와 관심",
            "🎊 조화와 협력 중시",
            "📅 계획적이고 조직적",
            "🏆 인정받고 싶은 욕구"
        ],
        "careers": [
            ("👩‍⚕️", "의료인"),
            ("👨‍🏫", "교사"),
            ("🎪", "이벤트 코디네이터"),
            ("🏨", "호텔리어"),
            ("💼", "인사 담당자"),
            ("🛍️", "판매 전문가")
        ],
        "good_match": ["ISTP", "ISFP"],
        "challenge_match": ["INTP", "ENTP"]
    },
    "ISTP": {
        "emoji": "🔧",
        "nickname": "장인 (The Virtuoso)",
        "group": "explorer",
        "color": "#f59e0b",
        "description": "냉철하고 분석적인 ISTP는 손으로 직접 만드는 것을 즐깁니다. 위기 상황에서 침착하게 문제를 해결하는 실용적인 문제 해결사입니다.",
        "traits": [
            "🔧 실용적이고 손재주가 좋음",
            "🧊 침착하고 냉정함",
            "🔍 분석적인 문제 해결 능력",
            "🏍️ 모험심과 스릴 추구",
            "⚡ 효율성과 논리 중시"
        ],
        "careers": [
            ("✈️", "파일럿"),
            ("🔧", "엔지니어"),
            ("🏍️", "정비사"),
            ("🎖️", "군인"),
            ("🔬", "법의학자"),
            ("🏃", "운동선수")
        ],
        "good_match": ["ESTJ", "ESFJ"],
        "challenge_match": ["ENFJ", "INFJ"]
    },
    "ISFP": {
        "emoji": "🎨",
        "nickname": "모험가 (The Adventurer)",
        "group": "explorer",
        "color": "#f59e0b",
        "description": "조용하고 감성적인 ISFP는 아름다움을 추구하는 예술가입니다. 현재를 즐기며, 자신만의 방식으로 세상을 표현합니다.",
        "traits": [
            "🎨 예술적 감각과 심미안",
            "🌸 온화하고 친절함",
            "🦋 자유로운 영혼",
            "💫 현재를 즐기는 삶",
            "🤫 조용하지만 열정적"
        ],
        "careers": [
            ("🎨", "화가/일러스트레이터"),
            ("📸", "사진작가"),
            ("👨‍🍳", "셰프"),
            ("🌿", "플로리스트"),
            ("💅", "뷰티 아티스트"),
            ("🐕", "수의사")
        ],
        "good_match": ["ESTJ", "ESFJ"],
        "challenge_match": ["ENTJ", "INTJ"]
    },
    "ESTP": {
        "emoji": "🎯",
        "nickname": "사업가 (The Entrepreneur)",
        "group": "explorer",
        "color": "#f59e0b",
        "description": "에너지 넘치고 행동 지향적인 ESTP는 순간을 살아갑니다. 빠른 판단력과 적응력으로 어떤 상황에서도 기회를 포착합니다.",
        "traits": [
            "⚡ 에너지 넘치고 활동적",
            "🎲 모험심과 위험 감수",
            "🗣️ 사교적이며 설득력 있음",
            "🎯 실용적인 문제 해결",
            "🏃 즉흥적이고 유연함"
        ],
        "careers": [
            ("💼", "사업가"),
            ("🎤", "영업 전문가"),
            ("🚔", "경찰관"),
            ("🏋️", "피트니스 트레이너"),
            ("🎰", "주식 트레이더"),
            ("🎬", "스턴트맨")
        ],
        "good_match": ["ISTJ", "ISFJ"],
        "challenge_match": ["INFJ", "ENFJ"]
    },
    "ESFP": {
        "emoji": "🎉",
        "nickname": "연예인 (The Entertainer)",
        "group": "explorer",
        "color": "#f59e0b",
        "description": "밝고 즐거운 에너지의 ESFP는 어디서든 분위기를 띄웁니다. 현재를 즐기고, 사람들과 함께하는 것을 사랑하는 타고난 엔터테이너입니다.",
        "traits": [
            "🎊 밝고 긍정적인 에너지",
            "🎭 뛰어난 엔터테인먼트 능력",
            "🤗 사교적이고 친화력 최고",
            "🎪 즉흥적이고 재미 추구",
            "💃 감각적이고 세련됨"
        ],
        "careers": [
            ("🎤", "가수/배우"),
            ("✈️", "승무원"),
            ("👨‍🍳", "셰프"),
            ("🎪", "이벤트 플래너"),
            ("🏃", "피트니스 강사"),
            ("📺", "MC/진행자")
        ],
        "good_match": ["ISTJ", "ISFJ"],
        "challenge_match": ["INTJ", "INFJ"]
    }
}

# 메인 타이틀
st.markdown('<h1 class="main-title">✨ MBTI 진로 탐색기 ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🔮 당신의 성격 유형에 맞는 꿈의 직업을 찾아보세요 🔮</p>', unsafe_allow_html=True)

# 세션 상태 초기화
if 'selected_mbti' not in st.session_state:
    st.session_state.selected_mbti = None

# MBTI 선택 UI
st.markdown("---")
st.markdown("### 🎯 당신의 MBTI를 선택하세요")

# 그룹별 MBTI 표시
col1, col2, col3, col4 = st.columns(4)

groups = {
    "analyst": {"name": "🧠 분석가형", "types": ["INTJ", "INTP", "ENTJ", "ENTP"], "col": col1},
    "diplomat": {"name": "💚 외교관형", "types": ["INFJ", "INFP", "ENFJ", "ENFP"], "col": col2},
    "sentinel": {"name": "🛡️ 관리자형", "types": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"], "col": col3},
    "explorer": {"name": "🎯 탐험가형", "types": ["ISTP", "ISFP", "ESTP", "ESFP"], "col": col4}
}

for group_key, group_info in groups.items():
    with group_info["col"]:
        st.markdown(f"**{group_info['name']}**")
        for mbti_type in group_info["types"]:
            data = mbti_data[mbti_type]
            if st.button(f"{data['emoji']} {mbti_type}", key=mbti_type, use_container_width=True):
                st.session_state.selected_mbti = mbti_type

# 결과 표시
if st.session_state.selected_mbti:
    selected = st.session_state.selected_mbti
    data = mbti_data[selected]
    
    st.markdown("---")
    
    # 결과 카드
    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <div class="result-emoji">{data['emoji']}</div>
            <div class="result-type" style="color: {data['color']}">{selected}</div>
            <div class="result-nickname">{data['nickname']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 설명
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); border-radius: 20px; padding: 25px; margin: 20px auto; max-width: 900px;">
        <p style="font-size: 1.15rem; line-height: 1.8; color: #e0e0e0; text-align: center;">
            {data['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 두 개의 컬럼으로 나누기
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 특성
        st.markdown(f"""
        <div class="section-title" style="border-color: {data['color']};">
            🌟 주요 특성
        </div>
        """, unsafe_allow_html=True)
        
        traits_html = '<div class="trait-box">'
        for trait in data['traits']:
            traits_html += f'<div class="trait-item">{trait}</div>'
        traits_html += '</div>'
        st.markdown(traits_html, unsafe_allow_html=True)
    
    with col_right:
        # 추천 직업
        st.markdown(f"""
        <div class="section-title" style="border-color: {data['color']};">
            💼 추천 직업
        </div>
        """, unsafe_allow_html=True)
        
        careers_html = '<div class="career-grid">'
        for emoji, career in data['careers']:
            careers_html += f'''
            <div class="career-item">
                <div class="career-emoji">{emoji}</div>
                <div class="career-name">{career}</div>
            </div>
            '''
        careers_html += '</div>'
        st.markdown(careers_html, unsafe_allow_html=True)
    
    # 궁합
    st.markdown(f"""
    <div style="margin-top: 30px;">
        <div class="section-title" style="border-color: {data['color']};">
            💕 인간관계 궁합
        </div>
        <div class="compatibility-section">
            <div class="compat-row">
                <div class="compat-item good-match">
                    <div style="color: #22c55e; font-weight: 700; margin-bottom: 10px;">✨ 찰떡 궁합</div>
                    <div style="font-size: 1.3rem; color: white;">{', '.join(data['good_match'])}</div>
                </div>
                <div class="compat-item challenge-match">
                    <div style="color: #ef4444; font-weight: 700; margin-bottom: 10px;">💪 도전적 관계</div>
                    <div style="font-size: 1.3rem; color: white;">{', '.join(data['challenge_match'])}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 다시 선택 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([1, 1, 1])
    with col_btn[1]:
        if st.button("🔄 다른 MBTI 살펴보기", use_container_width=True):
            st.session_state.selected_mbti = None
            st.rerun()

# 푸터
st.markdown("""
<div class="footer">
    <p>🌈 Made with 💖 for Career Education</p>
    <p>모든 MBTI 유형은 소중하며, 각자의 강점이 있습니다! ✨</p>
</div>
""", unsafe_allow_html=True)
