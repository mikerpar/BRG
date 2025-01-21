# BRG
Brain rot generator

How to use:
- fill the background clips folder with your selection of background clips
- Enter your text block in main where theres "enter your text here"
- run the script at main

What you need to set up:
- use pip to install the required packages
    - moviepy
    - google tts
    - google auth
    - if I missed something use the error messages to help you
- Make a folder named "video_output" in the repo
- Make a folder named "audio_workspace" in the repo
- Make a folder named "background_clips" in the repo and fill it with your choice of background footage
- Make a .env file and give it the following items:
GOOGLE_TTS_API_KEY = <YOUR KEY>
GOOGLE_APPLICATION_CREDENTIALS = <YOUR AUTH JSON>
- Then place your google credential json in the repo
  DO NOT SHARE ANY OF YOUR KEYS
- You will also need to set up your google tts under your own account
  or another tts of your choosing (you will have to edit the code in the repo for this)

  WARNING:
  This code is provided as-is and I am not responsible for how you use it. This code is also
  provided for educational purposes only.
