# TransLearn - Learn While You Translate

A Streamlit application for translating Japanese text to Thai while building a personalized vocabulary database.

## Features

- **Dual API Support**: Use either OpenAI or Google Gemini API
- **Japanese to Thai Translation**: Accurate translation powered by AI
- **Smart Vocabulary Extraction**: Automatically extracts important words, phrases, and grammar patterns
- **Persistent Vocabulary Database**: Build your learning collection across sessions
- **Editable Database**: Add, edit, or delete vocabulary entries
- **Export Options**: Download your vocabulary as CSV or Excel files
- **User-Friendly Interface**: Clean, intuitive design with real-time updates

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd llm_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Enter API Key**: In the sidebar, enter your OpenAI or Google Gemini API key
2. **Select API**: Choose which API service to use
3. **Paste Japanese Text**: Enter the Japanese text you want to translate
4. **Translate**: Click the "Translate & Extract Learning Items" button
5. **Review**: Check the translation and extracted learning items
6. **Add to Database**: Add useful items to your vocabulary database
7. **Edit & Download**: Edit your database and download as CSV or Excel