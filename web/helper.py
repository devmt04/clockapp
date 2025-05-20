import pyautogui
import pytesseract
# import openai
from google import genai

from pynput import keyboard
from PIL import Image
import time
import os
import config
import threading



import mss
import mss.tools


# Set your OpenAI API key
# openai.api_key = config.KEY

# Optional: Set tesseract path if it's not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ans = "no answer"
count = 1
# client = openai.OpenAI(api_key=config.KEY)

client = genai.Client(api_key=config.KEY)

def take_screenshot():
    global count
    os.makedirs("ss", exist_ok=True)
    filepath = f"ss/{count}.png"
    count += 1
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
    return filepath
   # # os.makedirs("ss", exist_ok=True)
   #  global count
   #  filepath = f"/home/mohit/Downloads/sea/opt/CodeTantraSEA/web/ss/{count}.png"
   #  count +=1
   #  screenshot = pyautogui.screenshot()
   #  screenshot.save(filepath)
   #  return filepath

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def ask_openai_question(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=["Here is text extracted from a image, featuring a Examination question with 4 options. Which one is correct option? Avoid explanation, just let me know which option is correct followed by little necessary explanation. The extracted text is: "+question]
        )

        return response.text.strip()
    except Exception as e:
        return f"Error calling API: {e}"

def broadcast():
    return ans


def begin():
    while True:
        time.sleep(15)
        path = take_screenshot()
        print(f"Screenshot {count} saved to {path}")
        text = extract_text_from_image(path)
        print("Extracted text:")
        print(text)
        print("Querying API...")
        answer = ask_openai_question(text)
        print("Answer:")
        print(answer)
        global ans
        ans = answer

def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l:
            pressed_keys.add('ctrl')
        elif hasattr(key, 'char') and key.char == 'm':
            if 'ctrl' in pressed_keys:
                print("Ctrl+M detected. Taking screenshot...")
                global ans 
                ans = "Starting.."
                begin()


    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.ctrl_l:
        pressed_keys.discard('ctrl')

pressed_keys = set()


def start():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("Listening for Ctrl+M...")
        listener.join()


def execute():
    thread = threading.Thread(target=start)
    thread.daemon = True
    thread.start()


