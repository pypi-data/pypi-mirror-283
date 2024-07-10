import textract
import os
from openai import OpenAI
from dotenv import set_key
from pathlib import Path

def main():
    filepath = input("Enter the path to the file: ")
    text = extract_text(filepath)
    process_text(text)

def extract_text(file_path):
    text = textract.process(file_path, method='tesseract', language='eng')
    return text.decode("utf-8")

def process_text(text):
    key = os.getenv('OPENAI_API_KEY', None)
    if key is None:
        print(Warning("OPENAI_API_KEY not found, please set it in your environment variables, or you can enter it manually"))
        key = input("Enter your OpenAI API key: ")
        confirm = input("Would you like to save this key in your environment variables? (y/n)[default:n]: ")
        if confirm.lower() == 'y':
            envpath = Path(input("Enter the path to your .env file, or if you don't have one, enter the path where you would like to save it: "))
            envpath.touch(mode=0o600, exist_ok=True)
            set_key(envpath, 'OPENAI_API_KEY', key)
            print("Key saved successfully")
        else:
            print("Key not saved")
    client = OpenAI(api_key=key)
    messages = [
        {
            'role': 'system',
            'content': 'You are a helpful assistant that specializes in extracting the specific information from the text, and providing it in a structured format, such as a JSON object.'
        },
        {
            'role': 'user',
            'content': text
        },
        {
            'role': 'system',
            'content': 'Extract the following information from the text: Name of insurance company(ies) providing the coverage, Limits/amount of insurance purchased, Type of coverage purchased, Policy effective and expiration dates'
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response.choices[0].message.content.strip()+'\n'
    
    with open('output.json', 'w+') as output:
        output.write(answer)
        print('Output saved to output.json')

if __name__ == "__main__":
    main()