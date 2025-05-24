# 🧪 StoryLab: Interactive AI Storytelling

Embark on a unique storytelling adventure powered by cutting-edge AI! StoryLab is a Streamlit application that lets you create and guide interactive narratives with dynamic characters. Select your heroes, choose your genre, and make decisions that shape the unfolding story, brought to life by the powerful Qwen3-32B model running on the Cerebras Cloud.

## ✨ Features

*   **Interactive Narrative:** Experience a story that adapts and evolves based on your choices.
*   **Character Selection:** Choose from predefined characters or create your own to populate your world.
*   **Dynamic Characters:** Watch characters move between locations and interact with each other, driven by the AI.
*   **Player Choice:** Influence the story's direction by selecting from AI-generated options or typing your own actions.
*   **Character Status Tracking:** See where your characters are in the world via simple status cards.
*   **Thematic Styling:** Visual themes adapt to the genre of your story.
*   **Story Export:** Save your completed adventure as a text file.
*   **Function Calling:** The AI utilizes tool use (function calling) to manage character movement and dialogue, making the simulation more structured and engaging.

## 🧠 Under the Hood: Cerebras & Qwen3-32B

This application leverages the power of large language models to create a truly interactive experience.

*   **Powered by Cerebras:** We use the [Cerebras Cloud SDK](https://www.cerebras.net/cloud/) to access powerful AI models efficiently. Cerebras hardware is designed for large language models, providing the computational backbone for generating complex narratives and handling function calls.

*   **Featuring Qwen3:** The core intelligence behind StoryLab is the latest generation [Qwen3 model](https://qwenlm.github.io/blog/qwen3/). Qwen3 brings significant advancements that are particularly well-suited for this kind of interactive narrative:
    *   **Superior Human Preference Alignment:** Qwen3 excels at **creative writing, role-playing, and multi-turn dialogues**. This is crucial for StoryLab's ability to generate engaging narrative text, maintain character voices, and handle the back-and-forth of an interactive chat story.
    *   **Expertise in Agent Capabilities & Tool Integration:** Qwen3's strong performance in **integrating with external tools** is fundamental to StoryLab. The AI is instructed to use specific "functions" (`move_character`, `speak_to_character`) to represent in-world actions. Qwen3's agent capabilities make it adept at understanding *when* and *how* to call these functions based on the narrative context and user input, making character actions feel intentional and integrated.
    *   **Enhanced Reasoning:** Qwen3's improved reasoning capabilities help the AI maintain **plot coherence, character consistency, and logical progression** within the story world, even as characters move and interact.
    *   **Thinking/Non-thinking Modes:** Qwen3's unique modal switching likely contributes to its ability to handle both the complex logic of tool use ("thinking mode") and the fluid, creative generation of narrative text and dialogue ("non-thinking mode") within the same turn.
    *   **Multilingual Support:** While StoryLab currently focuses on English, Qwen3's support for **100+ languages** opens exciting possibilities for future localization or multilingual storytelling features.

By combining Streamlit's interactive UI capabilities with the advanced features of Qwen3 via the Cerebras Cloud, StoryLab provides a glimpse into the future of AI-powered interactive entertainment.

## 🚀 Getting Started

Follow these steps to get StoryLab up and running on your local machine.

### Prerequisites

*   Python 3.7+
*   A Cerebras Cloud API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd story_lab
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd story_lab
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    ```

4.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```

5.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Set your Cerebras API Key:**
    You can set your API key using environment variables or Streamlit Secrets.
    *   **Environment Variable (Temporary):**
        ```bash
        export CEREBRAS_API_KEY='your_api_key_here'
        ```
        (Replace `'your_api_key_here'` with your actual key)
    *   **Streamlit Secrets (Recommended for deployment):**
        Create a directory `.streamlit` in your project root (`storylab/`) if it doesn't exist. Inside `.streamlit`, create a file named `secrets.toml` and add:
        ```toml
        CEREBRAS_API_KEY="your_api_key_here"
        ```
        (Replace `"your_api_key_here"` with your actual key)

7.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

