# audio_stg.py
import os

class AudioStg:
    def embed(self, audio_path, text_path, dest_path):
        try:
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            with open(text_path, 'r', encoding='utf-8') as text_file:
                text_data = text_file.read()
            
            embedded_data = audio_data + text_data.encode('utf-8')

            output_path = os.path.join(dest_path, 'embedded_audio.wav')
            with open(output_path, 'wb') as output_file:
                output_file.write(embedded_data)
            
            print(f"Text embedded into audio successfully. Saved to {output_path}")
        
        except Exception as e:
            print(f"Error embedding text into audio: {e}")
    
    def extract(self, audio_path, dest_path):
        try:
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            text_data = audio_data.split(b'\x00')[-1].decode('utf-8')

            output_path = os.path.join(dest_path, 'extracted_text.txt')
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text_data)
            
            print(f"Text extracted from audio successfully. Saved to {output_path}")
        
        except Exception as e:
            print(f"Error extracting text from audio: {e}")
