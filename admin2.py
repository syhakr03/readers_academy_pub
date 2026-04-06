import streamlit as st
from datetime import date, datetime
import pandas as pd

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="독서 교습소 관리자",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* 전체 배경 */
[data-testid="stAppViewContainer"] { background: #F7F8FA; }
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #E5E7EB; }

/* 사이드바 제목 */
.brand-box {
    background: linear-gradient(135deg, #2F6FED, #73A7FF);
    border-radius: 14px; padding: 14px 16px; color: #fff;
    margin-bottom: 10px;
}
.brand-box .name { font-size: 17px; font-weight: 800; }
.brand-box .sub  { font-size: 12px; opacity: .8; margin-top: 2px; }

/* 요약 카드 */
.metric-card {
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 14px; padding: 16px;
    text-align: center; margin-bottom: 4px;
    box-shadow: 0 4px 12px rgba(17,24,39,.06);
}
.metric-card .label { font-size: 12px; color: #6B7280; margin-bottom: 6px; }
.metric-card .num   { font-size: 32px; font-weight: 900; letter-spacing: -1px; }
.metric-card .sub   { font-size: 12px; color: #6B7280; margin-top: 4px; }

/* 수업 카드 */
.class-item {
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 14px; padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(17,24,39,.05);
}
.class-item .time { font-weight: 900; color: #0B3EA8; font-size: 15px; }
.class-item .cname { font-weight: 800; font-size: 15px; margin-bottom: 3px; }
.class-item .desc  { font-size: 12px; color: #6B7280; }

/* 목표 배너 */
.goal-banner {
    background: #FEF9C3; border: 1px solid #FDE68A;
    border-radius: 14px; padding: 14px 16px;
    margin-bottom: 6px;
}
.goal-banner strong { font-weight: 900; }
.goal-banner .sub   { color: #92400E; font-size: 13px; margin-top: 6px; }

/* 알림 항목 */
.alert-line {
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 12px; padding: 10px 14px;
    display: flex; justify-content: space-between;
    align-items: center; font-size: 13px;
    margin-bottom: 8px;
}
.tag-red {
    font-size: 12px; padding: 3px 9px; border-radius: 999px;
    border: 1px solid rgba(239,68,68,.3);
    background: rgba(239,68,68,.1); color: #7F1D1D;
}
</style>
""", unsafe_allow_html=True)

# ── 샘플 데이터 ──────────────────────────────────────────────
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame([
        {"이름": "김민준", "학년": "초4", "담당강사": "원장", "등록일": "2025-03-01", "상태": "수강중"},
        {"이름": "이서연", "학년": "초5", "담당강사": "원장", "등록일": "2025-02-15", "상태": "수강중"},
        {"이름": "박지호", "학년": "초6", "담당강사": "원장", "등록일": "2025-01-10", "상태": "수강중"},
        {"이름": "최수아", "학년": "중1", "담당강사": "원장", "등록일": "2025-03-10", "상태": "수강중"},
        {"이름": "정도윤", "학년": "중2", "담당강사": "원장", "등록일": "2025-02-01", "상태": "수강중"},
        {"이름": "강하은", "학년": "중1", "담당강사": "원장", "등록일": "2025-01-20", "상태": "수강중"},
    ])

if "classes" not in st.session_state:
    st.session_state.classes = pd.DataFrame([
        {"시간": "15:00", "수업명": "초등 독서 A반", "학생수": 3, "담당": "원장", "상태": "진행예정"},
        {"시간": "16:30", "수업명": "초등 독서 B반", "학생수": 2, "담당": "원장", "상태": "진행예정"},
        {"시간": "18:00", "수업명": "중등 독서 A반", "학생수": 3, "담당": "원장", "상태": "진행예정"},
        {"시간": "19:30", "수업명": "중등 독서 B반", "학생수": 2, "담당": "원장", "상태": "진행예정"},
    ])

if "attendance" not in st.session_state:
    today = date.today().isoformat()
    st.session_state.attendance = pd.DataFrame([
        {"날짜": today, "학생": "김민준", "수업": "초등 독서 A반", "상태": "출석"},
        {"날짜": today, "학생": "이서연", "수업": "초등 독서 A반", "상태": "출석"},
        {"날짜": today, "학생": "박지호", "수업": "초등 독서 B반", "상태": "결석"},
        {"날짜": today, "학생": "최수아", "수업": "중등 독서 A반", "상태": "지각"},
        {"날짜": today, "학생": "정도윤", "수업": "중등 독서 A반", "상태": "출석"},
        {"날짜": today, "학생": "강하은", "수업": "중등 독서 B반", "상태": "미처리"},
    ])

if "payments" not in st.session_state:
    st.session_state.payments = pd.DataFrame([
        {"학생": "김민준", "월": "2025-04", "금액": 150000, "상태": "납부완료"},
        {"학생": "이서연", "월": "2025-04", "금액": 150000, "상태": "납부완료"},
        {"학생": "박지호", "월": "2025-04", "금액": 150000, "상태": "미납"},
        {"학생": "박지호", "월": "2025-03", "금액": 150000, "상태": "미납"},
        {"학생": "최수아", "월": "2025-04", "금액": 180000, "상태": "미납"},
        {"학생": "정도윤", "월": "2025-04", "금액": 180000, "상태": "납부완료"},
        {"학생": "강하은", "월": "2025-04", "금액": 180000, "상태": "납부완료"},
    ])

if "progress" not in st.session_state:
    st.session_state.progress = pd.DataFrame([
        {"학생": "김민준", "책제목": "어린왕자", "총페이지": 120, "현재페이지": 80, "시작일": "2025-03-20", "메모": "독해력 향상 중"},
        {"학생": "이서연", "책제목": "마당을 나온 암탉", "총페이지": 200, "현재페이지": 150, "시작일": "2025-03-15", "메모": "어휘력 우수"},
        {"학생": "박지호", "책제목": "괴물이 나타났다", "총페이지": 180, "현재페이지": 60, "시작일": "2025-04-01", "메모": ""},
        {"학생": "최수아", "책제목": "파과", "총페이지": 300, "현재페이지": 200, "시작일": "2025-03-10", "메모": "심화독서 가능"},
        {"학생": "정도윤", "책제목": "채식주의자", "총페이지": 250, "현재페이지": 100, "시작일": "2025-04-01", "메모": ""},
        {"학생": "강하은", "책제목": "파과", "총페이지": 300, "현재페이지": 280, "시작일": "2025-03-05", "메모": "거의 완독"},
    ])

if "todo" not in st.session_state:
    st.session_state.todo = [
        {"text": "오늘 공지 작성", "done": False},
        {"text": "결석자 메시지 보내기", "done": False},
        {"text": "미납 안내 보내기", "done": False},
    ]

# ── 사이드바 ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <div class="name">📚 독서 교습소</div>
        <div class="sub">원장 관리 시스템</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "메뉴",
        ["📊 대시보드", "👨‍👩‍👧 학생 관리", "🗓 수업/시간표", "✅ 출결 관리", "💳 수납 관리", "📖 진도 관리"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption(f"오늘: {date.today().strftime('%Y년 %m월 %d일')}")

# ══════════════════════════════════════════════════════════════
# 1. 대시보드
# ══════════════════════════════════════════════════════════════
if page == "📊 대시보드":
    st.title("📊 메인 대시보드")
    st.caption(f"{date.today().strftime('%Y-%m-%d')} · 독서 교습소")

    # 목표 배너
    st.markdown("""
    <div class="goal-banner">
        <strong>🎯 오늘의 목표</strong>: 수업 진행 · 출결 체크 · 미납 안내
        <div class="sub">우선순위: 오늘 수업 → 출결 → 수납/미납 → 진도 기록</div>
    </div>
    """, unsafe_allow_html=True)

    # 요약 지표
    today_str = date.today().isoformat()
    att = st.session_state.attendance
    today_att = att[att["날짜"] == today_str]
    unpaid = st.session_state.payments[st.session_state.payments["상태"] == "미납"]
    absent_unprocessed = today_att[today_att["상태"] == "미처리"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">오늘 수업</div>
            <div class="num">{len(st.session_state.classes)}</div>
            <div class="sub">전일 대비 동일</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">미처리 출결</div>
            <div class="num" style="color:#F59E0B">{len(absent_unprocessed)}</div>
            <div class="sub">확인 필요</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">미납</div>
            <div class="num" style="color:#EF4444">{len(unpaid)}</div>
            <div class="sub">수납 처리 필요</div></div>""", unsafe_allow_html=True)
    with c4:
        total_students = len(st.session_state.students)
        st.markdown(f"""<div class="metric-card">
            <div class="label">전체 학생</div>
            <div class="num" style="color:#2F6FED">{total_students}</div>
            <div class="sub">수강 중</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.3, 0.7])

    with left:
        st.subheader("📅 오늘 수업")
        for _, row in st.session_state.classes.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="class-item">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div class="time">{row['시간']}</div>
                            <div class="cname">{row['수업명']}</div>
                            <div class="desc">{row['학생수']}명 · 담당: {row['담당']} · {row['상태']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                b1, b2, b3, _ = st.columns([1, 1, 1, 2])
                with b1:
                    if st.button("✅ 출결", key=f"att_{row['수업명']}"):
                        st.info(f"{row['수업명']} 출결 처리 → '출결 관리' 탭에서 확인하세요.")
                with b2:
                    if st.button("📝 수업노트", key=f"note_{row['수업명']}"):
                        st.info("수업 노트 기능 준비 중입니다.")
                with b3:
                    if st.button("💬 메시지", key=f"msg_{row['수업명']}"):
                        st.info("메시지 기능 준비 중입니다.")

    with right:
        st.subheader("⚡ 빠른 작업")
        for i, item in enumerate(st.session_state.todo):
            checked = st.checkbox(item["text"], value=item["done"], key=f"todo_{i}")
            st.session_state.todo[i]["done"] = checked

        st.divider()
        st.subheader("📋 출결 현황 (오늘)")
        status_counts = today_att["상태"].value_counts()
        cols = st.columns(2)
        for j, (status, color) in enumerate([("출석","#16A34A"),("결석","#EF4444"),("지각","#F59E0B"),("미처리","#6B7280")]):
            with cols[j % 2]:
                cnt = status_counts.get(status, 0)
                st.markdown(f"<b style='color:{color}'>{status}</b>: <b>{cnt}명</b>", unsafe_allow_html=True)

        st.divider()
        st.subheader("💳 수납 알림")
        for _, row in unpaid.iterrows():
            st.markdown(f"""
            <div class="alert-line">
                <span>{row['학생']} · {row['월']} · {row['금액']:,}원</span>
                <span class="tag-red">미납</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("📣 + 공지 작성", use_container_width=True, type="primary"):
            st.info("공지 작성 기능 준비 중입니다.")

# ══════════════════════════════════════════════════════════════
# 2. 학생 관리
# ══════════════════════════════════════════════════════════════
elif page == "👨‍👩‍👧 학생 관리":
    st.title("👨‍👩‍👧 학생 관리")

    with st.expander("➕ 신규 학생 등록", expanded=False):
        with st.form("new_student"):
            c1, c2, c3 = st.columns(3)
            name  = c1.text_input("이름")
            grade = c2.selectbox("학년", ["초1","초2","초3","초4","초5","초6","중1","중2","중3"])
            teach = c3.text_input("담당강사", value="원장")
            submitted = st.form_submit_button("등록")
            if submitted and name:
                new_row = {"이름": name, "학년": grade, "담당강사": teach,
                           "등록일": date.today().isoformat(), "상태": "수강중"}
                st.session_state.students = pd.concat(
                    [st.session_state.students, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ {name} 학생이 등록되었습니다.")
                st.rerun()

    st.dataframe(
        st.session_state.students,
        use_container_width=True,
        hide_index=True,
        column_config={
            "이름": st.column_config.TextColumn("이름", width=100),
            "학년": st.column_config.TextColumn("학년", width=80),
            "등록일": st.column_config.DateColumn("등록일", format="YYYY-MM-DD"),
            "상태": st.column_config.TextColumn("상태", width=90),
        }
    )

# ══════════════════════════════════════════════════════════════
# 3. 수업/시간표
# ══════════════════════════════════════════════════════════════
elif page == "🗓 수업/시간표":
    st.title("🗓 수업 / 시간표")

    with st.expander("➕ 수업 추가", expanded=False):
        with st.form("new_class"):
            c1, c2, c3, c4 = st.columns(4)
            time_  = c1.text_input("시간 (예: 17:00)")
            cname  = c2.text_input("수업명")
            cnt    = c3.number_input("학생 수", min_value=1, max_value=20, value=1)
            teacher= c4.text_input("담당", value="원장")
            if st.form_submit_button("추가"):
                if time_ and cname:
                    new_row = {"시간": time_, "수업명": cname, "학생수": int(cnt),
                               "담당": teacher, "상태": "진행예정"}
                    st.session_state.classes = pd.concat(
                        [st.session_state.classes, pd.DataFrame([new_row])], ignore_index=True)
                    st.success("✅ 수업이 추가되었습니다.")
                    st.rerun()

    st.dataframe(
        st.session_state.classes.sort_values("시간"),
        use_container_width=True, hide_index=True,
    )

# ══════════════════════════════════════════════════════════════
# 4. 출결 관리
# ══════════════════════════════════════════════════════════════
elif page == "✅ 출결 관리":
    st.title("✅ 출결 관리")

    sel_date = st.date_input("날짜 선택", value=date.today())
    sel_str  = sel_date.isoformat()

    att = st.session_state.attendance
    day_att = att[att["날짜"] == sel_str].copy()

    # 상태별 요약
    c1, c2, c3, c4 = st.columns(4)
    for col, status, color in zip([c1,c2,c3,c4],
                                   ["출석","결석","지각","미처리"],
                                   ["#16A34A","#EF4444","#F59E0B","#6B7280"]):
        cnt = len(day_att[day_att["상태"] == status])
        col.metric(status, f"{cnt}명")

    st.divider()

    if day_att.empty:
        st.info("해당 날짜의 출결 기록이 없습니다.")
    else:
        edited = st.data_editor(
            day_att[["학생","수업","상태"]].reset_index(drop=True),
            column_config={
                "상태": st.column_config.SelectboxColumn(
                    "상태", options=["출석","결석","지각","미처리"])
            },
            use_container_width=True,
            num_rows="fixed",
        )

    # 신규 출결 추가
    with st.expander("➕ 출결 기록 추가"):
        with st.form("new_att"):
            c1, c2, c3 = st.columns(3)
            student = c1.selectbox("학생", st.session_state.students["이름"].tolist())
            cls     = c2.selectbox("수업", st.session_state.classes["수업명"].tolist())
            status  = c3.selectbox("상태", ["출석","결석","지각","미처리"])
            if st.form_submit_button("저장"):
                new_row = {"날짜": sel_str, "학생": student, "수업": cls, "상태": status}
                st.session_state.attendance = pd.concat(
                    [st.session_state.attendance, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ 출결 기록이 저장되었습니다.")
                st.rerun()

# ══════════════════════════════════════════════════════════════
# 5. 수납 관리
# ══════════════════════════════════════════════════════════════
elif page == "💳 수납 관리":
    st.title("💳 수납 관리")

    pay = st.session_state.payments

    # 요약
    c1, c2, c3 = st.columns(3)
    c1.metric("전체 청구", f"{pay['금액'].sum():,}원")
    c2.metric("납부 완료", f"{pay[pay['상태']=='납부완료']['금액'].sum():,}원",
              delta=f"{len(pay[pay['상태']=='납부완료'])}건")
    c3.metric("미납", f"{pay[pay['상태']=='미납']['금액'].sum():,}원",
              delta=f"-{len(pay[pay['상태']=='미납'])}건", delta_color="inverse")

    st.divider()
    tab1, tab2 = st.tabs(["📋 전체 내역", "⚠️ 미납 목록"])

    with tab1:
        st.dataframe(pay, use_container_width=True, hide_index=True,
                     column_config={"금액": st.column_config.NumberColumn("금액", format="%d원")})

    with tab2:
        unpaid = pay[pay["상태"] == "미납"]
        if unpaid.empty:
            st.success("미납 학생이 없습니다! 🎉")
        else:
            for _, row in unpaid.iterrows():
                col1, col2, col3 = st.columns([2,1,1])
                col1.write(f"**{row['학생']}** · {row['월']}")
                col2.write(f"{row['금액']:,}원")
                if col3.button("납부 처리", key=f"pay_{row['학생']}_{row['월']}"):
                    mask = (st.session_state.payments["학생"] == row["학생"]) & \
                           (st.session_state.payments["월"] == row["월"])
                    st.session_state.payments.loc[mask, "상태"] = "납부완료"
                    st.success(f"✅ {row['학생']} {row['월']} 납부 완료 처리했습니다.")
                    st.rerun()

    with st.expander("➕ 수납 내역 추가"):
        with st.form("new_pay"):
            c1, c2, c3, c4 = st.columns(4)
            student = c1.selectbox("학생", pay["학생"].unique().tolist() +
                                   st.session_state.students["이름"].tolist())
            month   = c2.text_input("월 (예: 2025-05)")
            amount  = c3.number_input("금액", min_value=0, step=10000, value=150000)
            status  = c4.selectbox("상태", ["미납","납부완료"])
            if st.form_submit_button("추가"):
                new_row = {"학생": student, "월": month, "금액": amount, "상태": status}
                st.session_state.payments = pd.concat(
                    [st.session_state.payments, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ 수납 내역이 추가되었습니다.")
                st.rerun()

# ══════════════════════════════════════════════════════════════
# 6. 진도 관리
# ══════════════════════════════════════════════════════════════
elif page == "📖 진도 관리":
    st.title("📖 독서 진도 관리")

    prog = st.session_state.progress.copy()
    prog["진도율(%)"] = (prog["현재페이지"] / prog["총페이지"] * 100).round(1)

    # 진도 카드
    for _, row in prog.iterrows():
        pct = row["진도율(%)"]
        bar_color = "#16A34A" if pct >= 80 else "#2F6FED" if pct >= 40 else "#F59E0B"
        with st.container():
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**{row['학생']}** · {row['책제목']}")
                st.progress(int(pct) / 100, text=f"{row['현재페이지']} / {row['총페이지']} 페이지 ({pct}%)")
                if row["메모"]:
                    st.caption(f"📝 {row['메모']}")
            with c2:
                st.caption(f"시작일: {row['시작일']}")
        st.divider()

    with st.expander("➕ 진도 기록 추가 / 수정"):
        with st.form("new_prog"):
            c1, c2 = st.columns(2)
            student  = c1.selectbox("학생", st.session_state.students["이름"].tolist())
            book     = c2.text_input("책 제목")
            c3, c4, c5 = st.columns(3)
            total    = c3.number_input("총 페이지", min_value=1, value=200)
            current  = c4.number_input("현재 페이지", min_value=0, value=0)
            memo     = c5.text_input("메모")
            if st.form_submit_button("저장"):
                new_row = {"학생": student, "책제목": book, "총페이지": total,
                           "현재페이지": current, "시작일": date.today().isoformat(), "메모": memo}
                # 기존 기록이 있으면 업데이트
                mask = (st.session_state.progress["학생"] == student) & \
                       (st.session_state.progress["책제목"] == book)
                if mask.any():
                    st.session_state.progress.loc[mask, "현재페이지"] = current
                    st.session_state.progress.loc[mask, "메모"] = memo
                else:
                    st.session_state.progress = pd.concat(
                        [st.session_state.progress, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ 진도가 저장되었습니다.")
                st.rerun()