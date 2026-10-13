# 999931440
import streamlit as st
import random
import html

st.set_page_config(
    page_title="나의 MBTI 포켓몬 단짝 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 공식 포켓몬 일러스트: PokéAPI sprites 저장소의 official-artwork 이미지
# 이미지 제공 저장소: https://github.com/PokeAPI/sprites
POKEMON = {
    "INTJ": {"ko":"뮤츠","en":"Mewtwo","id":150,"types":"에스퍼","trait":"차분한 전략가 · 깊은 통찰력","why":"혼자 생각을 정리하고 큰 그림을 보는 당신에게 뮤츠의 지적인 분위기가 잘 어울려요.\\n서로의 독립성을 존중하면서도 중요한 순간에는 든든한 팀이 될 수 있어요."},
    "INTP": {"ko":"메타몽","en":"Ditto","id":132,"types":"노말","trait":"호기심 많은 아이디어 뱅크","why":"새로운 가능성을 탐구하는 INTP처럼 메타몽은 다양한 모습으로 변신할 수 있어요.\\n정답 하나에 얽매이지 않는 상상력 넘치는 단짝이 되어 줄 거예요."},
    "ENTJ": {"ko":"리자몽","en":"Charizard","id":6,"types":"불꽃 · 비행","trait":"자신감 넘치는 리더","why":"목표를 향해 거침없이 나아가는 당신에게 리자몽의 강렬한 에너지가 찰떡이에요.\\n함께라면 어려운 도전도 멋지게 돌파할 수 있겠어요."},
    "ENTP": {"ko":"겐가","en":"Gengar","id":94,"types":"고스트 · 독","trait":"장난기 가득한 발명가","why":"기발한 발상과 유쾌한 장난을 좋아하는 ENTP에게 겐가는 최고의 파트너예요.\\n예상 밖의 모험과 웃음이 끊이지 않는 콤비가 될 거예요."},
    "INFJ": {"ko":"가디안","en":"Gardevoir","id":282,"types":"에스퍼 · 페어리","trait":"다정하고 깊이 공감하는 마음","why":"다른 사람의 마음을 섬세하게 헤아리는 당신과 가디안은 깊이 통하는 단짝이에요.\\n소중한 사람을 지키려는 마음이 닮아 서로에게 큰 위로가 되어 줄 거예요."},
    "INFP": {"ko":"이브이","en":"Eevee","id":133,"types":"노말","trait":"따뜻한 상상가 · 무한한 가능성","why":"자신만의 세계와 가능성을 소중히 여기는 INFP에게 이브이의 매력이 잘 어울려요.\\n서로의 개성을 응원하며 함께 성장하는 포근한 친구가 될 거예요."},
    "ENFJ": {"ko":"피카츄","en":"Pikachu","id":25,"types":"전기","trait":"밝은 에너지 · 따뜻한 응원단장","why":"주변 사람들을 북돋우는 당신처럼 피카츄도 밝은 에너지를 전해요.\\n함께 있으면 어디서든 분위기가 환해지고 친구들에게 힘을 줄 수 있어요."},
    "ENFP": {"ko":"푸린","en":"Jigglypuff","id":39,"types":"노말 · 페어리","trait":"사랑스러운 분위기 메이커","why":"호기심과 감성이 풍부한 ENFP에게 노래와 매력이 넘치는 푸린이 잘 맞아요.\\n평범한 하루도 신나는 추억으로 바꿔 주는 단짝이 될 거예요."},
    "ISTJ": {"ko":"꼬부기","en":"Squirtle","id":7,"types":"물","trait":"믿음직하고 성실한 친구","why":"책임감 있고 차근차근 해내는 당신에게 꼬부기의 성실함이 잘 어울려요.\\n서두르지 않고 한 걸음씩 나아가며 서로를 믿는 관계를 만들 수 있어요."},
    "ISFJ": {"ko":"해피너스","en":"Blissey","id":242,"types":"노말","trait":"포근한 돌봄이 · 든든한 수호자","why":"주변을 세심하게 챙기는 ISFJ와 해피너스는 따뜻한 마음이 닮았어요.\\n지친 날에는 서로를 보살피고 편안하게 쉴 수 있는 안식처가 되어 줄 거예요."},
    "ESTJ": {"ko":"윈디","en":"Arcanine","id":59,"types":"불꽃","trait":"당당하고 의리 있는 리더","why":"결단력 있고 책임감 강한 당신에게 믿음직한 윈디가 최고의 파트너예요.\\n약속을 지키고 친구를 지키는 모습에서 서로의 든든함을 느낄 수 있어요."},
    "ESFJ": {"ko":"푸크린","en":"Wigglytuff","id":40,"types":"노말 · 페어리","trait":"사교적인 다정함 · 분위기 메이커","why":"사람들과 어울리고 모두를 챙기는 ESFJ에게 푸크린의 사랑스러운 에너지가 어울려요.\\n모두가 편안하게 웃을 수 있는 즐거운 모임을 함께 만들 거예요."},
    "ISTP": {"ko":"루카리오","en":"Lucario","id":448,"types":"격투 · 강철","trait":"침착한 실전파 · 문제 해결사","why":"말보다 행동으로 문제를 해결하는 ISTP에게 루카리오의 침착함과 실력이 잘 맞아요.\\n위기에도 흔들리지 않고 서로의 능력을 믿는 멋진 파트너가 될 거예요."},
    "ISFP": {"ko":"님피아","en":"Sylveon","id":700,"types":"페어리","trait":"섬세한 감성 · 부드러운 매력","why":"아름다움과 감정을 소중히 여기는 ISFP에게 다정한 님피아가 잘 어울려요.\\n말하지 않아도 마음을 나누며 일상 속 작은 행복을 발견할 수 있어요."},
    "ESTP": {"ko":"갸라도스","en":"Gyarados","id":130,"types":"물 · 비행","trait":"대담한 행동파 · 강렬한 추진력","why":"망설이기보다 직접 부딪혀 보는 ESTP에게 갸라도스의 압도적인 추진력이 어울려요.\\n함께라면 스릴 넘치는 모험도 두려움 없이 즐길 수 있겠어요."},
    "ESFP": {"ko":"루차불","en":"Hawlucha","id":701,"types":"격투 · 비행","trait":"무대 체질 · 활기찬 엔터테이너","why":"사람들과 즐거움을 나누는 ESFP에게 화려한 기술을 뽐내는 루차불이 딱이에요.\\n둘이 함께라면 어디서든 시선을 사로잡고 웃음과 활력을 전할 수 있어요."},
}

MBTI_INFO = {
    "I":"내향형 · 혼자만의 시간에서 에너지를 얻어요",
    "E":"외향형 · 사람들과 어울리며 에너지를 얻어요",
    "N":"직관형 · 가능성과 아이디어를 즐겨요",
    "S":"감각형 · 구체적인 경험과 현실을 중시해요",
    "T":"사고형 · 논리와 분석을 중요하게 생각해요",
    "F":"감정형 · 마음과 가치를 중요하게 생각해요",
    "J":"판단형 · 계획하고 정리하는 걸 좋아해요",
    "P":"인식형 · 유연하게 탐색하는 걸 좋아해요",
}

st.markdown("""
<style>
:root { --cream:#fff9e9; --yellow:#ffdc75; --gold:#e6a928; --brown:#59452e; --pink:#ffe8d9; }
.stApp { background: radial-gradient(circle at top left,#fff0bc 0,transparent 35%), var(--cream); color:var(--brown); }
html, body, [class*="css"] { font-family:'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; }
.block-container { max-width: 850px; padding-top: 2rem; padding-bottom: 3rem; }
.hero { text-align:center; padding: 1.6rem 1rem 1.2rem; border:2px solid #f4d77e; border-radius:28px; background:rgba(255,255,255,.72); box-shadow:0 10px 30px #b98d2820; }
.hero .eyebrow { color:#9c7621; font-weight:900; letter-spacing:2px; font-size: .9rem; }
.hero h1 { font-family:'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; font-size:clamp(2.2rem,6vw,3.5rem); color:#5a4427; line-height:1.2; margin:.45rem 0; }
.hero p { font-size:1.08rem; line-height:1.8; margin:.4rem 0; }
.stSelectbox label, .stRadio label, .stMarkdown { color:#59452e !important; }
.result-card { background:#fffefa; border:2px solid #f1d889; border-radius:28px; padding:1.5rem; box-shadow:0 12px 28px #8d6b2015; }
.pill { display:inline-block; background:#fff0bb; color:#795716; padding:.45rem .85rem; border-radius:999px; font-weight:800; margin:.2rem .2rem .2rem 0; }
.pokemon-name { font-family:'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; font-size:2.3rem; color:#59452e; margin:.25rem 0; }
.reason { background:#fff5d9; border-radius:18px; padding:1rem 1.2rem; line-height:1.9; font-size:1.05rem; white-space:pre-line; }
.stButton > button { border:0; border-radius:16px; background:#f4c84e; color:#4d391b; font-size:1.12rem; font-weight:900; padding:.75rem 1.2rem; min-height:3.2rem; }
.stButton > button:hover { background:#edb92f; color:#3f2c12; border:0; }
.small-note { font-size:.88rem; color:#806b4a; line-height:1.7; }
div[data-testid="stImage"] img { filter: drop-shadow(0 10px 12px #bda05b20); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">✨ YOUR POKÉMON BESTIE ✨</div>
  <h1>나의 MBTI 포켓몬 단짝 찾기</h1>
  <p>나와 찰떡궁합인 포켓몬은 누구일까요?<br>MBTI를 고르고 운명의 단짝을 만나 보세요!</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.markdown("### 🌼 먼저, 나의 MBTI를 골라 주세요")
types = list(POKEMON.keys())
cols = st.columns(4)
for i, letter in enumerate(["I/E", "N/S", "T/F", "J/P"]):
    with cols[i]:
        st.caption(["에너지 방향","정보를 보는 방식","결정 기준","생활 방식"][i])

selected = st.selectbox(
    "MBTI 유형",
    options=types,
    index=types.index(st.session_state.get("mbti", "INFP")) if st.session_state.get("mbti", "INFP") in types else 5,
    format_func=lambda x: f"{x}  ·  { {'INTJ':'전략가','INTP':'논리술사','ENTJ':'통솔자','ENTP':'변론가','INFJ':'옹호자','INFP':'중재자','ENFJ':'선도자','ENFP':'활동가','ISTJ':'현실주의자','ISFJ':'수호자','ESTJ':'경영자','ESFJ':'집정관','ISTP':'장인','ISFP':'모험가','ESTP':'사업가','ESFP':'연예인'}[x] }",
    label_visibility="collapsed",
)
st.session_state["mbti"] = selected

with st.expander("💡 내 MBTI 글자가 뜻하는 것"):
    st.write(" · ".join(MBTI_INFO[c] for c in selected))

if st.button("💛 내 단짝 포켓몬 찾기!", use_container_width=True):
    st.session_state["show_result"] = True
    st.session_state["last_result"] = selected

if st.session_state.get("show_result", False):
    mbti = st.session_state.get("last_result", selected)
    p = POKEMON[mbti]
    st.balloons()
    st.snow()
    st.markdown("<div style='text-align:center;font-size:1.1rem;font-weight:900;color:#9a721a;margin:1.2rem 0'>🎉 축하해요! 운명의 단짝을 찾았어요! 🎉</div>", unsafe_allow_html=True)
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center'><span class='pill'>나의 MBTI · {mbti}</span><br><div class='pokemon-name'>{p['ko']} <span style='font-size:1.25rem'>({p['en']})</span></div><div style='color:#8c7048;font-weight:700'>{p['trait']}</div></div>", unsafe_allow_html=True)
    # PokeAPI sprites 저장소의 고해상도 공식 아트워크
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{p['id']}.png"
    st.image(image_url, width=310, caption=f"{p['ko']} · Official Artwork")
    st.markdown(f"<div style='text-align:center'><span class='pill'>타입 · {p['types']}</span><span class='pill'>단짝 궁합 💛</span></div>", unsafe_allow_html=True)
    st.markdown("#### 🌟 너와 닮은 점")
    st.markdown(f"<div class='reason'>{p['why']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("🔄 다른 MBTI도 찾아보기", use_container_width=True):
        st.session_state["show_result"] = False
        st.rerun()

st.write("")
st.markdown("""
<div class="small-note" style="text-align:center">
🍯 이 결과는 재미를 위한 MBTI 테마 추천이에요.<br>
포켓몬 공식 일러스트는 PokéAPI sprites 저장소에서 불러옵니다.
</div>
""", unsafe_allow_html=True)
