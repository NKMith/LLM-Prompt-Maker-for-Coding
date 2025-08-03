# LLM Prompt Builder (Local App)

A simple desktop application to help you build large prompts for LLMs (like ChatGPT, Claude, or Gemini) by combining your own prompt with selected local code files and directory structures. Built using **Python** and **Tkinter**.

---

## ✨ Features

- ✅ Input a custom text prompt
- 📂 Select multiple code files to append to the final prompt
- 🔁 Replace files in the selection
- ❌ Remove files from the list
- 🗂️ (Optional) Add a directory structure (visual tree) to your final prompt
- 📋 Generate and view the final combined prompt
- 📎 Copy final prompt to clipboard
- 💾 Save final prompt to a `.txt` file
- ⚠️ Shows a warning if the generated prompt exceeds a safe size limit (default: 400,000 characters)


---
## 🚀 Getting Started

### 1. Install Python

Make sure you have **Python 3.7+** installed.

### 2. Install dependencies (if needed)

This app uses only built-in libraries (`tkinter`, `os`, etc.). No external libraries required.

### 3. Run the App

```bash
python app.py

