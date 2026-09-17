import streamlit as st

# ページの基本設定（スマホでも見やすいように）
st.set_page_config(page_title="Koso-Cia - シアター", page_icon="🚀", layout="centered")

# --- タイトルと秘密基地風デザインの雰囲気 ---
st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🎬 秘密基地シアター「コソシア」</h2>", unsafe_allow_html=True)
st.write("---")

# --- 1. 動画プレイヤー部分（上部） ---
st.subheader("📺 現在の上映中ムービー")
video_url = st.text_input("YouTubeなどの動画リンクを入力", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if video_url:
    try:
        st.video(video_url)
    except Exception:
        st.error("正しい動画リンクを入力してください。")

st.write("---")

# --- 2. 下部チャット＆スタンプ部分 ---
st.subheader("💬 リアルタイムチャット")

# チャットの履歴を保存する箱（メモリ上）
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャットの過去ログを表示
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        st.markdown(f"**{msg['name']}**: {msg['text']}")

# 入力フォーム（一番下に配置される形）
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        user_name = st.text_input("名前", value="ゲスト")
    with col2:
        user_msg = st.text_input("メッセージ")
    
    # リクエストされたスタンプボタン
    st.write("✨ スタンプ：")
    c1, c2, c3 = st.columns(3)
    stamp_clicked = None
    if c1.form_submit_button("👍 いいね！"): stamp_clicked = "👍 いいね！"
    if c2.form_submit_button("🌱 草"): stamp_clicked = "🌱 草"
    if c3.form_submit_button("💕 可愛い"): stamp_clicked = "💕 可愛い"

    submit_button = st.form_submit_button(label="送信")

    if submit_button and user_msg:
        st.session_state.messages.append({"name": user_name, "text": user_msg})
        st.rerun()
    elif stamp_clicked:
        st.session_state.messages.append({"name": user_name, "text": f"[{stamp_clicked}]"})
        st.rerun()

