import time
import requests
from ...utils import encode_image
from PIL import Image
from io import BytesIO
from .model_adapter import BaseModelAdapter
from tqdm import tqdm
from transformers.utils import logging
logging.set_verbosity_error() 

def test_adapter(
    model_adapter: BaseModelAdapter,
):
    image_url = "https://llava.hliu.cc/file=/nobackup/haotian/tmp/gradio/ca10383cc943e99941ecffdc4d34c51afb2da472/extreme_ironing.jpg"
    image = Image.open(BytesIO(requests.get(image_url).content))
    params = {
        "prompt": {
            "text": "What is unusual about this image?",
            "image": encode_image(image)
        },
        "do_sample": False,
        "top_p": 1.0,
        "max_new_tokens": 200,
    }
    print("\n## Testing model generate() method...")
    generated_text = model_adapter.generate(params)
    print("### Final generated text: \n", generated_text['text'])
    
    print("\n## Testing model generate_stream() method")
    streamer = model_adapter.generate_stream(params)
    generated_text = ""
    for text in streamer:
        added_text = text['text'][len(generated_text):]
        generated_text = text['text']
        time.sleep(0.03)
        print(added_text, end='', flush=True)
    print("\n### Final generated text via stream: \n", generated_text)
    
    