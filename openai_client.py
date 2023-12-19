import openai
import configparser
import requests
import json
import time

class OpenAI:

    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        # Initialize conversation history
        self.conversation_history = []

        # Set your API key
        openai.api_key = config.get('openai', 'openai_api_key')

    def reset_conversation(self):
        self.conversation_history = []

    #"gpt-3.5-turbo" or "gpt-4"
    def send_to_chatgpt(self, model_version, messages_to_send):
        try:
            # Send prompt request with conversation history
            response = openai.chat.completions.create(
                model=model_version,
                messages=messages_to_send,
                temperature=0.2,
                frequency_penalty=0.8,
                max_tokens=1000,
            )
        except Exception as e:
            print(f"Server is overloaded or not ready yet. Retrying in 5 minutes...{e}")
            time.sleep(300)  # Delay for 5 minutes (300 seconds)
            return self.send_to_chatgpt(self, model_version, messages_to_send)

        total_tokens = response.usage.total_tokens
        print(f"Total tokens used: {total_tokens}")

        return response.choices[0].message.content

    # Function to send a prompt and keep Chat history for context
    # add_to_hist - if we want to add this to previous conversation history so this responce is sent next time to ChatGPT as context
    def get_chat_response(self, model_version, prompt, add_to_hist=False):

        self.conversation_history.append({'role': 'user', 'content': prompt})
        #print(self.conversation_history)
        messages_to_send = self.conversation_history

        # Retrieve assistant's reply
        reply = self.send_to_chatgpt(model_version, messages_to_send)

        if add_to_hist:
            # Append assistant messages to conversation history
            self.conversation_history.append({"role": "assistant", "content": reply})
        else:
            # unset last prompt if we do not want ot keep a history of it
            self.conversation_history.pop()

        return reply

    # Function to send a prompt and not to keep Chat history for context
    def get_prompt_response(self, model_version, prompt):
        messages_to_send = [{'role': 'user', 'content': prompt}]

        # Retrieve assistant's reply
        reply = self.send_to_chatgpt(model_version, messages_to_send)

        return reply

