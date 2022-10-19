import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np # numpy - expand_dims 
from streamlit_lottie import st_lottie
import streamlit as st
from help import *
from video import *

def main():
    
    st.set_page_config(layout="wide")

    option_type = option_menu(
        menu_title = None,
        options = ["Home","Work","Contact"],
        icons = ["house","gear","envelope"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal",
    )
    
    if option_type == "Home":

        st.markdown("<h1 style='text-align: center; color: #08e08a;'>Virtual Notes Assistant</h1>",unsafe_allow_html=True)
        lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_1GkVPfS0cv.json")

        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # medium ; high
            #renderer="svg", # canvas
            height=400,
            width=-900,
            key=None,
        )        
        st.markdown("<h4 style='text-align: center; color: #dae5e0;'>Upload your audio and get your notes.</h4>",unsafe_allow_html=True)

    elif option_type == 'Work':
        audio = st.file_uploader("Upload audio file", type=['mp3','wav'])
        if audio is not None:
            audio1 = audio.read()
            st.audio(audio1, format='audio/mp3')
            if st.button('Get Text'):
                text = stt(audio.name)
                if text is not None:
                    st.write(text)
                else:
                    st.write('No text found')
        url = st.text_input("Or Enter Your Video URL ")
        if st.button("Get video", key="1", help="Get your video"):
            st.video(url)
            st.write('Working')
            video(url)
            text = stt('audio.wav')
            if text is not None:
                st.write(text)
            else:
                st.write('No text found')
        
        st.text("Or Give your voice")
        if st.button("Click to Record",key="record",help="Click to record your audio"):
            record_state = st.text("Recording...")
            duration = 15  # seconds
            fs = 48000
            myrecording = record(duration, fs)
            record_state.text("Saving sample as sample.mp3")

            path_myrecording = "./sample.mp3"

            save_record(path_myrecording, myrecording, fs)
            record_state.text("Done! Saved sample as sample.mp3")

            st.audio(read_audio(path_myrecording))
            
            text = stt('sample.mp3')
            if text is not None:
                st.write(text)
            else:
                st.write('No text found')


    else:
        st.subheader("About")
        st.text("This is a Virtual Notes Assistant, Made by a students of the IIIT-Kalyani, India.")
        st.text("Jahnavi Pravaleeka Battu")
        st.text("Sai Dileep Kumar Mukkamala")
        st.text("Senior CSE Students @ IIITKalyani")
        st.text("Data Science Enthusiasists.")

        lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_in4cufsz.json")

        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # medium ; high
            #renderer="svg", # canvas
            height=300,
            width=-900,
            key=None,
        )

        
        st.header(":mailbox: Get In Touch With Us!")


        contact_form = """
        <form action="https://formsubmit.co/msaidileepkumar2002@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here"></textarea>
            <button type="submit">Send</button>
        </form>
        """

        st.markdown(contact_form, unsafe_allow_html=True)

        # Use Local CSS File
        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


        local_css("style/style.css")



if __name__ == '__main__':
    main()