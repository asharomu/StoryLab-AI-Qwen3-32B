import streamlit as st
import uuid # For generating unique IDs
import re # Needed for re.sub in process_input

# Import modules from our organized structure
from config import API_KEY, MODEL_NAME, OPTIONS_SEPARATOR, GENRE_OPTIONS
from core.ai_interactions import get_cerebras_client, run_narrative_step, available_functions_def, available_functions_map
from core.helpers import parse_options, export_story
from ui.styling import apply_custom_css, apply_theme_colors
from ui.components import display_character_status
from ui.setup_view import show_character_selection

# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="AI Narrative Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Apply main custom CSS
apply_custom_css()

# --- Initialize Cerebras Client ---
client = get_cerebras_client(API_KEY)

if client is None:
    st.stop() # Stop the app if the client couldn't be initialized

# --- Function to process user input or option selection ---
def process_input(input_text: str, is_option_choice: bool = False):
    """Processes user input (text or option choice) and runs a narrative step."""
    st.session_state.processing = True

    # Add user message to chat history with unique ID
    message_id = str(uuid.uuid4())
    if is_option_choice:
        # Remove any leading emoji and whitespace for cleaner history display
        display_text = re.sub(r'^\s*[^\w\s]+\s*', '', input_text).strip()
        st.session_state.chat_messages.append({
            "id": message_id,
            "role": "user",
            "content": f"I choose: {display_text}",
            "turn": st.session_state.turn
        })
        # Craft the prompt for the model, asking for functions and options
        input_to_model = f"The user chooses this option: '{input_text}'. Describe the events that unfold as a result in the narrative. Actively use `move_character` and `speak_to_character` tools where appropriate to drive the action. Ensure at least one paragraph of detail, and then provide 3 new options following the '{OPTIONS_SEPARATOR}' separator. Each option should start with a relevant emoji that represents that choice. Remember to use simple, everyday language that both kids and adults can understand easily."
    else:
        st.session_state.chat_messages.append({
            "id": message_id,
            "role": "user",
            "content": input_text,
            "turn": st.session_state.turn
        })
        # Add instruction for functions, emojis in the options and language simplicity
        input_to_model = f"{input_text}\n\nDescribe the events that unfold. Actively use `move_character` and `speak_to_character` tools where appropriate to drive the action. Remember to provide 3 options after your response, each option should start with a relevant emoji that represents that choice. Use simple, everyday language that both kids and adults can understand easily."


    # Increment turn counter
    st.session_state.turn += 1

    # Run the narrative step using the core logic function
    full_response_text, updated_history = run_narrative_step(
        client=client, # Pass the client instance
        user_input_to_model=input_to_model,
        narrative_history=st.session_state.narrative_history,
        available_functions=available_functions_def,
        available_functions_map=available_functions_map
    )

    # Update the main narrative history in session state
    st.session_state.narrative_history = updated_history

    # Parse the full response for narrative and options using the helper function
    # Use the global OPTIONS_SEPARATOR
    narrative_part, _, current_options_list = parse_options(full_response_text, OPTIONS_SEPARATOR)

    # Add AI response to chat history for display with unique ID
    ai_message_id = str(uuid.uuid4())
    st.session_state.chat_messages.append({
        "id": ai_message_id,
        "role": "assistant",
        "content": narrative_part,
        "options": current_options_list,
        "turn": st.session_state.turn
    })

    # Update options list
    st.session_state.current_options = current_options_list
    st.session_state.processing = False


# --- Main Application Flow ---

st.markdown("<div class='chat-title'>🧪 StoryLab</div>", unsafe_allow_html=True)

# Check if we're in character selection or story mode
if 'story_started' not in st.session_state:
    st.session_state.story_started = False

# If we're in character selection mode, show the interface and exit
if not st.session_state.story_started:
    show_character_selection()
    st.stop() # Stop execution here - don't show the chat interface yet

# If we get here, we're in story mode - initialize if needed
if 'narrative_history' not in st.session_state:
    st.session_state.narrative_history = []

    # Get character names for the system prompt
    character_names = list(st.session_state.character_status.keys())
    character_descriptions = [
        f"'{name}' (a {st.session_state.character_status[name]['role']})" for name in character_names]
    character_list = ", ".join(character_descriptions)

    # Initialize with system message - UPDATED FOR MORE FUNCTION CALLING
    system_message_content = f"""You are the narrator and controller of the characters in this {st.session_state.theme.lower()} world. The main characters are {character_list}. Your primary role is to tell an engaging story based on user choices and actively manage the characters.

In this world, characters are dynamic! They frequently move between locations and talk to each other. **It is essential that you represent these actions using the provided tools.**

- **Whenever a character changes location**, use the `move_character` tool (e.g., if Elara goes to the market, call `move_character` with character_name='Elara', location='the Market').
- **Whenever one character speaks directly to another character**, use the `speak_to_character` tool (e.g., if Kael asks Elara a question, call `speak_to_character` with speaking_character='Kael', target_character='Elara', message='Are you ready?').

After describing the scene or events resulting from a tool call or user input, *always* provide at least one paragraph of narrative. Then, *always* provide exactly 3 distinct potential options for the user to choose from to continue the story, formatted after the '{OPTIONS_SEPARATOR}' separator. Each option should start with a relevant emoji that represents that choice.

Remember to use simple, everyday language suitable for readers ages 8 and up. Keep sentences short and words common.
"""
    st.session_state.narrative_history.append({"role": "system", "content": system_message_content})

    # Initialize chat messages for display (separate from narrative history used for the AI)
    st.session_state.chat_messages = []

    # Initialize turn counter and processing flag
    st.session_state.turn = 0
    st.session_state.processing = True
    st.session_state.current_options = []

    # Create a comma-separated list of character names
    character_names_list = ", ".join(character_names)

    # Generate initial scene - with emoji instructions and simple language
    # Also slightly rephrased to encourage immediate action/interaction
    initial_scene_prompt_to_model = f"Describe the starting scene with {character_names_list}. Have them begin interacting or moving right away. Ensure at least one paragraph of detail, and then provide the first 3 options following the '{OPTIONS_SEPARATOR}' separator. Each option should start with a relevant emoji that represents that choice. Use simple, everyday language that both kids and adults can understand easily."


    # Generate initial scene using the core logic function
    full_initial_response_content, updated_history_after_initial = run_narrative_step(
        client=client, # Pass the client instance
        user_input_to_model=initial_scene_prompt_to_model,
        narrative_history=st.session_state.narrative_history,
        available_functions=available_functions_def,
        available_functions_map=available_functions_map
    )
    st.session_state.narrative_history = updated_history_after_initial

    # Parse initial response using the helper function
    # Use the global OPTIONS_SEPARATOR
    narrative_part, _, initial_options_list = parse_options(full_initial_response_content, OPTIONS_SEPARATOR)

    # Add to chat messages for display with unique ID
    initial_message_id = str(uuid.uuid4())
    st.session_state.chat_messages.append({
        "id": initial_message_id,
        "role": "assistant",
        "content": narrative_part,
        "options": initial_options_list,
        "turn": 0
    })
    st.session_state.current_options = initial_options_list
    st.session_state.processing = False

# Apply theme colors based on the selected theme in session state
if 'theme' in st.session_state:
    apply_theme_colors(st.session_state.theme)
else:
    # Fallback to default theme if somehow not set (shouldn't happen if setup runs)
    apply_theme_colors(GENRE_OPTIONS[0])


# --- Sidebar with Theme Selection and Timeline ---
with st.sidebar:
    st.title("Story Settings")

    # Theme selection (uses ui/styling)
    st.markdown("### 🎨 Theme Selection")
    # Find the current theme's index, default to 0 if not found
    current_theme_index = GENRE_OPTIONS.index(st.session_state.theme) if 'theme' in st.session_state and st.session_state.theme in GENRE_OPTIONS else 0
    selected_theme = st.selectbox(
        "Choose a visual theme",
        ["Fantasy", "Sci-Fi", "Horror", "Mystery", "Medieval", "Western"], # Ensure all genres are options here
        key="theme_selector",
        index=current_theme_index
    )

    # Story timeline
    st.markdown("### 📜 Story Timeline")
    if st.session_state.chat_messages:
        # Display messages in reverse order to show latest at the top of the timeline
        for msg in reversed(st.session_state.chat_messages):
            if msg["role"] == "assistant":
                turn = msg.get("turn", 0)
                # Truncate the content for display
                short_content = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-turn">Turn {turn}</div>
                    <div class="timeline-content">{short_content}</div>
                </div>
                """, unsafe_allow_html=True)


    # Export story button (uses core/helpers)
    st.markdown("### 📝 Export Your Story")
    story_text = export_story(st.session_state.chat_messages) # Pass chat messages to the helper
    st.download_button(
        label="Download Story Text",
        data=story_text,
        file_name="my_adventure.txt",
        mime="text/plain",
        key="download_story"
    )

    # Restart button (resets session state)
    st.markdown("### 🔄 Reset Adventure")
    if st.button("New Story with New Characters", key="restart_btn"):
        # Clear all keys from session state to reset the app
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun() # Rerun to start from the character selection screen

# --- Display Character Status Cards ---
display_character_status() # Uses ui/components

# --- Main Chat Interface ---

# Chat Display
chat_container = st.container()
with chat_container:
    # Display messages in order
    for idx, message in enumerate(st.session_state.chat_messages):
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            # Display AI message with typing effect for the latest message
            if idx == len(st.session_state.chat_messages) - 1 and message["role"] == "assistant" and not st.session_state.processing:
                 # Only apply typing effect if it's the last message and not currently processing
                 st.markdown(f"<div class='ai-message'><span class='typing-effect'>{message['content']}</span></div>", unsafe_allow_html=True)
            else:
                 # Regular display for older messages or while processing
                 st.markdown(f"<div class='ai-message'>{message['content']}</div>", unsafe_allow_html=True)


            # Display options if present (only for the last message and if not processing)
            if "options" in message and message["options"] and idx == len(st.session_state.chat_messages) - 1 and not st.session_state.processing:
                st.markdown("<div class='options-container'>", unsafe_allow_html=True)
                st.markdown("<div class='turn-indicator'>Choose your next action:</div>", unsafe_allow_html=True)

                # Use columns for options if there are multiple (max 3 columns)
                num_options = len(message["options"])
                cols = st.columns(min(num_options, 3)) # Limit to 3 columns for better layout

                for i, option in enumerate(message["options"]):
                    # Ensure the option text (including emoji) is used for the button label
                    button_label = option.strip()
                    with cols[i % len(cols)]: # Cycle through the columns
                        # Use a unique key combining message ID and option index
                        unique_key = f"option_{message['id']}_{i}"
                        # Disable buttons if processing is ongoing
                        if st.button(button_label, key=unique_key, disabled=st.session_state.processing, use_container_width=True):
                            process_input(option, is_option_choice=True)
                            st.rerun() # Trigger a rerun to update the UI


                st.markdown("</div>", unsafe_allow_html=True)

# --- Loading indicator (only shown when processing) ---
if st.session_state.processing:
    # Use a placeholder to keep the input area visible while loading
    with st.container(): # Or use a specific area if needed
         st.markdown("<div class='loading-dots'>Thinking...</div>", unsafe_allow_html=True)
    # Disable input while processing
    disable_input = True
else:
    disable_input = False


# --- Chat Input ---
# Place input form at the bottom
with st.form(key="chat_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your own action:",
                               placeholder="Enter your own action or response...",
                               key="chat_input",
                               disabled=disable_input) # Disable input while processing

    # Hidden submit button (users can press Enter)
    # Make the submit button also disabled while processing
    submitted = st.form_submit_button("Send", type="primary", disabled=disable_input)

    if submitted and user_input and not st.session_state.processing:
        process_input(user_input, is_option_choice=False)
        st.rerun() # Trigger a rerun to update the UI
