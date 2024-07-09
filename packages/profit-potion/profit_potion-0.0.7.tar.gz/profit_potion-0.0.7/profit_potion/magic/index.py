"""
This is the main module to make magic
"""

import os
import base64
import json
import requests as rq
from openai import OpenAI


# pylint: disable=too-few-public-methods
class Analyst:
    """
    This is the class Analyst to make magic
    """

    def __init__(self, token: str, telegram_token: str = None, telegram_chat_id: str = None):
        """
        This is the constructor for the Analyst class
        args:
            token: str: This is the openai api key
            telegram_token: str: This is the telegram bot token
            telegram_chat_id: str: This is the telegram chat id
        """
        os.environ["OPENAI_API_KEY"] = token
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

        # Check if openai api key is set
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OpenAI API key is not set")

        self.client = OpenAI()

    def encoding_images(self, images_list: list) -> list:
        """
        This is the method to encode images in bs64 and return a list of strings
        """
        encoded_images = []
        for image in images_list:
            with open(image, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                image_element = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encoded_string}"},
                }

                encoded_images.append(image_element)

        return encoded_images

    def send_message_to_telegram(self, message: str) -> None:
        """
        This is the method to send message to telegram
        """
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"

        # if message is too long, split it and send it in multiple messages
        if len(message) > 4096:
            for i in range(0, len(message), 4096):
                payload = json.dumps({
                    "text": message[i:i + 4096],
                    "chat_id": self.telegram_chat_id
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                _ = rq.request("GET", url, headers=headers, data=payload)
        else:
            payload = json.dumps({
                "text": message,
                "chat_id": self.telegram_chat_id
            })
            headers = {
                'Content-Type': 'application/json'
            }
            _ = rq.request("GET", url, headers=headers, data=payload)


    def analyze_data(
        self,
        images_list: list = None,
        prompt: str = None,
        max_tokens: int = 300,
        model: str = "gpt-4o",
        send_to_telegram: bool = False
    ):
        """
        This is the method to analyze data
        """
        content = [
            {"type": "text", "text": prompt},
        ]

        if images_list:
            encoded_images = self.encoding_images(images_list)
            content.extend(encoded_images)

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens,
        )

        if send_to_telegram:
            self.send_message_to_telegram(response.choices[0].message.content)

        return response.choices[0]
