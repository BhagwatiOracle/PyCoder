import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread


model_name =  "Hhsjsnns/PyCoder-QLoRA-v1"

model = AutoModelForCausalLM.from_pretrained(model_name, dtype='auto', device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def PyCoder(message, history):

    messages = [
        {'role': 'system', 'content': "You are a PyCoder, an expert Python & AI assistant."}
    ]


    def extract_text(content):
        if isinstance(content, list):
            return " ".join(
                block.get("text", "") for block in content if isinstance(block, dict)
            )
        return str(content)


    for msg in history:
        role = msg.get("role")
        content = extract_text(msg.get("content"))

        if role in ("user", "assistant") and content.strip():
            messages.append({
                "role": role,
                "content": content
            })
    messages.append({"role": "user", "content": message})

    

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
        'max_new_tokens': 300,
        'streamer': streamer,
        **inputs
    }

    thread = Thread(
        target = model.generate,
        kwargs=generation_args,
    ) 

    thread.start()

    acc_text = ""

    for token in streamer:
        acc_text += token
        yield acc_text



    # Ensure the generation thread completes
    thread.join()




#---------------------UI---------------------------------



with open("style.css", "r", encoding="utf-8") as f:
    css = f.read()

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:

    gr.HTML("""
        <div class="app-header">
            <span class="logo-glow">PyCoder</span>
        </div>
    """)

    with gr.Column(elem_classes="chatbot"):
        gr.ChatInterface(fn=PyCoder)



    

    with gr.Sidebar():


        gr.HTML("""
<div class="settings-card">
    <div class="settings-title">⚙️ Settings</div>

    <div class="settings-item">
        <span>Model</span>
        <span class="settings-badge">PyCoder-QLoRA-v1</span>
    </div>

    <div class="settings-item">
        <span>Max Tokens</span>
        <span class="settings-badge">300</span>
    </div>
</div>
""")



demo.launch(share=True)
