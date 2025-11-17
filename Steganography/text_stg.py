import os

class TextStg:
    def _to_zero_width(self, text):
        # Convert the text to a binary string
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        # Convert binary string to zero-width space representation
        zero_width_text = ''.join('\u200b' if bit == '0' else '\u200c' for bit in binary_text)
        return zero_width_text

    def _from_zero_width(self, zero_width_text):
        # Convert zero-width space representation back to binary string
        binary_text = ''.join('0' if char == '\u200b' else '1' for char in zero_width_text)
        # Convert binary string back to text
        text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
        return text

    def embed(self, cover_text_file, secret_text_file, output_text_file):
        """
        Embed secret text into cover text using zero-width characters.
        """
        try:
            # Ensure files exist
            if not os.path.exists(cover_text_file):
                raise FileNotFoundError(f"Cover text file not found: {cover_text_file}")
            if not os.path.exists(secret_text_file):
                raise FileNotFoundError(f"Secret text file not found: {secret_text_file}")
            
            # Read cover text
            with open(cover_text_file, 'r', encoding='utf-8') as cover_file:
                cover_text = cover_file.read()
            
            # Read secret text
            with open(secret_text_file, 'r', encoding='utf-8') as secret_file:
                secret_text = secret_file.read()
            
            if not cover_text or not secret_text:
                raise ValueError("Either cover text or secret text is empty.")
            
            # Convert secret text to zero-width character representation
            zero_width_secret = self._to_zero_width(secret_text)
            
            # Combine cover text and zero-width secret text
            combined_text = cover_text + zero_width_secret
            
            # Write to output file
            with open(output_text_file, 'w', encoding='utf-8') as output_file:
                output_file.write(combined_text)
            
            print("Embedding successful!")
        except Exception as e:
            print(f"Error during embedding: {e}")

    def extract(self, stego_text_file, output_text_file):
        """
        Extract secret text from the stego text file using zero-width characters.
        """
        try:
            # Ensure file exists
            if not os.path.exists(stego_text_file):
                raise FileNotFoundError(f"Stego text file not found: {stego_text_file}")
            
            with open(stego_text_file, 'r', encoding='utf-8') as stego_file:
                stego_text = stego_file.read()
            
            if not stego_text:
                raise ValueError("Stego file is empty.")
            
            # Extract zero-width character representation from the stego text
            zero_width_secret = ''.join(char for char in stego_text if char in ['\u200b', '\u200c'])
            
            if not zero_width_secret:
                raise ValueError("No hidden secret text found.")
            
            # Convert zero-width character representation back to secret text
            secret_text = self._from_zero_width(zero_width_secret)
            
            # Write secret text to output file
            with open(output_text_file, 'w', encoding='utf-8') as output_file:
                output_file.write(secret_text)
            
            print("Extraction successful!")
        except Exception as e:
            print(f"Error during extraction: {e}")

# Example usage:
text_stg = TextStg()
text_stg.embed('cover.txt', 'secret.txt', 'output.txt')
text_stg.extract('output.txt', 'extracted_secret.txt')
