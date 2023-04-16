import openai
import urllib.request
from PIL import Image
import streamlit as st
import os
import speech_recognition as sr
from dotenv import load_dotenv

# set api-key
load_dotenv()
APIKEY = os.getenv("APIKEY")
openai.api_key = f"{APIKEY}"


def audio_input():
    # create a recognizer object
    r = sr.Recognizer()

    # use the default microphone as the audio source
    with sr.Microphone() as source:
        # print("Say something!")
        # listen for the audio and capture it
        audio = r.listen(source)

    try:
        # recognize speech using Google Speech Recognition
        text = r.recognize_google(audio)
        # print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))

    return text


def generate_image(image_description):
    # use openai to generate a .png image with the size 512*512
    img_response = openai.Image.create(
        prompt=image_description,
        n=1,
        size="512x512")

    # print(img_response)
    # reterive from dictionary
    img_url = img_response['data'][0]['url']

    # download the image from the URL and save it
    urllib.request.urlretrieve(img_url, 'img.png')
    img = Image.open("img.png")

    return img


def main():
    # page title
    st.title(' Image Generation ')
    st.text('You can enter by voice or by typing')

    st.subheader('Audio')
    if st.button('Audio Input'):
        # record audion and convert to text
        with st.spinner('Say something!'):
            img_description = audio_input()

        # display text details
        st.text_area('Here is what you said', img_description)

        st.info('Generating image for you')
        try:
            generated_img = generate_image(img_description)
        except st.StreamlitAPIException as e:
            st.error('Error: Invalid input value. Please say some words.')

        st.success('Image generate successfully')
        st.image(generated_img)

    st.subheader('Text')
    # text input box for image recognition
    img_description = st.text_input(
        'Please enther the desription of image you imagine')

    if st.button('Generate Image'):
        generated_img = generate_image(img_description)
        st.image(generated_img)


if __name__ == '__main__':
    main()
