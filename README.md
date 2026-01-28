<p align="center">
<svg width="400" height="80" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a78bfa"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif"
        font-size="48" font-weight="700"
        letter-spacing="1"
        fill="url(#gradient)"
        filter="url(#glow)">
    PyCoder
  </text>
</svg>
</p>

**PyCoder** is an AI-powered chatbot built on a **QLoRA-quantized DeepSeek-Coder-1B** model fine-tuned using **LoRA-based SFT**. It generates high-quality Python code and provides clear, human-readable explanations, all while remaining efficient on low-memory GPU setups.


# 🏗️ Model Architecture & Training

* Base Model:  

      deepseek-ai/deepseek-coder-1.3b-instruct

* Quantization: QLoRA (4-bit)

* Fine-Tuning Method: Supervised Fine-Tuning (SFT)

* Adapters: LoRA

* Dataset: 

      iamtarun/python_code_instructions_18k_alpaca

      teknium/OpenHermes-2.5

* Primary Task: Python code generation & explanation

* Fine-tuned model 

        Hhsjsnns/PyCoder-QLoRA-v1




---------

# ⚙️ Setup Instructions

1️⃣ Clone the repository
```bash
git clone https://github.com/BhagwatiOracle/PyCoder.git

cd PyCoder
```

2️⃣ Create a virtual environment
```bash
python -m venv venv

source venv/bin/activate     # Windows: venv\Scripts\activate
```

3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Run the app
```bash
python app.py
```
---

# 🎬Demo

<details>
  <summary><strong>📌 Click to expand Demo Video</strong></summary>

  <br>

  <div align="center">
    <video width="640" height="360" controls>
      <source src="assets\demo.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  </div>

  <br>
</details>





