# -*- coding: utf-8 -*-
"""Copy of TTS2Speechw.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/157Keeu3bfVlFdAZoka6touL-mLBwL8xs
"""

pip install replicate



pip install PyPDF2

from replicate.client import Client
import replicate

"""Replicate API

"""

replicate = replicate.Client(api_token='r8_aOIl4VQL6ApOSme2Jec3T4WKXW8fVWC2yE9ZP')

from google.colab import files
from PyPDF2 import PdfReader
import io

# Step 1: Choose a PDF file
uploaded = files.upload()

# Check if file is PDF, if not, prompt user to choose again
file_name = list(uploaded.keys())[0]
while not file_name.endswith('.pdf'):
    print("Uploaded file is not a PDF. Please upload a PDF file.")
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]

# Save the PDF file to a folder inside Google Colab
with open(file_name, 'wb') as f:
    f.write(uploaded[file_name])

# Step 2: Convert PDF file to text
pdf_text = ''
with open(file_name, 'rb') as f:
    pdf_reader = PdfReader(f)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()

# Step 3: Display proof that the file has text inside it
#print("Extracted text from PDF:")
#print(pdf_text[:500])  # Displaying the first 500 characters as proof

# Step 4: Save text to a file
#text_file_name = file_name.replace('.pdf', '.txt')
#with open(text_file_name, 'w') as f:
#    contentH=f.write(pdf_text)

#contentH+=contentH
# Step 5: Displaying human-readable text (decoded properly)
#with open(text_file_name, 'r') as f:
#    print(f.read())
#    human_readable_text = f.read()
#    #print(human_readable_text)
#    f_content = f.read()
#    print(f_content)

#escaped_text = human_readable_text.replace('"', r'\"')
#f'"{human_readable_text}"'
##api_input_text = f'"{pdf_text}"'

# Initialize variables
current_page = 0

# Split the text into words
words = pdf_text.split()
audio_files = []  # Initialize an empty list to store output MP3 files

# Process 20 words at a time
word_count = 0
start_index = 0
chunks = []

while start_index < len(words):
    end_index = min(start_index + 20, len(words))
    chunk = ' '.join(words[start_index:end_index])
    chunks.append(chunk)
    start_index = end_index

    # If we have accumulated 4 chunks or reached the end of the text
    if len(chunks) == 2 or start_index == len(words):
        # Join the chunks into a single variable
        api_input_text = '\n'.join(chunks)

        # Call the API with the concatenated chunks
        output = replicate.run(
            "adirik/styletts2:989cb5ea6d2401314eb30685740cb9f6fd1c9001b8940659b406f952837ab5ac",
            input={
                "beta": 0.7,
                "seed": 0,
                "text": api_input_text,
                "alpha": 0.3,
                "diffusion_steps": 10,
                "embedding_scale": 1.5
            }
        )

        # Assuming output is the MP3 file obtained from the API call
        audio_files.append(output)  # Append the MP3 file to the list

        # Reset chunks for the next cycle
        chunks = []

print(audio_files)

pip install requests



from moviepy.editor import concatenate_audioclips, AudioFileClip
import requests

# Step 1: Import requests



for i, url in enumerate(audio_files):
    response = requests.get(url)
    with open(f'audio{i+1}.mp3', 'wb') as f:
        f.write(response.content)

# Step 3: Create AudioFileClip objects for each downloaded MP3 file
audio_clips = []
for i in range(len(audio_files)):
    audio_clips.append(AudioFileClip(f'audio{i+1}.mp3'))

# Step 4: Concatenate AudioFileClip objects
concatenated_clip = concatenate_audioclips(audio_clips)

# Step 5: Write the concatenated audio to a file named 'playerOutput.mp3'
concatenated_clip.write_audiofile('playerOutput.mp3')