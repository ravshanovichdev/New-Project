<<<<<<< HEAD

# from aiogram import Bot, Dispatcher, executor, types
# from scripts.youtube import download as ytDownload
# import os
# import shutil
# import uuid
# from dotenv import load_dotenv
# load_dotenv()

# API_TOKEN = os.getenv("API_TOKEN")

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot)


# @dp.message_handler(commands=['start','help'])
# async def startHandler(msg: types.Message):
#     await msg.reply("👋 Привет! Пришли ссылку с YouTube или Instagram, и я скачаю тебе Видео и Аудио.")


# @dp.message_handler()
# async def linkHandler(msg: types.Message):
#     url = msg.text.strip()
#     session_id = str(uuid.uuid4())

# # YouTube
#     if (
#         url.startswith("https://youtu.be/")
#         or url.startswith("https://www.youtube.com/")
#         or url.startswith("https://youtube.com/")):
#         await msg.reply("📸 Обработка YouTube видео, подожди...")

#         try:
#             audio_path, video_path, output_path = ytDownload(url, session_id)

#             with open(output_path, "rb") as videoFile:
#                 await bot.send_video(
#                 msg.chat.id,
#                 video=videoFile,
#                 caption="✅ Видео с YouTube загружено с @some_think_bot"
#             )

#             with open(audio_path, "rb") as audioFile:
#                 await bot.send_audio(
#                 msg.chat.id,
#                 audio=audioFile,
#                 caption="🎵 Аудио YouTube скачано с @some_think_bot"
#             )

#         except Exception as e:
#             await msg.reply(f"❌ Ошибка при скачивании: {e}")
#         finally:
#             shutil.rmtree(f"./media_temp/{session_id}", ignore_errors=True)

    

#     else:
#         await msg.reply("⚠️ Я принимаю только ссылки с YouTube и Instagram.")


# async def on_startup(dp):
#     print("Bot is started !")


# if __name__ == '__main__':
#     executor.start_polling(dp, on_startup=on_startup)




from aiogram import Bot, Dispatcher, executor, types
from scripts.youtube import download as ytDownload
from scripts.instagram import instagram_video as instaDownload
from scripts.instagram import instagram_audio as insta_Audio
=======
from aiogram import Bot, Dispatcher, executor, types
from scripts.youtube import download as ytDownload
from scripts.facebook import download as fbDownload  
>>>>>>> 9935ea603501cb32c8456a9a830b9489b79f38ab
import os
import shutil
import uuid
import asyncio
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


<<<<<<< HEAD
@dp.message_handler(commands=['start'])
=======
@dp.message_handler(commands=['start', 'help'])
>>>>>>> 9935ea603501cb32c8456a9a830b9489b79f38ab
async def startHandler(msg: types.Message):
    await msg.reply(
        "👋 Привет! Пришли ссылку с YouTube или Facebook, и я скачаю тебе Видео и Аудио."
    )


@dp.message_handler()
async def handle_links(msg: types.Message):
    url = msg.text.strip()
    session_id = str(uuid.uuid4())
    temp_dir = f"./media_temp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)

    # YouTube
    if (
        url.startswith("https://youtu.be/")
        or url.startswith("https://www.youtube.com/")
        or url.startswith("https://youtube.com/")
    ):
        await msg.reply("📸 Обработка YouTube видео, подожди...")

        try:
            audio_path, video_path, output_path = ytDownload(url, session_id)

            with open(output_path, "rb") as videoFile:
                await bot.send_video(
<<<<<<< HEAD
                msg.chat.id,
                video=videoFile,
                caption="✅ YouTube video downloaded from @some_think_bot"
            )

            with open(audio_path, "rb") as audioFile:
                await bot.send_audio(
                msg.chat.id,
                audio=audioFile,
                caption="🎵 YouTube audio downloaded from @some_think_bot"
            )
=======
                    msg.chat.id,
                    video=videoFile,
                    caption="✅ Видео с YouTube загружено с @some_think_bot",
                )

            with open(audio_path, "rb") as audioFile:
                await bot.send_audio(
                    msg.chat.id,
                    audio=audioFile,
                    caption="🎵 Аудио YouTube скачано с @some_think_bot",
                )
>>>>>>> 9935ea603501cb32c8456a9a830b9489b79f38ab

        except Exception as e:
            await msg.reply(f"❌ Ошибка при скачивании: {e}")

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    # Facebook
    elif url.startswith("https://www.facebook.com/") or url.startswith("https://fb.watch/"):
        await msg.reply("📸 Обработка Facebook видео, подожди...")

        try:
            audio_path, video_path, output_path = fbDownload(url, session_id)

            if not os.path.exists(output_path):
                await msg.reply("❌ Видео файл не найден.")
                return
            if not os.path.exists(audio_path):
                await msg.reply("❌ Аудио файл не найден.")
                return

            with open(output_path, "rb") as video_file:
                await bot.send_video(
                    msg.chat.id,
                    video=video_file,
                    caption="✅ Видео с Facebook загружено с @some_think_bot",
                )

            with open(audio_path, "rb") as audio_file:
                await bot.send_audio(
                    msg.chat.id,
                    audio=audio_file,
                    caption="🎵 Аудио Facebook скачано с @some_think_bot",
                )

        except Exception as e:
            await msg.reply(f"❌ Ошибка при скачивании: {e}")

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

#Instagram

    elif "instagram.com/p/" in url or "instagram.com/reel/" in url:
        await msg.reply("📸 Обработка Instagram видео, подожди...")

        try:
            video_path = instaDownload(url, session_id)
            audio_path = insta_Audio(video_path)

            async with bot.session:
                with open(video_path, 'rb') as videoFile:
                    await bot.send_video(msg.chat.id, video=videoFile, caption='✅ Instagram video downloaded from @some_think_bot')
                with open(audio_path, 'rb') as audioFile:
                    await bot.send_audio(msg.chat.id, audio=audioFile, caption='🎵 Instagram audio downloaded from @some_think_bot')

        except Exception as e:
            await msg.reply(f"❌ Ошибка при скачивании: {e}")
        finally:
            shutil.rmtree(f"./media_temp/{session_id}", ignore_errors=True)

    else:
        await msg.reply("⚠️ Я принимаю только ссылки с YouTube и Facebook.")


async def on_startup(dp):
<<<<<<< HEAD
    print("Bot is starting...")
=======
    print("Bot is started!")
>>>>>>> 9935ea603501cb32c8456a9a830b9489b79f38ab


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
