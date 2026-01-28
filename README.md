<p align="center">
  <img src="assets/pycoder.png" alt="Pycoder" width="40%">
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
  <summary><strong>📌 Click to expand Demo</strong></summary>

  <br>

  <p align="center">
    <img src="assets/demo.gif" width="340" />
  </p>

</details>






