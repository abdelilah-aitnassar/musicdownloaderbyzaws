while True:
    try:
        from telethon import TelegramClient, events
        import asyncio
        from pytube import YouTube
        import os

        current_directory = os.path.dirname(os.path.realpath(__file__))
        session_name = 'send_name'
        audio_extensions = ('.mp3', '.ogg', '.m4a', '.webm')  # Add other audio extensions as needed

        # Explicitly specify a session file path
        session_file_path = os.path.join(current_directory, f'{session_name}.session')

        # Remove existing audio files at script startup
        for filename in os.listdir(current_directory):
            if filename.lower().endswith(audio_extensions):
                file_path = os.path.join(current_directory, filename)
                os.remove(file_path)

        # Function to download audio
        def download_audio(link):
            # Remove existing audio files before downloading
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

            except Exception as e:
                print(f"An error has occurred: {str(e)}")

            print("Download is completed successfully")


        # Telegram client initialization
        api_id = 27185648
        api_hash = '33d43db8c209893c4ff7cbf2ecccb8b4'
        bot_token = '6814352675:AAHqMqfgrSuUEJh-2SdkPhJr1EZMci4-YHE'
        app = TelegramClient(session_file_path, api_id, api_hash).start(bot_token=bot_token)


        async def main(event, current_directory):
            print('Main function called.')
            print(f'Event: {event}')

            sender_user_id = getattr(event.message.peer_id, 'user_id', None)
            print(f'Sender User ID: {sender_user_id}')

            if sender_user_id:
                await app.send_message(sender_user_id, 'Audio downloader!')

                # Set the audio_path dynamically based on the downloaded file
                audio_file = next((f for f in os.listdir(current_directory) if f.lower().endswith(audio_extensions)), None)
                if audio_file:
                    audio_path = os.path.join(current_directory, audio_file)

                    try:
                        await app.send_file(sender_user_id, audio_path)
                        print('File sent successfully.')
                    except Exception as e:
                        print(f"Error sending file: {str(e)}")


        async def on_message_handler(event, current_directory):
            print('Message handler called.')
            if 'yout' in event.message.text.lower():
                print('Sending an audio...')
                download_audio(event.message.text)
                try:
                    await main(event, current_directory)
                except Exception as e:
                    print(f"Error in main function: {str(e)}")
                print('Sent.')

                # Remove temporary downloaded audio files
                for filename in os.listdir(current_directory):
                    if filename.lower().endswith(audio_extensions):
                        file_path = os.path.join(current_directory, filename)
                        os.remove(file_path)

        with app:
            app.add_event_handler(lambda event, cd=current_directory: on_message_handler(event, cd), events.NewMessage())
            app.run_until_disconnected()
    except:
        continue
