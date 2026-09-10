# Clicky

> **Turn any concept into an interactive explanation.**

Clicky is an AI-powered teaching agent that transforms complex ideas into **interactive visual explanations**.

Instead of simply giving you a wall of text, Clicky thinks about **how a concept should be visualized**, builds a diagram around it, adds annotations and interactions, and turns the result into a small interactive learning experience.

**Ask a question → Clicky understands the concept → Clicky designs the explanation → You explore it.**

---

## ✨ Why Clicky?

Most AI explanations look like this:

```text
Question
   ↓
Paragraph
   ↓
Another paragraph
   ↓
"I hope that makes sense."
```

Clicky takes a different approach:

```text
                  ┌─────────────────┐
                  │   Your Concept  │
                  └────────┬────────┘
                           │
                    AI Agent reasons
                           │
                           ▼
              ┌────────────────────────┐
              │ Visual representation  │
              │ + explanations         │
              │ + interactions         │
              └────────────┬───────────┘
                           │
                           ▼
                  🖱️ Interactive lesson
```

The goal is simple:

**Don't just explain the concept. Let the user explore it.**

---

## 🎯 What Clicky Can Do

Give Clicky almost any concept:

```text
"Explain how a neural network works"
```

```text
"Explain the TCP three-way handshake"
```

```text
"How does a compiler work?"
```

```text
"Explain photosynthesis"
```

```text
"Show me how an operating system schedules processes"
```

And Clicky can turn the idea into an interactive visualization.

### Examples

* 🧠 Neural networks
* 🌐 Networking protocols
* ⚙️ Operating systems
* 💻 Algorithms
* 🔐 Cryptography
* 📦 Distributed systems
* 🧬 Biology
* ⚛️ Physics
* 📊 Data structures
* 🤖 AI concepts
* 🏗️ Software architecture
* ...and much more

---

## 🎨 Clean Diagram + Human Annotations

Clicky combines visual diagrams with contextual explanations.

### Diagram layer

The concept can be represented using:

* Clean shapes
* Nodes
* Arrows
* Connectors
* Structured layouts

### Annotation layer

The explanation can include:

* Informal explanations
* Callouts
* Key principles
* Short notes
* Visual hints

This creates a balance between **technical clarity** and a **whiteboard teaching feel**.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kavi-yara-san/Clicky.git
cd Clicky
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the model


Create a `.env` file in the project root with your API key:

​```bash
API_KEY=your-api-key-here
​```

Then edit `config/config.yaml` to set your model name:

​```yaml
model:
  name: your-model-name
​```
### 5. Run Clicky

```bash
uvicorn main:app --reload  
```

---

## 💡 Example Prompts

### Computer Science

```text
Explain how a hash table works.
```

```text
Visualize how a CPU cache works.
```

```text
Explain the TCP three-way handshake interactively.
```

### AI

```text
Show me how attention works in a transformer.
```

```text
Explain backpropagation visually.
```

### Physics

```text
Explain how a lever works.
```

```text
Visualize electromagnetic induction.
```

### Biology

```text
Explain how a neuron sends a signal.
```

```text
Show how photosynthesis converts light into energy.
```

### Software Engineering

```text
Explain how a request travels through a web application.
```

```text
Visualize a microservices architecture.
```

---

## 📁 Project Structure

```text
Clicky/
├── agent/
│   ├── core.py
│   └── orchestration.py
│
├── config/
│   ├── config.py
│   └── config.yaml
│
├── llms/
│   └── ...
│
├── prompts/
│   ├── load.py
│   └── sketchy.md
│
├── tools/
│   └── ...
│
├── main.py
├── ui.html
├── requirements.txt
├── LICENSE
└── README.md
```

### Directory Overview

| Path               | Description                                   |
| ------------------ | --------------------------------------------- |
| `agent/`           | Core agent logic and orchestration            |
| `config/`          | Application and model configuration           |
| `llms/`            | LLM provider integrations                     |
| `prompts/`         | System prompts and visualization instructions |
| `tools/`           | Tools available to the agent                  |
| `main.py`          | FastAPI application entry point               |
| `ui.html`          | Frontend interface                            |
| `requirements.txt` | Python dependencies                           |
| `LICENSE`          | Project license                               |
| `README.md`        | Project documentation                         |


## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **Async Python**
* **LLM adapters (currently Gemini only)**
* **HTML5 Canvas**
* **JavaScript**
* **Interactive HTML**
* **Tool-based agent orchestration**

---

## 🤝 Contributing

Contributions are welcome! ❤️

Clicky is an experiment in making AI-generated explanations more **visual, interactive, and useful for learning**.

There are many ways to contribute:

* Improve visualization quality
* Add new visualization patterns
* Improve agent reasoning
* Add new LLM providers
* Improve diagram layouts
* Improve collision detection
* Add new interactive components
* Improve animations
* Improve accessibility
* Improve the UI/UX
* Add example visualizations
* Fix bugs
* Improve documentation

### Development

1. Fork the repository.
2. Create a new branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes.
4. Test your changes.
5. Commit your changes:

```bash
git commit -m "Add my feature"
```

6. Push your branch:

```bash
git push origin feature/my-feature
```

7. Open a Pull Request.

### Pull Requests

When submitting a PR, please try to:

* Keep changes focused.
* Explain what you changed and why.
* Include screenshots or examples for UI/visualization changes.
* Make sure existing functionality still works.
* Update documentation when necessary.

Whether it's a small bug fix, a new visualization idea, or a major improvement — **every contribution is welcome.**

---

## 📜 License

Clicky is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

## ⭐ The Idea

**Any concept can become an interactive experience.**

Give Clicky a concept.

Let the agent figure out how to teach it.

**Learn by exploring.**
