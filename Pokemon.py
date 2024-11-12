import os;
import time;
import pyautogui;
import keyboard;
import pytesseract;
from PIL import Image;
import speech_recognition as sr 

# buttonLoc = pyautogui.locateOnScreen("Cookie.png",confidence=0.8)
# pyautogui.moveTo(buttonLoc)
# pyautogui.click(buttonLoc,clicks=(100),interval=0.1)

# Configure pytesseract to use the installed Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path as per your installation

def capture_screen():
    # Take a screenshot of the entire screen and save it to a file
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.convert("RGB")  # Convert to RGB to save as JPEG
    screenshot.save("screenshot.jpg", "JPEG")
    return "screenshot.jpg"

def extract_data_from_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    # Get data from the image using pytesseract
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    return data

def find_word_coordinates(data, word):
    word = word.lower().strip()
    for i, text in enumerate(data['text']):
        if text.lower().strip() == word:
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            return x + w // 2, y + h // 2
    return None

def listen_for_word(language="es-ES"):  # Set default language to Spanish (Spain)
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print(f"Escuchando la palabra en {language}...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            # Listen for speech and recognize it
            audio = recognizer.listen(source, timeout=5)
            word = recognizer.recognize_google(audio, language=language)  # Use the specified language
            print(f"Dijiste: {word}")
            return word
        except sr.UnknownValueError:
            print("Lo siento, no pude entender lo que dijiste.")
            return None
        except sr.RequestError:
            print("Lo siento, hubo un problema con el servicio de reconocimiento de voz.")
            return None

def main():
    print("Presiona 'Esc' para detener el programa en cualquier momento.")
    
    while True:
        # Capture the screen
        image_path = capture_screen()
        
        # Extract data from the screenshot
        data = extract_data_from_image(image_path)
        
        # Extract unique words from the data
        unique_words = set(text.lower().strip() for text in data['text'] if text.strip())
        
        # Print the unique words found
        print("\nPalabras encontradas en la pantalla:")
        for word in sorted(unique_words):
            print(word)
        
        # Listen for a word to click on (in Spanish)
        word_to_search = listen_for_word(language="es-ES")  # Spanish language code
        
        if word_to_search:
            word_to_search = word_to_search.strip().lower()
            # Find the coordinates of the specified word
            coordinates = find_word_coordinates(data, word_to_search)
            if coordinates:
                print(f"La palabra '{word_to_search}' fue encontrada en {coordinates}. Haciendo clic en ella.")
                pyautogui.click(coordinates)
            else:
                print(f"La palabra '{word_to_search}' no fue encontrada en la pantalla.")
        
        # Check if the 'Esc' key is pressed to stop the program
        if keyboard.is_pressed('esc'):
            print("Saliendo del programa.")
            break

if __name__ == "__main__":
    main()