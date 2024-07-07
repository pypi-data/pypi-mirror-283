import os
import time
import google.generativeai as genai
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
from aiohttp import ClientSession


listhtml = []

def MaskaWeb(Question, URL):
    global listhtml
    listhtml = []

    getwebsiteHTML(URL)
    
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
                    str(listhtml),
                    "This is the Website\n",
                    "(All info is in the website URL, DON'T TELL ME THAT YOU FOUND IT ON HTML, You Are MaskaAI, an Assistant that helps with every question, so talk like you already know the answer)\n",
                ],
            },
        ]
    )

    response = chat_session.send_message(f"{Question}")

    return response.text

def fetch_html(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to retrieve the URL. Status code: {response.status_code}"

def save_to_list(content):
    listhtml.append(content)

def get_endpoints(base_url):
    endpoints = set()
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                url = link['href']
                full_url = urljoin(base_url, url)
                endpoints.add(full_url)
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {base_url}: {e}")
    return list(endpoints)[:2]

def getwebsiteHTML(url):
    # Clear/Create the output list
    global listhtml
    listhtml = []
    
    # Fetch and save the main URL's HTML
    html_content = fetch_html(url)
    save_to_list(html_content)
    print(f"HTML content of {url} saved to list")

    # Fetch and save HTML of endpoint URLs
    base_url = url if url.startswith("http://") or url.startswith("https://") else "http://" + url
    endpoints = get_endpoints(base_url)
    for endpoint in endpoints:
        html_content = fetch_html(endpoint)
        save_to_list(html_content)
        print(f"HTML content of {endpoint} saved to list")
            


# url = "figma.com"
# message = "Talk to me about Prices of it"
# x = MaskaWeb(message, url)