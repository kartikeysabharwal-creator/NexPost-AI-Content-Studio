# 🚀 NexPost AI — Generative AI Content Studio

**An AI-powered LinkedIn Content Generation and Optimization Platform**

NexPost AI is a Generative AI application built using **Python, Streamlit, and Groq LLMs**. It helps users create, rewrite, analyze, and optimize professional LinkedIn content through advanced prompt engineering and AI-powered insights.

## ✨ Features

- 🤖 **AI Post Generator:** Generate three unique LinkedIn post variations.
- ✍️ **Content Rewriter:** Improve existing posts with AI-powered rewriting.
- 🎯 **Audience Targeting:** Customize content based on audience, topic, and tone.
- 🌍 **Multilingual Generation:** Generate posts in supported languages.
- 📊 **Content Quality Scoring:** Evaluate AI-generated content using quality indicators.
- ⚡ **Model Comparison:** Compare LLM outputs and inference latency.
- 📈 **Performance Dashboard:** Visualize content statistics and generation metrics.
- 🧠 **Few-Shot Prompt Engineering:** Improve generation consistency through example-based prompting.
- 🎨 **Interactive Interface:** Modern web dashboard developed with Streamlit.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Streamlit | Interactive web interface |
| Groq API | LLM inference |
| GPT-OSS | AI content generation |
| Pandas | Data processing and analysis |
| Plotly | Interactive data visualization |
| Prompt Engineering | Content generation and optimization |

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/NexPost-AI.git
cd NexPost-AI
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository name.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API Key

Get your API key from [Groq Console](https://console.groq.com/keys).

Set it in your Mac Terminal:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Never commit API keys or credentials to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

Replace `app.py` with your actual Streamlit entry-point filename if different.

Open the application in your browser:

**http://localhost:8501**

## 🧠 How It Works

1. The user enters a topic and selects the desired language, tone, and post length.
2. NexPost AI constructs a customized prompt using the selected parameters.
3. The prompt is sent to a Groq-hosted large language model.
4. The model generates multiple LinkedIn post variations.
5. The application presents the generated content along with quality indicators and analysis.
6. Users can review, refine, and copy their preferred content.

## 🏗️ System Architecture

```text
            User Input
                |
                v
         Streamlit Interface
                |
                v
       Prompt Engineering Layer
                |
                v
           Groq LLM API
                |
                v
       AI-Generated Content
                |
        +-------+-------+
        |       |       |
        v       v       v
     Rewrite  Quality  Model
              Scoring  Comparison
        |       |       |
        +-------+-------+
                |
                v
        Results Dashboard
```

## 📊 Evaluation and Analytics

NexPost AI provides content analysis and performance indicators, including:

- Content quality scores
- Word count and readability-related metrics
- LLM response latency
- Comparative model performance
- Generated content statistics

**Note:** Content quality scores are application-level estimates and should not be interpreted as guaranteed predictions of actual LinkedIn engagement or virality.

## 🎯 Applications

NexPost AI can assist:

- Students and job seekers
- Content creators
- Marketing professionals
- Entrepreneurs
- LinkedIn users developing their professional presence

## 🔮 Future Enhancements

- AI-powered hashtag recommendations
- Automated content scheduling
- Retrieval-augmented generation (RAG)
- LinkedIn API integration
- Multimodal content generation
- Personalized content recommendations
- Engagement analytics using real platform data

## 📚 Academic Project

**Project Name:** NexPost AI — Generative AI Content Studio

**Project Type:** Final-Year Capstone Project

**Domain:** Generative Artificial Intelligence, Natural Language Processing, and Prompt Engineering

**Developer:** Kartikey Sabharwal

## 🔒 Security

Groq API keys must be stored securely using environment variables or a secrets-management mechanism. Sensitive credentials should never be included in public repositories.

## 📄 License

This project is developed for educational and academic purposes. Refer to the repository's `LICENSE` file for the applicable permissions, if provided.

---

⭐ **If you find NexPost AI useful, consider starring the repository!**

**Developed by Kartikey Sabharwal**
