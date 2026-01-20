import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 진로 탐색기",
    page_icon="🧭",
    layout="wide"
)

# CSS 스타일링 - 깔끔한 디자인
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stApp {
        background: #f8fafc;
    }
    
    .main-header {
        text-align: center;
        padding: 40px 0 30px 0;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
    }
    
    .main-subtitle {
        font-size: 1.1rem;
        color: #64748b;
    }
    
    .mbti-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        max-width: 700px;
        margin: 0 auto;
    }
    
    .group-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-align: center;
        padding: 8px;
        margin-bottom: 5px;
    }
    
    .result-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .profile-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 24px;
    }
    
    .profile-header {
        display: flex;
        align-items: center;
        gap: 24px;
        margin-bottom: 24px;
        padding-bottom: 24px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .profile-emoji {
        font-size: 4rem;
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        border-radius: 20px;
        padding: 20px;
    }
    
    .profile-info h1 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 8px 0;
    }
    
    .profile-nickname {
        font-size: 1.2rem;
        color: #64748b;
        margin: 0;
    }
    
    .profile-description {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #475569;
    }
    
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .trait-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .trait-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 18px;
        background: #f8fafc;
        border-radius: 12px;
        font-size: 0.95rem;
        color: #334155;
    }
    
    .career-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
    }
    
    .career-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        padding: 20px 16px;
        background: #f8fafc;
        border-radius: 14px;
        transition: all 0.2s ease;
    }
    
    .career-item:hover {
        background: #f1f5f9;
        transform: translateY(-2px);
    }
    
    .career-emoji {
        font-size: 2rem;
    }
    
    .career-name {
        font-size: 0.9rem;
        font-weight: 500;
        color: #334155;
        text-align: center;
    }
    
    .compat-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }
    
    .compat-card {
        padding: 20px;
        border-radius: 14px;
        text-align: center;
    }
    
    .compat-good {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1px solid #a7f3d0;
    }
    
    .compat-challenge {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 1px solid #fecaca;
    }
    
    .compat-label {
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    .compat-good .compat-label { color: #059669; }
    .compat-challenge .compat-label { color: #dc2626; }
    
    .compat-types {
        display: flex;
        justify-content: center;
        gap: 12px;
    }
    
    .compat-type {
        padding: 10px 18px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .compat-good .compat-type {
        background: white;
        color: #059669;
    }
    
    .compat-challenge .compat-type {
        background: white;
        color: #dc2626;
    }
    
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #2563eb;
        transform: translateY(-1px);
    }
    
    /* 그룹별 버튼 색상 */
    .analyst-btn button { background: #8b5cf6 !important; }
    .analyst-btn button:hover { background: #7c3aed !important; }
    
    .diplomat-btn button { background: #10b981 !important; }
    .diplomat-btn button:hover { background: #059669 !important; }
    
    .sentinel-btn button { background: #3b82f6 !important; }
    .sentinel-btn button:hover { background: #2563eb !important; }
    
    .explorer-btn button { background: #f59e0b !important; }
    .explorer-btn button:hover { background: #d97706 !important; }
    
    div[data-testid="stMarkdownContainer"] p {
        color: #475569;
    }
</style>
""", unsafe_allow_html=True)

# MBTI 데이터
mbti_data = {
    "INTJ": {
        "emoji": "🧠",
        "nickname": "전략가 (Architect)",
        "group": "analyst",
        "description": "독립적이고 전략적인 사고를 하는 INTJ는 항상 큰 그림을 보며 장기적인 계획을 세웁니다. 높은 기준을 가지고 있으며, 복잡한 문제를 해결하는 데 탁월한 능력을 발휘합니다. 지식에 대한 강한 열망과 함께 효율성을 추구합니다.",
        "traits": [
            ("🎯", "목표 지향적이며 장기적 비전 보유"),
            ("🔬", "분석적이고 논리적인 사고력"),
            ("📚", "지식과 자기계발에 대한 강한 열망"),
            ("🏔️", "높은 기준과 완벽주의 성향"),
            ("🤔", "독립적이며 자율적으로 일하는 것을 선호")
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
        "nickname": "논리술사 (Logician)",
        "group": "analyst",
        "description": "끝없는 호기심을 가진 INTP는 이론과 아이디어의 세계에서 살아갑니다. 논리적 분석을 통해 복잡한 문제의 본질을 파악하고, 혁신적인 해결책을 찾아냅니다. 창의적 사고와 지적 탐구를 즐깁니다.",
        "traits": [
            ("💡", "창의적이고 혁신적인 사고방식"),
            ("🧩", "복잡한 문제 해결에 탁월"),
            ("📖", "이론적이고 추상적인 개념에 관심"),
            ("🎨", "독창적인 아이디어 생성 능력"),
            ("🔍", "끊임없는 분석과 탐구 정신")
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
        "nickname": "통솔자 (Commander)",
        "group": "analyst",
        "description": "타고난 리더인 ENTJ는 카리스마와 자신감으로 사람들을 이끕니다. 효율성을 추구하며 목표 달성을 위해 체계적으로 계획하고 실행합니다. 도전을 즐기고 성과를 중시합니다.",
        "traits": [
            ("👔", "강력한 리더십과 추진력"),
            ("📋", "체계적이고 조직적인 업무 처리"),
            ("🎤", "설득력 있는 의사소통 능력"),
            ("⚡", "결단력과 빠른 의사결정"),
            ("🏆", "성취 지향적이며 높은 야망")
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
        "nickname": "변론가 (Debater)",
        "group": "analyst",
        "description": "기발한 아이디어와 날카로운 재치를 가진 ENTP는 토론을 즐기고 관습에 도전합니다. 새로운 가능성을 탐구하며 창의적인 해결책을 찾는 것을 좋아합니다.",
        "traits": [
            ("🗣️", "뛰어난 토론 및 설득 능력"),
            ("🌟", "창의적이고 혁신적인 사고"),
            ("🎢", "새로운 도전과 변화를 즐김"),
            ("🧠", "빠른 두뇌 회전과 재치"),
            ("🔄", "유연하고 적응력이 뛰어남")
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
        "nickname": "옹호자 (Advocate)",
        "group": "diplomat",
        "description": "이상주의적이고 원칙적인 INFJ는 깊은 통찰력으로 사람들의 마음을 읽습니다. 조용하지만 강한 신념을 가지고 세상을 더 나은 곳으로 만들고자 노력합니다.",
        "traits": [
            ("💫", "깊은 통찰력과 직관"),
            ("❤️", "타인에 대한 공감 능력"),
            ("🌍", "이상주의적이며 가치 지향적"),
            ("✍️", "창의적인 표현력"),
            ("🤝", "의미 있는 관계 추구")
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
        "nickname": "중재자 (Mediator)",
        "group": "diplomat",
        "description": "시적인 영혼을 가진 INFP는 자신만의 내면 세계에서 살아갑니다. 진정성과 창의성을 중요시하며, 이상적인 세상을 꿈꿉니다.",
        "traits": [
            ("🌈", "풍부한 상상력과 창의성"),
            ("💝", "깊은 감정과 공감 능력"),
            ("📝", "자기표현에 대한 욕구"),
            ("🕊️", "평화를 추구하며 갈등 회피"),
            ("✨", "진정성과 개성 중시")
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
        "nickname": "선도자 (Protagonist)",
        "group": "diplomat",
        "description": "따뜻한 카리스마를 가진 ENFJ는 타인의 성장을 돕는 것에서 기쁨을 느낍니다. 영감을 주는 리더로서 사람들을 하나로 모읍니다.",
        "traits": [
            ("🤗", "뛰어난 대인관계 능력"),
            ("🎯", "타인의 잠재력을 발견하고 격려"),
            ("💬", "설득력 있는 소통 능력"),
            ("🌺", "이타적이며 헌신적"),
            ("🎪", "조직력과 리더십")
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
        "nickname": "활동가 (Campaigner)",
        "group": "diplomat",
        "description": "열정적이고 창의적인 ENFP는 어디서든 가능성을 발견합니다. 사람들에게 영감을 주고, 새로운 아이디어로 세상을 밝게 만듭니다.",
        "traits": [
            ("🎉", "열정적이고 에너지 넘침"),
            ("🌈", "창의적이고 상상력이 풍부"),
            ("🤝", "사교적이며 친화력이 높음"),
            ("🎨", "다양한 관심사와 재능"),
            ("💫", "낙관적이며 긍정적")
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
        "nickname": "현실주의자 (Logistician)",
        "group": "sentinel",
        "description": "신뢰할 수 있고 책임감 있는 ISTJ는 전통과 규칙을 존중합니다. 꼼꼼하고 체계적으로 일을 처리하며, 맡은 일은 반드시 완수합니다.",
        "traits": [
            ("📌", "책임감이 강하고 신뢰할 수 있음"),
            ("📊", "체계적이고 꼼꼼한 업무 처리"),
            ("⚖️", "공정하고 논리적인 판단"),
            ("🏆", "끈기와 인내심"),
            ("🔒", "전통과 규칙 존중")
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
        "nickname": "수호자 (Defender)",
        "group": "sentinel",
        "description": "헌신적이고 따뜻한 ISFJ는 조용히 타인을 돌봅니다. 세심한 배려와 성실함으로 주변 사람들에게 안정감을 줍니다.",
        "traits": [
            ("🤗", "헌신적이고 배려심이 깊음"),
            ("📝", "세심하고 꼼꼼한 성격"),
            ("🏠", "가정과 전통 중시"),
            ("🤝", "협조적이며 팀워크 중시"),
            ("💪", "책임감과 인내심")
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
        "nickname": "경영자 (Executive)",
        "group": "sentinel",
        "description": "질서와 전통을 수호하는 ESTJ는 타고난 조직 관리자입니다. 명확한 규칙 아래서 효율적으로 일하며, 팀을 이끄는 데 능숙합니다.",
        "traits": [
            ("👔", "강한 리더십과 조직력"),
            ("📋", "체계적이고 효율적인 업무 처리"),
            ("⚡", "결단력과 실행력"),
            ("🎯", "목표 지향적이며 성과 중시"),
            ("⚖️", "공정함과 정직함")
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
        "nickname": "집정관 (Consul)",
        "group": "sentinel",
        "description": "따뜻하고 사교적인 ESFJ는 타인을 돌보는 것에서 기쁨을 찾습니다. 조화로운 환경을 만들고 사람들을 하나로 모읍니다.",
        "traits": [
            ("🤝", "사교적이고 친화력이 높음"),
            ("💕", "타인에 대한 배려와 관심"),
            ("🎊", "조화와 협력 중시"),
            ("📅", "계획적이고 조직적"),
            ("🏆", "인정받고 싶은 욕구")
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
        "nickname": "장인 (Virtuoso)",
        "group": "explorer",
        "description": "냉철하고 분석적인 ISTP는 손으로 직접 만드는 것을 즐깁니다. 위기 상황에서 침착하게 문제를 해결하는 실용적인 문제 해결사입니다.",
        "traits": [
            ("🔧", "실용적이고 손재주가 좋음"),
            ("🧊", "침착하고 냉정한 판단력"),
            ("🔍", "분석적인 문제 해결 능력"),
            ("🏍️", "모험심과 스릴 추구"),
            ("⚡", "효율성과 논리 중시")
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
        "nickname": "모험가 (Adventurer)",
        "group": "explorer",
        "description": "조용하고 감성적인 ISFP는 아름다움을 추구하는 예술가입니다. 현재를 즐기며 자신만의 방식으로 세상을 표현합니다.",
        "traits": [
            ("🎨", "예술적 감각과 심미안"),
            ("🌸", "온화하고 친절한 성품"),
            ("🦋", "자유로운 영혼"),
            ("💫", "현재를 즐기는 삶"),
            ("🤫", "조용하지만 열정적")
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
        "nickname": "사업가 (Entrepreneur)",
        "group": "explorer",
        "description": "에너지 넘치고 행동 지향적인 ESTP는 순간을 살아갑니다. 빠른 판단력과 적응력으로 어떤 상황에서도 기회를 포착합니다.",
        "traits": [
            ("⚡", "에너지 넘치고 활동적"),
            ("🎲", "모험심과 위험 감수"),
            ("🗣️", "사교적이며 설득력 있음"),
            ("🎯", "실용적인 문제 해결"),
            ("🏃", "즉흥적이고 유연함")
        ],
        "careers": [
            ("💼", "사업가"),
            ("🎤", "영업 전문가"),
            ("🚔", "경찰관"),
            ("🏋️", "피트니스 트레이너"),
            ("📈", "주식 트레이더"),
            ("🎬", "스턴트맨")
        ],
        "good_match": ["ISTJ", "ISFJ"],
        "challenge_match": ["INFJ", "ENFJ"]
    },
    "ESFP": {
        "emoji": "🎉",
        "nickname": "연예인 (Entertainer)",
        "group": "explorer",
        "description": "밝고 즐거운 에너지의 ESFP는 어디서든 분위기를 띄웁니다. 현재를 즐기고 사람들과 함께하는 것을 사랑하는 타고난 엔터테이너입니다.",
        "traits": [
            ("🎊", "밝고 긍정적인 에너지"),
            ("🎭", "뛰어난 엔터테인먼트 능력"),
            ("🤗", "사교적이고 친화력 최고"),
            ("🎪", "즉흥적이고 재미 추구"),
            ("💃", "감각적이고 세련됨")
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

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🧭 MBTI 진로 탐색기</h1>
    <p class="main-subtitle">나의 성격 유형에 맞는 직업과 관계를 찾아보세요</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'selected_mbti' not in st.session_state:
    st.session_state.selected_mbti = None

# MBTI 선택 섹션
st.markdown("### MBTI 유형 선택")

groups = {
    "analyst": {"name": "🧠 분석가형", "types": ["INTJ", "INTP", "ENTJ", "ENTP"], "class": "analyst-btn"},
    "diplomat": {"name": "💚 외교관형", "types": ["INFJ", "INFP", "ENFJ", "ENFP"], "class": "diplomat-btn"},
    "sentinel": {"name": "🛡️ 관리자형", "types": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"], "class": "sentinel-btn"},
    "explorer": {"name": "🎯 탐험가형", "types": ["ISTP", "ISFP", "ESTP", "ESFP"], "class": "explorer-btn"}
}

col1, col2, col3, col4 = st.columns(4)
columns = [col1, col2, col3, col4]

for i, (group_key, group_info) in enumerate(groups.items()):
    with columns[i]:
        st.markdown(f"<p class='group-label'>{group_info['name']}</p>", unsafe_allow_html=True)
        for mbti_type in group_info["types"]:
            st.markdown(f"<div class='{group_info['class']}'>", unsafe_allow_html=True)
            if st.button(f"{mbti_data[mbti_type]['emoji']} {mbti_type}", key=mbti_type, use_container_width=True):
                st.session_state.selected_mbti = mbti_type
            st.markdown("</div>", unsafe_allow_html=True)

# 결과 표시
if st.session_state.selected_mbti:
    selected = st.session_state.selected_mbti
    data = mbti_data[selected]
    
    st.markdown("---")
    
    # 프로필 카드
    st.markdown(f"""
    <div class="result-container">
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-emoji">{data['emoji']}</div>
                <div class="profile-info">
                    <h1>{selected}</h1>
                    <p class="profile-nickname">{data['nickname']}</p>
                </div>
            </div>
            <p class="profile-description">{data['description']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 특성 & 직업 섹션
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">✨ 주요 특성</div>
        </div>
        """, unsafe_allow_html=True)
        
        traits_html = '<div class="trait-list">'
        for emoji, trait in data['traits']:
            traits_html += f'<div class="trait-item"><span>{emoji}</span> {trait}</div>'
        traits_html += '</div>'
        st.markdown(traits_html, unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">💼 추천 직업</div>
        </div>
        """, unsafe_allow_html=True)
        
        careers_html = '<div class="career-grid">'
        for emoji, career in data['careers']:
            careers_html += f'''
            <div class="career-item">
                <span class="career-emoji">{emoji}</span>
                <span class="career-name">{career}</span>
            </div>
            '''
        careers_html += '</div>'
        st.markdown(careers_html, unsafe_allow_html=True)
    
    # 궁합 섹션
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-card">
        <div class="section-title">💕 성격 궁합</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="compat-section">
        <div class="compat-card compat-good">
            <div class="compat-label">✨ 잘 맞는 유형</div>
            <div class="compat-types">
                {''.join([f'<span class="compat-type">{t}</span>' for t in data['good_match']])}
            </div>
        </div>
        <div class="compat-card compat-challenge">
            <div class="compat-label">💪 노력이 필요한 유형</div>
            <div class="compat-types">
                {''.join([f'<span class="compat-type">{t}</span>' for t in data['challenge_match']])}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 다시 선택 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([1, 1, 1])
    with col_btn[1]:
        if st.button("🔄 다른 유형 살펴보기", use_container_width=True):
            st.session_state.selected_mbti = None
            st.rerun()

# 푸터
st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #94a3b8; font-size: 0.9rem;">
    <p>모든 MBTI 유형은 고유한 강점을 가지고 있습니다 ✨</p>
</div>
""", unsafe_allow_html=True)
