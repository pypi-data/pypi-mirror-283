import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from chatgpt_automation.chatgpt_automation import ChatGPTAutomation

chat = ChatGPTAutomation()

input("if website opened press enter...")

import os

# Get the current working directory
current_path = os.getcwd()

# Join path components
file_path = os.path.join(current_path, ".", "setup.py")

chat.upload_file_for_prompt(file_path)

chat.send_prompt_to_chatgpt("Hello please explain this file for me:")

if chat.check_response_status():
    print(chat.return_last_response())
else:
    print("we have some problem in the send prompt or file to chatgpt pelase contact to the admin")

