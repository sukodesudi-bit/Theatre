import json
import os
import streamlit as st

# ページの設定
st.set_page_config(
    page_title="シアター",
    page_icon="🎬",
    layout="centered",
)

# データを保存するファイル名
DATA_FILE = "data.json"


# データの読み込み関数
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # 初期データ
    return {
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "messages": [
            {"name": "🚀 司令官", "text": "わーい！始まるよ！"},
            {"name": "🐱 ネコ", "text": "楽しみ！"},
            {"name": "👤 ゲスト", "text": "マインクラフトだー！"},
        ],
    }


# データの保存関数
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# データをセッションまたはファイルから読み込み
if "app_data" not in st.session_state:
    st.session_state.app_data = load_data()

data = st.session_state.app_data

# かわいいデザインを適用するCSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #333333;
    }
    .header-container {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
        color: #1e293b;
    }
    .chat-bubble {
        background-color: #ffffff;
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        font-size: 14px;
    }
    .chat-name {
        font-size: 11px;
        color: #94a3b8;
        margin-bottom: 2px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- ヘッダー ---
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">🎬 シアター</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 映画館（シアター）セクション ---
st.markdown("### 📺 上映中ムービー")

# 動画URLの入力
new_url = st.text_input(
    "YouTubeなどの動画リンクを入力", value=data["video_url"]
)
if new_url != data["video_url"]:
    data["video_url"] = new_url
    save_data(data)
    st.rerun()

# 動画プレイヤーの表示
try:
    st.video(data["video_url"])
except Exception:
    st.warning("正しいYouTubeのリンクを入力してね！")

st.markdown("---")

# --- チャットセクション ---
st.markdown("### 💬 リアルタイムチャット")

# コメントを吹き出し風に表示
for msg in data["messages"]:
    st.markdown(
        f"""
        <div class="chat-bubble">
            <div class="chat-name">{msg['name']}</div>
            <div>{msg['text']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# コメント入力フォーム
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        user_name = st.text_input("名前", value="ゲスト")
    with col2:
        user_msg = st.text_input("メッセージ")

    st.markdown("✨ スタンプ:")
    col_s1, col_s2, col_s3 = st.columns(3)
    stamp_chosen = None
    if col_s1.form_submit_button("👍 いいね！"):
        stamp_chosen = "👍 いいね！"
    if col_s2.form_submit_button("🌱 草"):
        stamp_chosen = "🌱 草"
    if col_s3.form_submit_button("💕 可愛い"):
        stamp_chosen = "💕 可愛い"

    submit_chat = st.form_submit_button("送信")

    if submit_chat and user_msg:
        data["messages"].append({"name": user_name, "text": user_msg})
        save_data(data)
        st.rerun()
    elif stamp_chosen:
        data["messages"].append(
            {"name": user_name, "text": f"[{stamp_chosen}]"}
        )
        save_data(data)
        st.rerun()

# 更新ボタン
if st.button("🔄 最新のチャットを読み込む"):
    st.rerun()
