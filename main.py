#importign required libraries
import speech_recognition as sr
import cv2
import pyttsx3
import os
from openai import OpenAI
import base64
import mimetypes

# Load the image file
img_path = "webcam_photo.jpg"

# Determine the MIME type (e.g., image/jpeg)
img_type, _ = mimetypes.guess_type(img_path)

client = OpenAI(
    # This is the default and can be omitted
    api_key=("YOUR API KEY"),
)



#setting up objects for stt
r = sr.Recognizer()
m = sr.Microphone()
r.dynamic_energy_threshold = True
r.pause_threshold = 0.5

#setting up camera object
cap = cv2.VideoCapture(0) 
#learn AWS


#take in a string and speak it through the headphones
def speaking_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def move_servo(degrees): #implement if time allows
    pass


def get_description_from_image(image,uinput):
   
    # Read the image file and encode it as base64
    with open(image, "rb") as img_file:
        img_b64_str = base64.b64encode(img_file.read()).decode("utf-8")
    prompt = uinput

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are a visual aid please try to explain what you see in the image to the best of your ability, here is the users specific question: "+prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"},
                    },
                ],
            }
        ],
    )

    result = response.choices[0].message.content
    return result

try:
    while True:
        print("Listening!")
        speaking_text("Listening")
        move_servo(0)


        with m as source: audio = r.listen(source)

        print("Interpreting audio")
        speaking_text("Interpreting audio")
        move_servo(90)
        

        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            print("you said",value)
            value = value.lower()
            jarvis_location = value.find('jarvis')

            if jarvis_location != -1:
                uinput = value[(jarvis_location+6):]
                ret, frame = cap.read()

                # Check if the frame was captured successfully
                if ret:
                    # Save the image
                    cv2.imwrite("webcam_photo.jpg", frame)
                speaking_text(get_description_from_image("webcam_photo.jpg",uinput))
                


        except sr.UnknownValueError:
            print("Gibberish Alert")
        except sr.RequestError as e:
            print("Check your wifi; {0}".format(e))
except KeyboardInterrupt:
    pass
