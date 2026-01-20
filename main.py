import streamlit as st

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 CSS 스타일링 (화려하고 예쁜 디자인)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="꿈을 찾는 MBTI 진로 나침반",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS 주입
st.markdown("""
    <style>
    /* 전체 폰트 및 배경 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 메인 타이틀 그라데이션 효과 */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF512F, #DD2476, #4A00E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
    }

    /* 서브 타이틀 스타일 */
    .sub-header {
        color: #4A00E0;
        font-weight: 700;
        border-bottom: 2px solid #DD2476;
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* 카드 스타일 (Box Design) */
    .info-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #DD2476;
        transition: transform 0.3s ease;
    }
    .info-card:hover {
        transform: translateY(-5px);
    }

    /* 직업 추천 태그 스타일 */
    .job-tag {
        display: inline-block;
        background: linear-gradient(90deg, #8E2DE2, #4A00E0);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* 사이드바 스타일 조정 */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    
    /* 이모지 크기 키우기 */
    .emoji-large {
        font-size: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MBTI 데이터베이스 (특성 및 추천 직업)
# -----------------------------------------------------------------------------
mbti_data = {
    # 분석가형
    "INTJ": {
        "name": "용의주도한 전략가 (Architect)",
        "emoji": "🧠",
        "keywords": ["#비전", "#독립적", "#논리적", "#계획적"],
        "desc": "상상력이 풍부하며 철두철미한 계획을 세우는 전략가형입니다. 지적 호기심이 많고 복잡한 문제를 해결하는 것을 즐깁니다.",
        "jobs": ["투자 은행가", "소프트웨어 개발자", "변호사", "과학자", "경영 컨설턴트", "데이터 분석가"]
    },
    "INTP": {
        "name": "논리적인 사색가 (Logician)",
        "emoji": "🧪",
        "keywords": ["#호기심", "#분석", "#아이디어", "#탐구"],
        "desc": "끊임없이 새로운 지식에 목말라하는 혁신가형입니다. 추상적인 개념을 다루는 것을 좋아하며 독창적입니다.",
        "jobs": ["컴퓨터 프로그래머", "수학자", "대학교수", "연구원", "철학자", "시스템 엔지니어"]
    },
    "ENTJ": {
        "name": "대담한 통솔자 (Commander)",
        "emoji": "🦁",
        "keywords": ["#리더십", "#결단력", "#목표지향", "#효율성"],
        "desc": "대담하고 상상력이 풍부하며 강한 의지의 지도자형입니다. 장기적인 계획을 수립하고 목표를 달성하는 데 능숙합니다.",
        "jobs": ["기업 임원(CEO)", "변호사", "경영 컨설턴트", "정치인", "프로젝트 매니저", "창업가"]
    },
    "ENTP": {
        "name": "뜨거운 논쟁을 즐기는 변론가 (Debater)",
        "emoji": "🔥",
        "keywords": ["#창의적", "#도전", "#언변", "#다재다능"],
        "desc": "지적인 도전을 두려워하지 않는 똑똑한 호기심형입니다. 기존의 틀을 깨고 새로운 가능성을 발견하는 것을 즐깁니다.",
        "jobs": ["발명가", "벤처 투자자", "저널리스트", "마케팅 디렉터", "정치 평론가", "크리에이티브 디렉터"]
    },
    # 외교관형
    "INFJ": {
        "name": "선의의 옹호자 (Advocate)",
        "emoji": "🧙‍♂️",
        "keywords": ["#통찰력", "#이타주의", "#신념", "#창의성"],
        "desc": "조용하고 신비로우며 샘솟는 영감으로 타인에게 영향을 줍니다. 깊은 통찰력으로 사람들의 성장을 돕는 것을 좋아합니다.",
        "jobs": ["심리 상담가", "작가", "사회복지사", "인사 담당자(HR)", "예술가", "특수교사"]
    },
    "INFP": {
        "name": "열정적인 중재자 (Mediator)",
        "emoji": "🧚",
        "keywords": ["#이상주의", "#낭만", "#공감", "#예술"],
        "desc": "상냥하고 이타적이며 낭만적인 성향을 가졌습니다. 자신만의 가치관을 중요시하며 창의적인 활동을 통해 자아를 실현합니다.",
        "jobs": ["그래픽 디자이너", "작가/시인", "심리학자", "사서", "편집자", "일러스트레이터"]
    },
    "ENFJ": {
        "name": "정의로운 사회운동가 (Protagonist)",
        "emoji": "🛡️",
        "keywords": ["#카리스마", "#영향력", "#소통", "#협동"],
        "desc": "청중을 사로잡고 의욕을 불어넣는 카리스마 넘치는 지도자형입니다. 타인의 잠재력을 이끌어내는 데 탁월합니다.",
        "jobs": ["홍보 전문가(PR)", "세일즈 매니저", "정치인", "기업 교육 강사", "방송 PD", "아나운서"]
    },
    "ENFP": {
        "name": "재기발랄한 활동가 (Campaigner)",
        "emoji": "🎉",
        "keywords": ["#열정", "#자유", "#상상력", "#인기"],
        "desc": "창의적이고 활발하며 웃음이 끊이지 않는 분위기 메이커입니다. 새로운 사람을 만나고 새로운 경험을 하는 것을 사랑합니다.",
        "jobs": ["엔터테이너", "마케터", "이벤트 기획자", "여행 가이드", "저널리스트", "상품 기획자(MD)"]
    },
    # 관리자형
    "ISTJ": {
        "name": "청렴결백한 논리주의자 (Logistician)",
        "emoji": "📋",
        "keywords": ["#책임감", "#현실적", "#전통", "#질서"],
        "desc": "사실에 근거하여 사고하며 이성적이고 매사에 신중합니다. 한 번 시작한 일은 끝까지 책임지는 성실함이 무기입니다.",
        "jobs": ["회계사", "공무원", "감사관", "법조인", "데이터베이스 관리자", "약사"]
    },
    "ISFJ": {
        "name": "용감한 수호자 (Defender)",
        "emoji": "🛡️",
        "keywords": ["#헌신", "#인내", "#성실", "#따뜻함"],
        "desc": "소중한 이들을 지키기 위해 헌신하는 성격입니다. 조용하고 차분하지만, 맡은 바 임무에는 강한 책임감을 보입니다.",
        "jobs": ["간호사", "초등학교 교사", "사회복지사", "사서", "인사 관리자", "치과 위생사"]
    },
    "ESTJ": {
        "name": "엄격한 관리자 (Executive)",
        "emoji": "⚖️",
        "keywords": ["#규칙", "#지도력", "#조직", "#현실적"],
        "desc": "사물과 사람을 관리하는 데 뛰어난 능력을 지닌 경영자형입니다. 체계적이고 규칙을 준수하며 효율성을 최우선으로 합니다.",
        "jobs": ["군 장교", "경찰관", "판사", "재무 이사", "프로젝트 매니저", "은행 지점장"]
    },
    "ESFJ": {
        "name": "사교적인 외교관 (Consul)",
        "emoji": "🤝",
        "keywords": ["#친목", "#봉사", "#조화", "#인기"],
        "desc": "타인에게 세심한 관심을 쏟으며 사교적인 성격입니다. 사람들과 어울리며 돕는 과정에서 에너지를 얻습니다.",
        "jobs": ["항공 승무원", "호텔 지배인", "유치원 교사", "홍보 전문가", "의료 코디네이터", "파티 플래너"]
    },
    # 탐험가형
    "ISTP": {
        "name": "만능 재주꾼 (Virtuoso)",
        "emoji": "🔧",
        "keywords": ["#기술", "#도구", "#냉철", "#모험"],
        "desc": "대담하고 현실적인 성향으로 도구 사용에 능숙합니다. 호기심이 많고 상황 적응력이 뛰어나 문제 해결에 강합니다.",
        "jobs": ["파일럿", "소프트웨어 엔지니어", "응급구조사", "토목 기사", "정비사", "빅데이터 전문가"]
    },
    "ISFP": {
        "name": "호기심 많은 예술가 (Adventurer)",
        "emoji": "🎨",
        "keywords": ["#예술", "#감성", "#온화", "#현재"],
        "desc": "항상 새로운 것을 찾아 시도하거나 도전할 준비가 되어 있는 융통성 있는 성격입니다. 따뜻한 감성을 예술로 승화시킵니다.",
        "jobs": ["패션 디자이너", "보석 세공사", "작곡가", "수의사", "플로리스트", "셰프"]
    },
    "ESTP": {
        "name": "모험을 즐기는 사업가 (Entrepreneur)",
        "emoji": "🚀",
        "keywords": ["#스릴", "#에너지", "#직관", "#행동"],
        "desc": "위험을 기꺼이 감수하는 성격으로 영리하고 에너지가 넘칩니다. 순간의 포착 능력이 뛰어나며 문제를 즉각적으로 해결합니다.",
        "jobs": ["주식 중개인", "스포츠 에이전트", "소방관", "여행 가이드", "영업 전문가", "건축가"]
    },
    "ESFP": {
        "name": "자유로운 영혼의 연예인 (Entertainer)",
        "emoji": "💃",
        "keywords": ["#스타", "#긍정", "#즉흥", "#유머"],
        "desc": "주위에 있으면 인생이 지루할 새가 없을 정도로 즉흥적이고 열정이 넘칩니다. 사람들을 즐겁게 하는 타고난 엔터테이너입니다.",
        "jobs": ["배우/가수", "패션 머천다이저", "인테리어 디자이너", "놀이 치료사", "여행 코디네이터", "파티 플래너"]
    }
}

# -----------------------------------------------------------------------------
# 3. 사이드바 구성
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4792/4792929.png", width=100)
    st.markdown("## 👋 내 MBTI 선택하기")
    
    # MBTI 선택 박스
    selected_mbti = st.selectbox(
        "당신의 MBTI 유형을 선택해주세요!",
        options=list(mbti_data.keys()),
        index=0
    )
    
    st.write("---")
    st.markdown("### 🌟 진로 탐색 꿀팁")
    st.info("""
    MBTI는 절대적인 지표가 아닙니다!
    자신의 성향을 이해하고,
    흥미로운 직업을 탐색하는
    도구로만 활용해보세요. :)
    """)

# -----------------------------------------------------------------------------
# 4. 메인 컨텐츠 영역
# -----------------------------------------------------------------------------

# 타이틀 표시
st.markdown('<div class="main-title">✨ 나의 MBTI 진로 나침반 ✨</div>', unsafe_allow_html=True)

# 선택된 데이터 가져오기
data = mbti_data[selected_mbti]

# 메인 레이아웃 (2단 분리: 왼쪽 설명, 오른쪽 키워드)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f'<div class="sub-header">{data["emoji"]} 당신의 유형은?</div>', unsafe_allow_html=True)
    st.markdown(f"### **{selected_mbti} : {data['name']}**")
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write(data['desc'])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="sub-header">🔑 핵심 키워드</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card" style="text-align:center;">', unsafe_allow_html=True)
    for keyword in data['keywords']:
        st.markdown(f"**{keyword}**")
    st.markdown('</div>', unsafe_allow_html=True)

# 추천 직업 섹션 (전체 너비)
st.markdown('<div class="
