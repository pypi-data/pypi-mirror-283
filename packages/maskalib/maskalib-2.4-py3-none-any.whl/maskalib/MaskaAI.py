import os
import time
import google.generativeai as genai
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
from aiohttp import ClientSession

def MaskaAI(Question, Instruction):
    
    genai.configure(api_key="AIzaSyALOKmYt2F8YbJMfrDDllQRbIiBTZobSpY")

    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 999,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                        Instruction,
                ],
            },
        ]
    )

    response = chat_session.send_message(f"{Question}")

    return response.text
