from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from threading import Thread
from typing import List
from transformers import AutoModelForCausalLM , AutoTokenizer, TextIteratorStreamer
import uvicorn
import torch
import os


MODEL_NAME = "BhagwatiOracle/PyCoder-QLoRA-v1"

torch.set_num_threads(os.cpu_count())

print(f"Loading model: {MODEL_NAME} ...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype="auto", device_map="auto")
model.eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
print("Model loaded.")


app = FastAPI(title='PyCoder API')

class ChatRequest(BaseModel):
    message: str
    max_new_token: int = 300
    history: List[dict] = []




@app.post('/chat')
def chat(req:ChatRequest):
    messages = [
        {"role": "system", "content": "You are PyCoder, an expert Python & AI assistant."}
    ]
    for m in req.history:
        if m.get('role') in ("user","assistant") and m.get('content','').strip():
            messages.append({'role':m['role'], "content": m["content"]})
    messages.append({'role': 'user', 'content': req.message})
    
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize = False,
        add_generation_prompt = True
    )

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens = True
    )

    inputs = tokenizer(prompt, return_tensors='pt').to(model.device)

    generation_args = {
        'max_new_tokens': 150,
        'streamer': streamer,
        **inputs
    }

    thread = Thread(
        target = model.generate,
        kwargs=generation_args,
    ) 

    thread.start()

    def generate():
        for token in streamer:
            yield token

    thread.join()

    return StreamingResponse(generate(), media_type='text/plain')


@app.get('/health')
def health():
    return {'status':'ok','model': f'{MODEL_NAME} running !'}

#---------------------------------APP___________________________________



