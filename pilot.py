import streamlit as st
import openai
import os
import base64
import tempfile
import requests

#api_key_ = os.getenv("GPT_KEY")
api_key_ = ''

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key_}"
    }

st.title('Image Captening demo')

url_placeholder = st.empty()
img_url = url_placeholder.text_input(label='image url')

drop_placeholder = st.empty()
drop_img = drop_placeholder.file_uploader("upload image")

if img_url:
    drop_placeholder.empty()

if drop_img is not None:
    url_placeholder.empty()
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, drop_img.name)
    with open(path, "wb") as f:
        f.write(drop_img.getvalue())
    #print('path: ',path)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def drop_process():
    base64_image = encode_image(path)

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Generate a detailed caption for the image"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

def url_generate_text(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    print(response)
    return response.choices[0].text.strip()


def url_Process_image():
    prompt = f"Generate a detailed caption for the image at the given URL: {img_url}"
    generated_text = url_generate_text(prompt, api_key_)
    characters_per_line = 50
    captions = ""
    for i in range(0, len(generated_text), characters_per_line):
        captions += (generated_text[i : i + characters_per_line])
    return captions


if st.button("Generate Caption"):
    if img_url:
        caption=url_Process_image()
        st.image(img_url)
        st.write(caption)
    
    if drop_img:
        st.image(drop_img)
        caption = drop_process()
        st.write(caption)