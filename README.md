# 🧮 Maths Problem Solver

Solve mathematical problems using advanced Large Language Models (LLMs) and symbolic computation tools, all in one interactive app!

---
<img width="1920" height="1080" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/c33f02e2-9ba4-4ca0-911e-3ef5f7c25f33" />
<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/5d3e16c6-2aa8-47a3-ac08-f3adaab57f5a" />
<img width="1920" height="1080" alt="Screenshot (1)" src="https://github.com/user-attachments/assets/73c71d14-cd58-4c7b-94b2-6f885e31ef2b" />
---

## 🚀 Features

- **Natural language math problem solving**  
  Ask math questions in plain English and get step-by-step solutions.

- **Symbolic computation (SymPy)**  
  Perform algebra, calculus, equation solving, and more.

- **Wikipedia search integration**  
  Get relevant information from Wikipedia for your math queries.

- **Multiple LLM providers**  
  Supports Groq, Ollama, and more.

- **Step-by-step explanations**  
  Detailed, logical breakdowns of solutions.

---

## 🛠️ Quick Start

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/Maths_Problem_Solver.git
cd Maths_Problem_Solver
```

### 2. Install dependencies

```sh
pip install uv
python -m venv .myvenv
source .myvenv/bin/activate  # On Windows: .myvenv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Run the backend

```sh
uvicorn src.ui.fastapi:app --reload
```

### 4. Launch the frontend

```sh
streamlit run src/ui/app.py
```

Or use Docker:

```sh
docker build -t maths_solver .
docker run -p 8000:8000 -p 8501:8501 maths_solver
```

---

## 📚 How to Use

1. **Select your preferred LLM provider and model.**
2. **Enter your math question in natural language.**
3. **View detailed, step-by-step solutions and explanations.**

---

## 🐳 Docker Support

Both FastAPI (API, port 8000) and Streamlit (UI, port 8501) are exposed.  
See the [Dockerfile](Dockerfile) for details.

---

## 💡 About

This project combines the power of LLMs and symbolic math engines to help you solve and understand mathematical problems interactively.

---

## 🤝 Contributing

Pull requests are welcome!  
Please open an issue to discuss your ideas or report bugs.

---

## 📄 License

MIT License

---

## 📧 Contact

For questions or support, open an issue or contact