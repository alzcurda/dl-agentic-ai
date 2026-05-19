import os
import time
import pandas as pd
import base64
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with the provided API key
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    return df

def print_html(content, title=None, is_image=False):
    from IPython.display import display, HTML, Image
    if title:
        print(f"\n--- {title} ---")
    if is_image:
        display(Image(filename=content))
    else:
        print(content)
    print("-" * 40)

def retry_on_429(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except errors.APIError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Rate limit hit or API error: {e}. Retrying in 40 seconds (Attempt {attempt+1}/{max_retries})...")
            time.sleep(40)
        except Exception as e:
            raise e

def _do_get_response(model_name, prompt):
    actual_model = "gemini-2.5-flash"
    response = client.models.generate_content(model=actual_model, contents=prompt)
    return response.text

def get_response(model_name, prompt):
    return retry_on_429(_do_get_response, model_name, prompt)

def encode_image_b64(path):
    with open(path, "rb") as image_file:
        b64_string = base64.b64encode(image_file.read()).decode("utf-8")
    ext = path.split('.')[-1].lower()
    media_type = f"image/{ext}" if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp'] else "image/png"
    return media_type, b64_string

def _do_image_call(model_name, prompt, media_type, b64):
    from google.genai import types
    actual_model = "gemini-2.5-flash"
    image_data = base64.b64decode(b64)
    part = types.Part.from_bytes(data=image_data, mime_type=media_type)
    response = client.models.generate_content(
        model=actual_model,
        contents=[prompt, part]
    )
    return response.text

def image_openai_call(model_name, prompt, media_type, b64):
    return retry_on_429(_do_image_call, model_name, prompt, media_type, b64)

def image_anthropic_call(model_name, prompt, media_type, b64):
    return image_openai_call(model_name, prompt, media_type, b64)

def ensure_execute_python_tags(code):
    if "<execute_python>" not in code:
        return f"<execute_python>\n{code}\n</execute_python>"
    return code
