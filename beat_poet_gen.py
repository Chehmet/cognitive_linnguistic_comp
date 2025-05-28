# beat_poet_generator_gemini.py
#
# Description:
# This script uses the Google Generative AI (Gemini) API to generate text
# emulating the style of selected Beat Generation poets.
# It's designed as a starting point for the research project comparing
# AI-generated texts with human-authored Beat poetry.
#
# Requirements:
# - Python 3.7+
# - google-generativeai library (`pip install google-generativeai`)
# - GOOGLE_API_KEY environment variable set with your API key.
#
# Usage:
# python beat_poet_generator_gemini.py
#
# The script will generate texts for predefined prompts. You can modify
# the `POET_PROMPTS` dictionary or the `custom_prompt` variable to experiment.

import google.generativeai as genai
import os

# --- Configuration ---
# Model to use (e.g., 'gemini-pro' for text generation)
MODEL_NAME = "gemini-pro"

# Generation parameters (adjust as needed for creativity vs. coherence)
GENERATION_CONFIG = {
    "temperature": 0.8,       # Controls randomness. Higher values (e.g., 0.8-1.0) are more creative.
    "top_p": 0.9,             # Nucleus sampling.
    "top_k": 40,              # Consider top_k most likely tokens.
    "max_output_tokens": 300, # Maximum length of the generated text.
}

# Safety settings (adjust based on your content policy needs)
# Refer to Gemini API documentation for details on these settings.
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# --- Prompts for Beat Poets ---
# These are examples; you'll want to refine them for your specific research.
POET_PROMPTS = {
    "Jack Kerouac": (
        "Write a 150-200 word poetic prose piece in the style of Jack Kerouac. "
        "Channel his spontaneous 'bop prosody' and themes of jazz, the open road, fleeting moments, "
        "spirituality (especially Buddhist influences), and a sense of melancholic American energy. "
        "Use vivid, stream-of-consciousness imagery, run-on sentences, and capture a raw, immediate feeling. "
        "Imagine neon signs flickering on a rainy city street, the sound of a distant saxophone, "
        "and the yearning for something just beyond the horizon."
    ),
    "Allen Ginsberg": (
        "Generate a 150-200 word poetic passage in the style of Allen Ginsberg, reminiscent of 'Howl' or 'America.' "
        "Employ long, prophetic, Whitmanesque lines, anaphoric repetition (e.g., 'Moloch whose...'), and direct, "
        "unflinching address of socio-political themes. Channel a tone of visionary outrage, despair mixed with "
        "a desperate hope for transcendence, and sharp critiques of modern society. Use raw, visceral language "
        "and imagery that confronts uncomfortable truths."
    ),
    "Lawrence Ferlinghetti": (
        "Compose a 150-200 word poem in the style of Lawrence Ferlinghetti, particularly his 'A Coney Island of the Mind' period. "
        "Use a conversational, accessible, yet witty and observant tone. Focus on imagery of urban landscapes, "
        "commentary on contemporary life, art, and popular culture, often with an undercurrent of questioning, "
        "bemusement, or gentle satire. The language should be clear, with unexpected juxtapositions and a "
        "sense of the poet as an engaged observer of the everyday absurd."
    ),
}

def configure_gemini():
    """Configures the Gemini API with the API key."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your API key to use the Gemini API.")
        print("You can get a key from Google AI Studio: https://aistudio.google.com/app/apikey")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return False

def generate_text_with_gemini(prompt_text, model_name=MODEL_NAME,
                              generation_config=GENERATION_CONFIG,
                              safety_settings=SAFETY_SETTINGS):
    """
    Generates text using the Gemini API based on the provided prompt.

    Args:
        prompt_text (str): The input prompt for the model.
        model_name (str): The name of the Gemini model to use.
        generation_config (dict): Configuration for text generation.
        safety_settings (list): Safety settings for content generation.

    Returns:
        str: The generated text, or None if an error occurred.
    """
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        response = model.generate_content(prompt_text)
        
        # Check if the response has text and handle potential blocking
        if response.parts:
            return response.text
        elif response.prompt_feedback and response.prompt_feedback.block_reason:
            print(f"Prompt blocked. Reason: {response.prompt_feedback.block_reason}")
            if response.prompt_feedback.safety_ratings:
                 for rating in response.prompt_feedback.safety_ratings:
                    print(f"  Category: {rating.category}, Probability: {rating.probability}")
            return None
        else:
            # If no parts and no block reason, it might be an unexpected empty response
            print("Warning: Received an empty response from the API without a clear block reason.")
            return None

    except Exception as e:
        print(f"An error occurred during text generation: {e}")
        return None

def main():
    """Main function to demonstrate Beat poet text generation."""
    if not configure_gemini():
        return

    print("--- Generating Beat Poetry with Gemini API ---")

    for poet_name, prompt in POET_PROMPTS.items():
        print(f"\n--- Attempting to generate text in the style of: {poet_name} ---")
        print(f"Prompt:\n\"{prompt[:150]}...\"") # Print a snippet of the prompt

        generated_text = generate_text_with_gemini(prompt)

        if generated_text:
            print("\nGenerated Text:")
            print("-" * 20)
            print(generated_text)
            print("-" * 20)
        else:
            print(f"Could not generate text for {poet_name}.")
        print("\n" + "=" * 50 + "\n")

    # --- Example of using a custom prompt ---
    # print("\n--- Generating text with a custom prompt ---")
    # custom_prompt = (
    #     "Write a short, free-verse poem about a flickering neon sign "
    #     "in a lonely diner at 3 AM, evoking a sense of urban desolation "
    #     "and fleeting beauty, in a style reminiscent of a Beat poet."
    # )
    # print(f"Custom Prompt:\n\"{custom_prompt}\"")
    # custom_generated_text = generate_text_with_gemini(custom_prompt)
    # if custom_generated_text:
    #     print("\nGenerated Custom Text:")
    #     print("-" * 20)
    #     print(custom_generated_text)
    #     print("-" * 20)
    # else:
    #     print("Could not generate text for the custom prompt.")

if __name__ == "__main__":
    main()
