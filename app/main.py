import discord
import dotenv
from server import server_thread
from deepl import Translator
from langdetect import detect
from flask import Flask
import os
import threading

# Flaskの設定
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running!'

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 特権的なインテントの設定
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
TOKEN = os.environ.get("TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
if not DEEPL_API_KEY:
    raise ValueError("DeepL API key is not set. Please set the API key in Replit Secrets.")
translator = Translator(DEEPL_API_KEY)

# ロールの名前を定義
JP_SPEAKER_ROLE = "JP Child of Light"
ABROAD_SPEAKER_ROLE = "Child of Light"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    member_roles = [role.name for role in message.author.roles]

    try:
        # 言語を検出
        detected_lang = detect(message.content)

        if JP_SPEAKER_ROLE in member_roles:
            if detected_lang == 'ja':
                # 日本語からインドネシア語に翻訳
                translated = translator.translate_text(message.content, target_lang='ID')
                await message.channel.send(f'Indonesian Translation: {translated.text}')
            else:
                # その他の言語から日本語に翻訳
                translated = translator.translate_text(message.content, target_lang='JA')
                await message.channel.send(f'Indonesian Translation: {translated.text}')

        elif ABROAD_SPEAKER_ROLE in member_roles:
            if detected_lang == 'id':
                # インドネシア語から日本語に翻訳
                translated = translator.translate_text(message.content, target_lang='JA')
                await message.channel.send(f'日本語訳: {translated.text}')
            else:
                # その他の言語から日本語に翻訳
                translated = translator.translate_text(message.content, target_lang='JA')
                await message.channel.send(f'日本語訳: {translated.text}')
        else:
            await message.channel.send('この機能を利用するためのロールがありません。')
    except Exception as e:
        await message.channel.send(f"Error: {str(e)}")

# Replitの環境変数に設定したボットのトークンを取得
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Bot token is not set. Please set the token in Replit Secrets.")

# Flaskアプリを別スレッドで実行
threading.Thread(target=run_flask).start()

# Discordボットを実行
client.run(TOKEN)
