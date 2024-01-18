from telethon import TelegramClient, events
import asyncio
from pytube import YouTube
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

audio_extensions = ('.mp3', '.ogg', '.m4a', '.webm')  # Add other audio extensions as needed

for filename in os.listdir(current_directory):
    if filename.lower().endswith(audio_extensions):
        file_path = os.path.join(current_directory, filename)
        os.remove(file_path)


def DownloadAudio(link):
    import os

    current_directory = os.path.dirname(os.path.realpath(__file__))

    audio_extensions = ('.mp3', '.ogg', '.m4a', '.webm')  # Add other audio extensions as needed

    for filename in os.listdir(current_directory):
        if filename.lower().endswith(audio_extensions):
            file_path = os.path.join(current_directory, filename)
            os.remove(file_path)

    youtube_object = YouTube(link)
    try:
        audio_stream = youtube_object.streams.filter(only_audio=True).first()
    except:
        audio_stream = youtube_object.streams.get_audio_only()

    try:
        audio_stream.download()
        
        # Change the file extension to .mp3
        original_file = os.path.join(current_directory, audio_stream.default_filename)
        new_file = os.path.splitext(original_file)[0] + '.mp3'
        os.rename(original_file, new_file)
        
    except:
        print("An error has occurred")

    print("Download is completed successfully")


api_id = 27185648
msg = 'audio downloader!'
api_hash = '33d43db8c209893c4ff7cbf2ecccb8b4'
bot_token = '6814352675:AAHqMqfgrSuUEJh-2SdkPhJr1EZMci4-YHE'
session_name = 'send_name'
audio_path = ''  # The audio file path will be set dynamically based on the downloaded file

app = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)


async def main(event):
    print('Main function called.')
    print(f'Event: {event}')

    sender_user_id = getattr(event.message.peer_id, 'user_id', None)
    print(f'Sender User ID: {sender_user_id}')

    if sender_user_id:
        await app.send_message(sender_user_id, msg)
        await asyncio.sleep(1)  # Reduce sleep duration to 1 second

        # Set the audio_path dynamically based on the downloaded file
        audio_file = next((f for f in os.listdir(current_directory) if f.lower().endswith(audio_extensions)), None)
        if audio_file:
            audio_path = os.path.join(current_directory, audio_file)

            try:
                await app.send_file(sender_user_id, audio_path)
                print('File sent successfully.')
            except Exception as e:
                print(f"Error sending file: {str(e)}")


async def on_message_handler(event):
    print('Message handler called.')
    if 'yout' in event.message.text.lower():
        print('Sending an audio...')
        DownloadAudio(event.message.text)
        try:
            await main(event)
        except Exception as e:
            print(f"Error in main function: {str(e)}")
        print('Sent.')
        import os

        current_directory = os.path.dirname(os.path.realpath(__file__))

        audio_extensions = ('.mp3', '.ogg', '.m4a', '.webm')  # Add other audio extensions as needed

        for filename in os.listdir(current_directory):
            if filename.lower().endswith(audio_extensions):
                file_path = os.path.join(current_directory, filename)
                os.remove(file_path)

with app:
    app.add_event_handler(on_message_handler, events.NewMessage())
    app.run_until_disconnected()
