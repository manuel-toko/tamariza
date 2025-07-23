import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from datetime import datetime

# CSVファイルのパス
CSV_PATH = "events.csv"

st.title("📅 Event Calendar")

# --- 1. CSVからイベント読み込み（キャッシュしない） ---
def load_events():
    try:
        df = pd.read_csv(CSV_PATH)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["title", "start", "end"])

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("hhttps://hasetai.com/wp_hasetaisite01/wp-content/uploads/2024/03/kyushu-university-ito-campus-multipurpose-ground01.jpg");
        background-attachment: fixed;
        background-size: contain;
        background-repeat: no-repeat;: rgba(0,0,0,0.9);  
    }
        background-position: center top;
        background-color
    </style>
    """,
    unsafe_allow_html=True
)

# 最初に読み込み
df = load_events()

# --- 2. カレンダーオプション設定 ---
options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    },
    "editable": True,    # ← 編集を有効化！
    "selectable": True
}

# --- 3. カレンダー表示＆編集取得 ---
events = df.to_dict(orient="records")
returned_event = calendar(events=events, options=options)

# --- 4. 編集されたイベントがあればCSVに保存 ---
if returned_event and "event" in returned_event:
    st.success("📥 イベントが編集されました！CSVに保存中...")

    updated_event = returned_event["event"]

    df_index = df[
        (df["title"] == updated_event["title"]) &
        (df["start"] != updated_event["start"])
    ].index

    if len(df_index) > 0:
        df.loc[df_index[0], "start"] = updated_event["start"]
        df.loc[df_index[0], "end"] = updated_event["end"]
        df.to_csv(CSV_PATH, index=False)
        st.info("✅ 保存完了！")
    else:
        st.warning("😅 対応するイベントがCSVに見つかりませんでした。")



# --- 5. 新しいイベント追加フォーム ---
st.markdown("---")
st.subheader("🆕 新しいイベントを追加")

with st.form("event_form"):
    title = st.text_input("イベント名")
    date = st.date_input("日付")
    start_time = st.time_input("開始時間", value=datetime.now().time())
    end_time = st.time_input("終了時間", value=start_time)
    submitted = st.form_submit_button("追加")

    if submitted:
        # フォーマット：YYYY-MM-DDTHH:MM:SS
        start = datetime.combine(date, start_time).strftime("%Y-%m-%dT%H:%M:%S")
        end = datetime.combine(date, end_time).strftime("%Y-%m-%dT%H:%M:%S")
        new_event = {"title": title, "start": start, "end": end}
        df = pd.concat([df, pd.DataFrame([new_event])], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        st.success("✅ 新しいイベントを追加しました！")
        st.experimental_rerun()  # 追加後にページを再読み込みして即反映

# --- 6. イベント削除UI ---
st.markdown("---")
st.subheader("🗑️ イベント削除")

if len(df) == 0:
    st.info("イベントはまだありません。")
else:
    for i, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([4, 3, 3, 1])
        with col1:
            st.write(f"**{row['title']}**")
        with col2:
            st.write(f"{row['start']}")
        with col3:
            st.write(f"{row['end']}")
        with col4:
            if st.button("削除", key=f"delete_{i}"):
                df = df.drop(i)
                df.to_csv(CSV_PATH, index=False)
                st.success("🗑️ 削除しました！")
                st.experimental_rerun()
