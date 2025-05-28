# AI Beat Poet Generator (Gemini API)

This project uses the Google Generative AI (Gemini) API to generate text in the style of Beat Generation poets like Jack Kerouac, Allen Ginsberg, and Lawrence Ferlinghetti. It is part of a research initiative to compare AI-generated literary emulations with original human-authored texts, focusing on cognitive-linguistic markers of creativity.

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-name]
    ```

2.  **Install Python dependencies:**
    Make sure you have Python 3.7+ installed.
    ```bash
    pip install google-generativeai
    ```
    (You might want to use a virtual environment: `python -m venv venv`, then `source venv/bin/activate` or `venv\Scripts\activate`)

3.  **Set up your Google API Key:**
    *   Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   Set this key as an environment variable named `GOOGLE_API_KEY`.
        *   **Linux/macOS (Terminal):**
            ```bash
            export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
            ```
            (Add this line to your `~/.bashrc`, `~/.zshrc`, or shell configuration file for it to persist across sessions.)
        *   **Windows (PowerShell):**
            ```powershell
            $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
            ```
            (To make it persistent, you can add it to your PowerShell profile script. Run `notepad $PROFILE` to edit it.)

## Running the Script

Execute the Python script from your terminal:
```bash
python beat_poet_generator_gemini.py
