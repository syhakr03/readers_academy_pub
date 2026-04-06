import streamlit as st
from datetime import date, timedelta
import base64

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="독서 교습소 - 학부모/학생 포털",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #F7F8FA; }
[data-testid="collapsedControl"]   { display: none; }

.greeting     { font-size: 17px; font-weight: 700; color: #111827; }
.greeting-sub { font-size: 12px; color: #6B7280; margin-top: 2px; }

.card {
    background: #fff; border: 0.5px solid #E5E7EB;
    border-radius: 16px; padding: 16px 18px; margin-bottom: 14px;
}
.card-title {
    font-size: 11px; font-weight: 600; color: #6B7280;
    letter-spacing: .5px; text-transform: uppercase; margin-bottom: 12px;
}
.metric-box {
    background: #F7F8FA; border-radius: 12px;
    padding: 12px; text-align: center;
}
.metric-box .m-label { font-size: 11px; color: #6B7280; margin-bottom: 4px; }
.metric-box .m-val   { font-size: 24px; font-weight: 700; }
.metric-box .m-sub   { font-size: 11px; color: #6B7280; margin-top: 2px; }

.row-item {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 0; border-top: 0.5px solid #F3F4F6; font-size: 13px;
}
.row-item:first-child { border-top: none; padding-top: 0; }
.row-label { color: #6B7280; }
.row-val   { font-weight: 600; color: #111827; }

.badge { font-size: 11px; padding: 3px 10px; border-radius: 99px; font-weight: 600; }
.badge-green { background: #EAF3DE; color: #27500A; }
.badge-red   { background: #FCEBEB; color: #791F1F; }
.badge-amber { background: #FAEEDA; color: #633806; }
.badge-blue  { background: #E6F1FB; color: #0C447C; }
.badge-new   { background: #FEF9C3; color: #92400E;
               font-size: 10px; padding: 2px 7px; border-radius: 99px; font-weight: 600; }

.progress-bg   { background: #F3F4F6; border-radius: 99px;
                 height: 7px; margin: 6px 0 3px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 99px; }

.memo-box {
    background: #F7F8FA; border-radius: 12px; padding: 12px 14px;
    font-size: 13px; color: #374151; line-height: 1.6;
    border-left: 3px solid #378ADD;
}

/* 상단 작은 원형 사진 */
.photo-sm {
    width: 52px; height: 52px; border-radius: 50%;
    overflow: hidden; border: 2px solid #E5E7EB;
    margin-top: 2px;
}
.photo-sm img { width: 100%; height: 100%; object-fit: cover; }
.initial-sm {
    width: 52px; height: 52px; border-radius: 50%;
    background: #B5D4F4; color: #0C447C;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 700; margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── 샘플 데이터 ──────────────────────────────────────────────
today = date.today()

STUDENTS = {
    "김민준": {
        "학년": "초4", "반": "초등 독서 A반", "담당": "원장",
        "등록일": "2025-03-01", "연락처": "010-1234-5678",
        "books": [
            {"제목": "어린왕자", "총": 120, "현재": 80, "시작": "2025-03-20",
             "완독": False,
             "히스토리": [("2025-04-03", 20), ("2025-03-27", 30), ("2025-03-20", 30)]},
            {"제목": "샬롯의 거미줄", "총": 180, "현재": 180, "시작": "2025-02-10",
             "완독": True,
             "히스토리": [("2025-03-10", 50), ("2025-02-25", 60), ("2025-02-10", 70)]},
        ],
        "memo": "독해력이 꾸준히 향상되고 있어요. 어휘력 연습을 병행하면 더욱 좋을 것 같습니다.",
        "memo_date": "2025-04-03",
        "attendance": [
            ("2025-04-03", "초등 독서 A반", "출석"),
            ("2025-03-27", "초등 독서 A반", "결석"),
            ("2025-03-20", "초등 독서 A반", "출석"),
            ("2025-03-13", "초등 독서 A반", "출석"),
            ("2025-03-06", "초등 독서 A반", "지각"),
        ],
        "absent_reason": {"2025-03-27": "발열로 인한 결석 (학부모 연락)"},
        "payments": [
            {"월": "2025-04", "금액": 150000, "상태": "납부완료", "납부일": "2025-04-01"},
            {"월": "2025-03", "금액": 150000, "상태": "납부완료", "납부일": "2025-03-03"},
            {"월": "2025-02", "금액": 150000, "상태": "납부완료", "납부일": "2025-02-02"},
        ],
    },
    "최수아": {
        "학년": "중1", "반": "중등 독서 A반", "담당": "원장",
        "등록일": "2025-03-10", "연락처": "010-9876-5432",
        "books": [
            {"제목": "파과", "총": 300, "현재": 200, "시작": "2025-03-10",
             "완독": False,
             "히스토리": [("2025-04-03", 50), ("2025-03-25", 80), ("2025-03-10", 70)]},
        ],
        "memo": "심화 독서가 가능한 수준입니다. 토론 활동을 추가해도 좋을 것 같아요.",
        "memo_date": "2025-04-03",
        "attendance": [
            ("2025-04-03", "중등 독서 A반", "출석"),
            ("2025-03-27", "중등 독서 A반", "출석"),
            ("2025-03-20", "중등 독서 A반", "출석"),
            ("2025-03-13", "중등 독서 A반", "지각"),
        ],
        "absent_reason": {},
        "payments": [
            {"월": "2025-04", "금액": 180000, "상태": "미납",    "납부일": "-"},
            {"월": "2025-03", "금액": 180000, "상태": "납부완료","납부일": "2025-03-05"},
        ],
    },
}

# 공지 날짜를 오늘 기준으로 동적 생성 (데모용)
NOTICES = [
    {"제목": "5월 수업 일정 안내",
     "날짜": (today - timedelta(days=2)).isoformat(),
     "내용": "5월은 1일(어린이날 연휴)로 인해 2일부터 수업 시작됩니다. 일정 참고 부탁드립니다."},
    {"제목": "4월 독서 과제 안내",
     "날짜": (today - timedelta(days=5)).isoformat(),
     "내용": "이번 달 독서 과제는 현재 읽고 있는 책의 인상 깊은 장면을 한 단락으로 써오는 것입니다."},
    {"제목": "봄 독서 발표회 안내",
     "날짜": (today - timedelta(days=6)).isoformat(),
     "내용": "4월 마지막 주 토요일에 봄 독서 발표회가 진행될 예정입니다. 참가를 원하시는 분은 미리 알려주세요."},
    {"제목": "3월 수업료 납부 안내",
     "날짜": (today - timedelta(days=35)).isoformat(),
     "내용": "3월 수업료 납부 기한은 3월 5일까지입니다."},
    {"제목": "2월 수업 일정 변경",
     "날짜": (today - timedelta(days=60)).isoformat(),
     "내용": "2월 설 연휴로 인해 수업 일정이 변경됩니다."},
]

# ── 헬퍼: 1주일 내 공지 필터 ─────────────────────────────────
def get_recent_notices(notices, days=7, max_count=4):
    cutoff = today - timedelta(days=days)
    recent = [n for n in notices if date.fromisoformat(n["날짜"]) >= cutoff]
    recent.sort(key=lambda x: x["날짜"], reverse=True)
    return recent[:max_count]

# ── 세션 초기화 ──────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student_name = ""
if "student_photos" not in st.session_state:
    st.session_state.student_photos = {}

# ══════════════════════════════════════════════════════════════
# 로그인 화면
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px">
        <div style="font-size:44px">📚</div>
        <div style="font-size:22px;font-weight:800;color:#111827;margin-top:8px">독서 교습소</div>
        <div style="font-size:13px;color:#6B7280;margin-top:4px">학부모 · 학생 포털</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 로그인")
    sel_name = st.selectbox("학생 이름", options=["선택하세요"] + list(STUDENTS.keys()))
    code = st.text_input("인증 코드", type="password", placeholder="교습소에서 받은 코드")

    if st.button("로그인", use_container_width=True, type="primary"):
        if sel_name == "선택하세요":
            st.warning("학생 이름을 선택해 주세요.")
        elif code != "1234":
            st.error("인증 코드가 올바르지 않습니다. (샘플 코드: 1234)")
        else:
            st.session_state.logged_in = True
            st.session_state.student_name = sel_name
            st.rerun()
    st.caption("샘플 인증 코드: **1234**")
    st.stop()

# ══════════════════════════════════════════════════════════════
# 로그인 후 공통 데이터
# ══════════════════════════════════════════════════════════════
name        = st.session_state.student_name
info        = STUDENTS[name]
photo_bytes = st.session_state.student_photos.get(name)

# ── 상단: 인사말 + 작은 원형 사진 + 로그아웃 ────────────────
col_g, col_ph, col_lo = st.columns([4, 1, 1])

with col_g:
    st.markdown(f"""
    <div class="greeting">안녕하세요, {name[0]}부모님 👋</div>
    <div class="greeting-sub">{today.strftime('%Y년 %m월 %d일')} · {info['반']}</div>
    """, unsafe_allow_html=True)

with col_ph:
    if photo_bytes:
        b64 = base64.b64encode(photo_bytes).decode()
        st.markdown(f"""
        <div class="photo-sm">
            <img src="data:image/jpeg;base64,{b64}" />
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="initial-sm">{name[0]}</div>', unsafe_allow_html=True)

with col_lo:
    st.markdown("<div style='margin-top:10px'>", unsafe_allow_html=True)
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["🏠 홈", "📖 독서 진도", "✅ 출결", "💳 수납", "📣 공지 전체", "⚙️ 내 정보"]
)

# ══════════════════════════════════════════════════════════════
# 탭 1 — 홈
# ══════════════════════════════════════════════════════════════
with tab1:
    att          = info["attendance"]
    att_count    = sum(1 for _, _, s in att if s == "출석")
    absent_count = sum(1 for _, _, s in att if s == "결석")
    current_book = next((b for b in info["books"] if not b["완독"]), info["books"][0])
    pct          = int(current_book["현재"] / current_book["총"] * 100)

    # 내 아이 요약 카드
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">내 아이 요약</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="m-label">이번달 출석</div>
            <div class="m-val" style="color:#185FA5">{att_count}</div>
            <div class="m-sub">결석 {absent_count}회</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="m-label">독서 진도</div>
            <div class="m-val" style="color:#3B6D11">{pct}%</div>
            <div class="m-sub">{current_book['제목']}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 수납 현황 미리보기
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">수납 현황</div>', unsafe_allow_html=True)
    for p in info["payments"][:2]:
        color = "badge-green" if p["상태"] == "납부완료" else "badge-red"
        st.markdown(f"""
        <div class="row-item">
            <span class="row-label">{p['월']} 교습비</span>
            <div style="display:flex;align-items:center;gap:10px">
                <span class="row-val">{p['금액']:,}원</span>
                <span class="badge {color}">{p['상태']}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── 최근 공지 (1주일 이내 자동 표시) ──
    recent = get_recent_notices(NOTICES)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if recent:
        # 제목 + 🆕 건수 배지
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
            <span class="card-title" style="margin-bottom:0">최근 공지</span>
            <span class="badge-new">🆕 {len(recent)}건</span>
        </div>""", unsafe_allow_html=True)

        for n in recent:
            notice_date = date.fromisoformat(n["날짜"])
            days_ago    = (today - notice_date).days
            days_label  = "오늘" if days_ago == 0 else ("어제" if days_ago == 1 else f"{days_ago}일 전")
            with st.expander(f"📢  {n['제목']}  ·  {days_label}"):
                st.write(n["내용"])
                st.caption(f"원장 · {n['날짜']}")
    else:
        st.markdown('<div class="card-title">최근 공지</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:13px;color:#6B7280;padding:4px 0">'
            '최근 1주일 내 공지사항이 없습니다.</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 2 — 독서 진도
# ══════════════════════════════════════════════════════════════
with tab2:
    total_books    = len(info["books"])
    finished_books = sum(1 for b in info["books"] if b["완독"])

    c1, c2 = st.columns(2)
    c1.metric("전체 책", f"{total_books}권")
    c2.metric("완독",   f"{finished_books}권")
    st.markdown("---")

    for book in info["books"]:
        pct       = int(book["현재"] / book["총"] * 100)
        bar_color = "#639922" if book["완독"] else "#378ADD"
        s_badge   = ('<span class="badge badge-green">완독</span>' if book["완독"]
                     else f'<span class="badge badge-blue">{pct}%</span>')
        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <div style="font-size:14px;font-weight:700;color:#111827">{book['제목']}</div>
                {s_badge}
            </div>
            <div style="font-size:12px;color:#6B7280;margin-bottom:6px">시작일: {book['시작']}</div>
            <div class="progress-bg">
                <div class="progress-fill" style="width:{pct}%;background:{bar_color}"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#6B7280;margin-top:2px">
                <span>{book['현재']} / {book['총']} 페이지</span><span>{pct}%</span>
            </div>
        </div>""", unsafe_allow_html=True)
        with st.expander(f"📋 {book['제목']} 진도 히스토리"):
            for d, p in book["히스토리"]:
                st.markdown(f"- `{d}` — +{p} 페이지")

    st.markdown("**선생님 메모**")
    st.markdown(f"""
    <div class="memo-box">
        "{info['memo']}"
        <div style="font-size:11px;color:#6B7280;margin-top:8px">원장 · {info['memo_date']}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 3 — 출결
# ══════════════════════════════════════════════════════════════
with tab3:
    att     = info["attendance"]
    s_count = {"출석": 0, "결석": 0, "지각": 0}
    for _, _, s in att:
        if s in s_count:
            s_count[s] += 1
    total_a = sum(s_count.values())
    rate    = int(s_count["출석"] / total_a * 100) if total_a > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("출석",   f"{s_count['출석']}회")
    c2.metric("결석",   f"{s_count['결석']}회")
    c3.metric("지각",   f"{s_count['지각']}회")
    c4.metric("출석률", f"{rate}%")
    st.markdown("---")
    st.markdown("**날짜별 출결 내역**")

    color_map = {"출석": "badge-green", "결석": "badge-red",
                 "지각": "badge-amber",  "미처리": "badge-blue"}
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for d, cls, s in att:
        badge      = color_map.get(s, "badge-blue")
        reason     = info["absent_reason"].get(d, "")
        reason_html = (f'<div style="font-size:11px;color:#6B7280;margin-top:3px">{reason}</div>'
                       if reason else "")
        st.markdown(f"""
        <div class="row-item" style="flex-direction:column;align-items:flex-start">
            <div style="display:flex;justify-content:space-between;width:100%">
                <span class="row-label">{d} · {cls}</span>
                <span class="badge {badge}">{s}</span>
            </div>
            {reason_html}
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 4 — 수납
# ══════════════════════════════════════════════════════════════
with tab4:
    payments   = info["payments"]
    total_amt  = sum(p["금액"] for p in payments)
    paid_amt   = sum(p["금액"] for p in payments if p["상태"] == "납부완료")
    unpaid_amt = sum(p["금액"] for p in payments if p["상태"] == "미납")

    c1, c2, c3 = st.columns(3)
    c1.metric("전체 청구", f"{total_amt:,}원")
    c2.metric("납부 완료", f"{paid_amt:,}원")
    c3.metric("미납", f"{unpaid_amt:,}원",
              delta=f"-{unpaid_amt:,}" if unpaid_amt else None,
              delta_color="inverse")
    st.markdown("---")

    if any(p["상태"] == "미납" for p in payments):
        st.warning("⚠️ 미납 교습비가 있습니다. 교습소로 문의해 주세요.")

    st.markdown("**납부 내역**")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for p in payments:
        badge = "badge-green" if p["상태"] == "납부완료" else "badge-red"
        st.markdown(f"""
        <div class="row-item">
            <div>
                <div class="row-val">{p['월']} 교습비</div>
                <div style="font-size:11px;color:#6B7280">납부일: {p['납부일']}</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
                <span class="row-val">{p['금액']:,}원</span>
                <span class="badge {badge}">{p['상태']}</span>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 5 — 공지 전체
# ══════════════════════════════════════════════════════════════
with tab5:
    cutoff = today - timedelta(days=7)
    st.markdown(f"**공지사항 전체** · 총 {len(NOTICES)}건")
    st.markdown("")
    for n in NOTICES:
        is_new    = date.fromisoformat(n["날짜"]) >= cutoff
        new_label = "  🆕" if is_new else ""
        with st.expander(f"📢  {n['제목']}{new_label}  |  {n['날짜']}"):
            st.write(n["내용"])
            st.caption(f"원장 · {n['날짜']}")

# ══════════════════════════════════════════════════════════════
# 탭 6 — 내 정보 (사진 업로드 포함)
# ══════════════════════════════════════════════════════════════
with tab6:
    st.markdown("**내 정보**")

    # 사진(큰) + 기본 정보
    pc, ic = st.columns([1, 2])
    with pc:
        if photo_bytes:
            b64 = base64.b64encode(photo_bytes).decode()
            st.markdown(f"""
            <div style="width:100px;height:100px;border-radius:50%;overflow:hidden;
                        border:2px solid #E5E7EB;margin:0 auto">
                <img src="data:image/jpeg;base64,{b64}"
                     style="width:100%;height:100%;object-fit:cover"/>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="width:100px;height:100px;border-radius:50%;background:#B5D4F4;
                        color:#0C447C;display:flex;align-items:center;justify-content:center;
                        font-size:36px;font-weight:700;margin:0 auto">
                {name[0]}
            </div>""", unsafe_allow_html=True)

    with ic:
        st.markdown(f"""
        <div class="card" style="margin-bottom:0">
            <div class="row-item"><span class="row-label">이름</span>
                <span class="row-val">{name}</span></div>
            <div class="row-item"><span class="row-label">학년</span>
                <span class="row-val">{info['학년']}</span></div>
            <div class="row-item"><span class="row-label">수강반</span>
                <span class="row-val">{info['반']}</span></div>
            <div class="row-item"><span class="row-label">담당</span>
                <span class="row-val">{info['담당']}</span></div>
            <div class="row-item"><span class="row-label">등록일</span>
                <span class="row-val">{info['등록일']}</span></div>
            <div class="row-item"><span class="row-label">연락처</span>
                <span class="row-val">{info['연락처']}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 사진 업로드 / 삭제
    st.markdown("**📷 프로필 사진 관리**")
    uploaded = st.file_uploader(
        "사진을 선택하세요 (JPG, PNG)",
        type=["jpg", "jpeg", "png"],
        key=f"profile_upload_{name}",
    )
    if uploaded:
        st.session_state.student_photos[name] = uploaded.read()
        st.success("✅ 사진이 저장되었습니다!")
        st.rerun()

    if photo_bytes:
        st.caption("현재 프로필 사진이 등록되어 있습니다.")
        if st.button("🗑 사진 삭제", key="delete_photo"):
            del st.session_state.student_photos[name]
            st.info("사진이 삭제되었습니다.")
            st.rerun()
    else:
        st.caption("등록된 사진이 없습니다. 위에서 업로드해 주세요.")
