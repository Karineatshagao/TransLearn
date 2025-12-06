import streamlit as st
import pandas as pd
import openai
from google import genai
from io import BytesIO
import json

# Page configuration
st.set_page_config(
    page_title="TransLearn - Learn While You Translate",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for vocabulary storage
if 'vocabulary_db' not in st.session_state:
    st.session_state.vocabulary_db = pd.DataFrame(columns=[
        'Japanese', 'Reading', 'Thai', 'Type', 'Example', 'Notes'
    ])

if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None

if 'current_vocabulary' not in st.session_state:
    st.session_state.current_vocabulary = None

# Sidebar for API Keys
st.sidebar.title("🔑 API Configuration")

api_choice = st.sidebar.radio(
    "Select API to use:",
    ["OpenAI", "Google Gemini"],
    help="Choose which AI service to use for translation"
)

# Conditionally show API key input and model selection based on choice
if api_choice == "OpenAI":
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key"
    )
    openai_model = st.sidebar.selectbox(
        "Select OpenAI Model",
        [
            "gpt-5.1-2025-11-13",
            "gpt-5-mini-2025-08-07",
            "gpt-5-nano-2025-08-07"
        ],
        index=1,
        help="Choose which OpenAI model to use"
    )
    gemini_api_key = None
    gemini_model = None
else:  # Google Gemini
    gemini_api_key = st.sidebar.text_input(
        "Google Gemini API Key",
        type="password",
        help="Enter your Google Gemini API key"
    )
    gemini_model = st.sidebar.selectbox(
        "Select Gemini Model",
        [
            "gemini-3-pro-preview",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
            "gemini-2.0-flash-exp"
        ],
        index=1,
        help="Choose which Gemini model to use"
    )
    openai_api_key = None
    openai_model = None

st.sidebar.markdown("---")
st.sidebar.markdown("### About TransLearn")
st.sidebar.info(
    "TransLearn helps you learn Japanese while translating! "
    "Translate Japanese text to Thai and build your vocabulary database."
)

# Main app
st.title("📚 TransLearn")
st.subheader("Learn While You Translate - Japanese to Thai")
st.markdown("---")

# Function to translate using OpenAI
def translate_with_openai(text, api_key, model):
    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""You are a professional Japanese to Thai translator and language teacher.

Task:
1. Translate the following Japanese text to Thai accurately.
2. Extract important vocabulary, phrases, and grammar patterns that would be valuable for a learner.

Japanese text:
{text}

Please respond in the following JSON format:
{{
    "translation": "Thai translation here",
    "learning_items": [
        {{
            "japanese": "Japanese word/phrase/grammar",
            "reading": "Reading in hiragana or romaji",
            "thai": "Thai meaning",
            "type": "word/phrase/grammar",
            "example": "Example sentence in Japanese",
            "notes": "Explanation or additional notes"
        }}
    ]
}}

Important:
- Extract 5-10 most important learning items
- Include a mix of vocabulary, phrases, and grammar patterns
- Prioritize items that are useful and commonly used
- Provide clear explanations in the notes field IN THAI
- Respond ONLY with valid JSON, no additional text
"""

        # Use Responses API for GPT-5 models
        response = client.responses.create(
            model=model,
            input=prompt,
            reasoning={"effort": "low"},  # Fast responses for translation tasks
            text={"verbosity": "medium"}
        )

        # Parse the JSON response
        result = json.loads(response.output_text)
        return result

    except Exception as e:
        st.error(f"Error with OpenAI API: {str(e)}")
        return None

# Function to translate using Gemini
def translate_with_gemini(text, api_key, model_name):
    try:
        # Use new Gemini API client
        client = genai.Client(api_key=api_key)

        prompt = f"""You are a professional Japanese to Thai translator and language teacher.

Task:
1. Translate the following Japanese text to Thai accurately.
2. Extract important vocabulary, phrases, and grammar patterns that would be valuable for a learner.

Japanese text:
{text}

Please respond in the following JSON format:
{{
    "translation": "Thai translation here",
    "learning_items": [
        {{
            "japanese": "Japanese word/phrase/grammar",
            "reading": "Reading in hiragana or romaji",
            "thai": "Thai meaning",
            "type": "word/phrase/grammar",
            "example": "Example sentence in Japanese",
            "notes": "Explanation or additional notes"
        }}
    ]
}}

Important:
- Extract 5-10 most important learning items
- Include a mix of vocabulary, phrases, and grammar patterns
- Prioritize items that are useful and commonly used
- Provide clear explanations in the notes field IN THAI
- Respond ONLY with valid JSON, no additional text
"""

        # Use new Gemini API method
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        result_text = response.text.strip()

        # Try to extract JSON from the response
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        result = json.loads(result_text)
        return result

    except Exception as e:
        st.error(f"Error with Gemini API: {str(e)}")
        return None

# Main translation interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🇯🇵 Japanese Input")
    japanese_input = st.text_area(
        "Enter Japanese text to translate:",
        height=200,
        placeholder="例えば、ここに日本語を入力してください..."
    )

    translate_button = st.button("🔄 Translate & Extract Learning Items", type="primary", width="stretch")

with col2:
    st.markdown("### 🇹🇭 Thai Translation")
    translation_placeholder = st.empty()

# Translation logic
if translate_button:
    if not japanese_input.strip():
        st.warning("Please enter some Japanese text to translate.")
    elif api_choice == "OpenAI" and not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif api_choice == "Google Gemini" and not gemini_api_key:
        st.error("Please enter your Google Gemini API key in the sidebar.")
    else:
        with st.spinner("Translating and analyzing..."):
            if api_choice == "OpenAI":
                result = translate_with_openai(japanese_input, openai_api_key, openai_model)
            else:
                result = translate_with_gemini(japanese_input, gemini_api_key, gemini_model)

            if result:
                st.session_state.translation_result = result['translation']
                # Ensure proper column order and naming
                learning_items_df = pd.DataFrame(result['learning_items'])

                # Check if columns are already capitalized or lowercase
                has_lowercase = any(col in learning_items_df.columns for col in ['japanese', 'reading', 'thai', 'type', 'example', 'notes'])
                has_capitalized = any(col in learning_items_df.columns for col in ['Japanese', 'Reading', 'Thai', 'Type', 'Example', 'Notes'])

                # Only rename if columns are lowercase
                if has_lowercase and not has_capitalized:
                    column_mapping = {
                        'japanese': 'Japanese',
                        'reading': 'Reading',
                        'thai': 'Thai',
                        'type': 'Type',
                        'example': 'Example',
                        'notes': 'Notes'
                    }
                    learning_items_df = learning_items_df.rename(columns=column_mapping)

                # Ensure all required columns exist
                required_cols = ['Japanese', 'Reading', 'Thai', 'Type', 'Example', 'Notes']
                for col in required_cols:
                    if col not in learning_items_df.columns:
                        learning_items_df[col] = ''

                # Select only the required columns in the correct order
                st.session_state.current_vocabulary = learning_items_df[required_cols].copy()
                st.success("Translation completed!")
                st.rerun()

# Display translation
if st.session_state.translation_result:
    with col2:
        translation_placeholder.text_area(
            "Translation:",
            value=st.session_state.translation_result,
            height=200,
            disabled=True
        )

# Display and manage vocabulary
if st.session_state.current_vocabulary is not None and not st.session_state.current_vocabulary.empty:
    st.markdown("---")
    st.markdown("### 📖 Learning Items from Current Translation")

    # Display current vocabulary
    st.dataframe(
        st.session_state.current_vocabulary,
        width="stretch",
        hide_index=True
    )

    # Add to global database
    col_add, col_clear = st.columns([1, 1])
    with col_add:
        if st.button("➕ Add All to My Vocabulary Database", width="stretch"):
            # Concatenate and remove duplicates based on Japanese word
            st.session_state.vocabulary_db = pd.concat(
                [st.session_state.vocabulary_db, st.session_state.current_vocabulary],
                ignore_index=True
            ).drop_duplicates(subset=['Japanese', 'Reading'], keep='first')
            st.success(f"Added {len(st.session_state.current_vocabulary)} items to your vocabulary database!")
            st.session_state.current_vocabulary = None
            st.rerun()

    with col_clear:
        if st.button("🗑️ Clear Current Items", width="stretch"):
            st.session_state.current_vocabulary = None
            st.rerun()

# Global vocabulary database
st.markdown("---")
st.markdown("### 📚 My Vocabulary Database")
st.markdown(f"**Total items: {len(st.session_state.vocabulary_db)}**")

if not st.session_state.vocabulary_db.empty:
    # Editable dataframe
    st.markdown("#### Edit Your Vocabulary")
    edited_df = st.data_editor(
        st.session_state.vocabulary_db,
        width="stretch",
        num_rows="dynamic",
        key="vocab_editor"
    )

    # Update the session state with edited data
    col_save, col_remove_dupes = st.columns([1, 1])
    with col_save:
        if st.button("💾 Save Changes", type="primary", width="stretch"):
            st.session_state.vocabulary_db = edited_df
            st.success("Changes saved!")
            st.rerun()

    with col_remove_dupes:
        if st.button("🧹 Remove Duplicates", width="stretch"):
            original_count = len(st.session_state.vocabulary_db)
            st.session_state.vocabulary_db = st.session_state.vocabulary_db.drop_duplicates(
                subset=['Japanese', 'Reading'],
                keep='first'
            ).reset_index(drop=True)
            new_count = len(st.session_state.vocabulary_db)
            removed = original_count - new_count
            st.success(f"Removed {removed} duplicate entries!")
            st.rerun()

    # Download options
    st.markdown("#### 📥 Download Your Vocabulary")
    col_csv, col_excel, col_clear_all = st.columns([1, 1, 1])

    with col_csv:
        csv = st.session_state.vocabulary_db.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="translearn_vocabulary.csv",
            mime="text/csv",
            width="stretch"
        )

    with col_excel:
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.vocabulary_db.to_excel(writer, index=False, sheet_name='Vocabulary')
        excel_data = output.getvalue()

        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name="translearn_vocabulary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch"
        )

    with col_clear_all:
        if st.button("🗑️ Clear All Data", width="stretch"):
            if st.session_state.get('confirm_clear', False):
                st.session_state.vocabulary_db = pd.DataFrame(columns=[
                    'Japanese', 'Reading', 'Thai', 'Type', 'Example', 'Notes'
                ])
                st.session_state.confirm_clear = False
                st.success("All vocabulary data cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm clearing all data.")

else:
    st.info("Your vocabulary database is empty. Translate some Japanese text and add learning items to build your collection!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>TransLearn - Learn While You Translate | Japanese to Thai Translation & Vocabulary Builder</p>
    </div>
    """,
    unsafe_allow_html=True
)
