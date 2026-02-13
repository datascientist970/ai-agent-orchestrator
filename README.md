# Agentic AI Platform

![Agentic AI Logo](https://via.placeholder.com/300x100?text=Agentic+AI)

**Agentic AI** is an advanced autonomous agent orchestration platform built with **Django**, **Bootstrap 5**, and **Google Gemini 2.5 Flash API**, capable of executing recursive agent pipelines with memory support (RAG) for research, analysis, and automation tasks.

---

## 🚀 Features

* Multi-agent system for task decomposition, execution, and evaluation.
* RAG-enabled memory with vector search (Qdrant client compatible).
* Gemini 2.5 Flash API integration for content generation and embeddings.
* Interactive **Bootstrap 5** front-end with glitchy neon & robotic UI.
* Real-time task status: Planner → Worker → Evaluator → Final Output.
* Dynamic task ID generation and step-wise output visualization.
* Glassmorphic, futuristic UI with animated grid overlay.

---

## 💻 Tech Stack

* **Backend:** Django 5.1.5, Python 3.12
* **Front-end:** Bootstrap 5, HTML/CSS/JS
* **AI Models:** Google Gemini 2.5 Flash (`generateContent`, `embedContent`)
* **Vector Database:** Qdrant (for memory retrieval)
* **Other Libraries:** `httpx`, `numpy`, `pydantic`

---

## ⚡ Installation

1. **Clone the repo:**

```bash
git clone https://github.com/yourusername/agentic-ai.git
cd agentic-ai
```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```


3. **Set up environment variables:**

Create `.env` in project root:

```env
GEMINI_API_KEY=your_gemini_2_5_flash_api_key
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

4. **Run Django server:**

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🖥️ Usage

1. Enter a task in the **Primary Directive / Task** textarea (e.g., `"Build a multi-agent protein folding system"`).
2. Click **Execute Agents**.
3. Watch the **Planner → Worker → Evaluator → Final Output** pipeline populate dynamically.

The front-end will display:

* Step-wise agent outputs
* Task ID
* Real-time AI feedback

---

## 🔗 Gemini 2.5 Flash Integration

* **Text generation:** `generateContent`
* **Embeddings:** `embedContent` (for RAG / vector memory)
* Make sure to use the correct **model name**:

```python
EMBED_MODEL = "/gemini-embedding-001"
GEN_MODEL = "models/gemini-2.5-flash"
```

---

## 💡 Front-end Highlights

* Neon glitchy headers (`Orbitron`) and tech-style input forms.
* Glassmorphic cards for task input and results.
* Animated loading spinner and step badges.
* Realistic multi-agent workflow simulation.
* Fully responsive with Bootstrap 5.

---

## 🛠️ Customization

* Swap Gemini models in `agents/client.py` for new versions.
* Connect to a live Qdrant instance for RAG memory.
* Extend agent workflows in `agents/agent_graph.py`.
* Adjust front-end styles in `templates/index.html` CSS section.

---

## ⚠️ Notes

* This project is designed for **local development**; production deployment requires proper security and API key management.
* Make sure **Qdrant** is running locally or use a cloud instance.
* CSRF protection is disabled for local testing with `@csrf_exempt`. Re-enable for production.

---

## 🔮 Future Enhancements

* Streaming agent outputs in real-time.
* Multi-agent collaboration and prioritization.
* Gemini 3+ support for advanced reasoning.
* Interactive dashboard for task analytics and memory inspection.

---



Do you want me to do that next?
