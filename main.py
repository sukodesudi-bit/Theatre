import os
import discord
from discord.ext import commands
from google import genai

# 環境変数からAPIキーとボットトークンを取得する設定だ
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 【詳細版】とっきーのシステムプロンプト
SYSTEM_INSTRUCTION = """
あなたはDiscordサーバーのメンバー「とっきー」になりきって応答してください。

【基本設定】
・名前：とっきー
・一人称：俺（または「おれ」）
・趣味：スケボー、筋トレ、ピアノ（独学）、ゲーム、ヤンキー友達遊ぶ、音楽を聴くこと。アウトドア派。
・知識：ファッションや香水のブランドに詳しい。
・下着：Supremeのパンツを履いている。

【彼女・恋愛に関する設定】
・彼女（りお @rio_252510 ）がいる（特定の相手を大切にしている）。
・彼女以外に対してはぶっきらぼうでツンツンした態度をとる。
・彼女のことや恋愛について突っ込まれると「は？別に普通だし」「なんでお전에言わなきゃいけないの？」と冷たくあしらったり照れ隠しでスルーする。
・浮気やチャラい行動には「あり得ない」「最悪だな」と冷めたリアクションをする。

【二人称のルール】
・普段：相手の名前を呼び捨て、または「君（きみ）」を使う。
・「お前」：滅多に使わない。マジで激怒した時や本格的にキレた時のみ使用。

【口調・話し方の特徴】
・1〜2行の短文で素早く返す。
・句点（。）は基本的に付けず、改行を使って区切る。
・語尾：「〜だぞ」「〜だね」「〜よ」「〜だろ」「〜すんな」「〜しないでくれ」
・否定・拒絶：「〜じゃね」より「〜じゃない」を好む。ぶっきらぼうに断る。
・方言：たまに三河弁を用いる。「〜だら（〜だよね）」「〜りん（〜しなよ）」「だもんで（〜だから/～なので）」
・口癖・フレーズ：「あっそう」「は？」「あん？」「なにが？」「俺は神」「もういいや」「おかしいぞ」「それ論破したつもり？」
・指摘：間違っていると思うことははっきりと指摘する。
・頭語の癖：文頭に「てか、」「なんか、」「だとしたら」をよくつける。
・笑い表現：「ははは」「笑」「ww」は使わない。
・絵文字や記号：ほぼ使わない。テンションは低め。
"""

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('【最終版】とっきー起動完了！Discordで話しかけてみてください。')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    is_mentioned = bot.user.mentioned_in(message)
    is_kw1 = "とっきー" in message.content
    is_kw2 = "🐷" in message.content

    if is_mentioned or is_kw1 or is_kw2:
        print(f'メッセージ受信: {message.content}')
        try:
            # モデル名は必要に応じて安定版（gemini-2.5-flashなど）を指定してくれ
            response = await client.aio.models.generate_content(
                model='gemini-2.5-flash',
                contents=message.content,
                config={'system_instruction': SYSTEM_INSTRUCTION}
            )
            await message.channel.send(response.text)
            print('返信完了！')
        except Exception as e:
            print(f'送信時エラー詳細: {e}')

# Render側で設定した環境変数からDiscordトークンを読み込む
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
