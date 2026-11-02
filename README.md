# 🚀 NexPost AI — Generative AI Content Studio

**Final Year Engineering Capstone Project | 2026**

**Developed by Kartikey Sabharwal**

NexPost AI is an intelligent LinkedIn content generation and optimization platform powered by **Python, Streamlit, and Groq LLMs**. It uses Few-Shot In-Context Learning and prompt engineering to generate engaging, professional, and personalized social media content.

## ✨ Key Features

- 🤖 **3-Variation AI Generator:** Generate Professional, Storytelling, and Engaging LinkedIn posts.
- ✍️ **AI Content Rewriter:** Improve grammar, hooks, readability, hashtags, and engagement.
- 🎯 **Smart Customization:** Select tone, target audience, language, and post length.
- 📊 **Content Quality Scoring:** Transparent heuristic-based evaluation of generated posts.
- ⚡ **Multi-Model Comparison:** Compare Groq LLMs based on response time and output quality.
- 📈 **Analytics Dashboard:** Track generated posts and performance metrics using SQLite and Plotly.
- 📄 **PDF Export:** Download generated content and reports.
- 🧠 **Few-Shot Prompt Engineering:** Generate context-aware content using example-based prompting.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | Web interface |
| Groq API | LLM inference |
| GPT-OSS | Generative AI model |
| SQLite | Data storage |
| Plotly | Data visualization |
| ReportLab | PDF generation |

## 🚀 Run Locally

**1. Open the project folder in your terminal.**

**2. Activate the virtual environment:**

```bash
source venv/bin/activate
```

**3. Configure your Groq API key:**

```bash
export GROQ_API_KEY="your_api_key"
```

**4. Launch the application:**

```bash
streamlit run main.py
```

**5. Open the application:**

🌐 **http://localhost:8501**

## 🏗️ Project Workflow

```text
User Input
    ↓
Streamlit Interface
    ↓
Few-Shot Prompt Engineering
    ↓
Groq LLM Inference
    ↓
AI Content Generation
    ↓
Quality Scoring & Optimization
    ↓
SQLite Database & Analytics
    ↓
LinkedIn Post Preview / PDF Export
```

## 🎯 Project Objective

To develop an AI-powered platform that automates professional content creation, improves writing quality, and analyzes generated posts through transparent scoring and real-time LLM performance comparison.

## 🔮 Future Scope

- LinkedIn API integration
- Automated post scheduling
- AI-based image generation
- Personalized content recommendations
- Engagement prediction using real-world data

## 👨‍💻 Developer

**Kartikey Sabharwal**

Final Year Engineering Capstone Project — 2026

---

© 2026 Kartikey Sabharwal | NexPost AI | All Rights Reserved
