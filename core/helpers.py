import streamlit as st
import re # Needed for parsing text
import json # Needed for function args

# --- Helper Functions ---

# Function to update character status based on function calls
def update_character_status(tool_call_name=None, function_args=None):
    """Updates character status in session state based on tool call arguments."""
    if 'character_status' not in st.session_state:
        st.session_state.character_status = {}

    # Update based on tool calls
    if tool_call_name and function_args:
        if tool_call_name == "move_character":
            character = function_args.get("character_name")
            location = function_args.get("location")
            if character and location:
                 # Find the character case-insensitively if necessary, or rely on model to match name exactly
                 found_char_name = None
                 for char_name in st.session_state.character_status.keys():
                     if char_name.lower() == character.lower():
                         found_char_name = char_name
                         break

                 if found_char_name:
                    st.session_state.character_status[found_char_name]["location"] = location
                    # Optional: Add a log message
                    # st.sidebar.write(f"🚗 Updated {found_char_name}'s location to {location}")
                 else:
                     # Optional: Log if character not found
                     st.sidebar.warning(f"AI tried to move unknown character: {character}")


# Function to extract locations from narrative text using simple heuristics
def extract_locations_from_text(text):
    """Attempts to extract location changes from narrative text and update character status."""
    if 'character_status' not in st.session_state:
        return # Don't display if no characters are set up

    # Get list of characters to track
    characters = list(st.session_state.character_status.keys())

    # Simple pattern matching for location changes
    # This regex is basic and might need refinement for complex narratives
    # Looks for patterns like "Character moved to Location" or "Character entered Location"
    # It tries to capture the character name and the location name.
    # It handles optional "the " before the location.
    # It assumes character names are reasonably simple words/phrases.
    # It will match the *first* character name found in the pattern in the text.
    location_patterns = [
        r"([A-Za-z ]+) (?:moved|went|traveled|journeyed|walked) to (?:the )?([A-Za-z0-9 ]+)",
        r"([A-Za-z ]+) (?:entered|arrived at|reached) (?:the )?([A-Za-z0-9 ]+)"
        # Add more patterns as needed
    ]

    for pattern in location_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            char_candidate = match.group(1).strip()
            location = match.group(2).strip()

            # Check if the matched character candidate is one of our known characters
            found_char_name = None
            for char_name in characters:
                # Use a simple check if the candidate name is very close or matches a word in the character name
                if char_name.lower() in char_candidate.lower() or char_candidate.lower() in char_name.lower():
                     found_char_name = char_name
                     break # Found a match, use this one

            if found_char_name and location and len(location) > 2: # Avoid very short or empty locations
                # Update the location for the found character
                st.session_state.character_status[found_char_name]["location"] = location
                # Optional: Add a log message
                # st.sidebar.write(f"🗺️ Extracted {found_char_name}'s location as {location}")
                # If we find one update, we can potentially stop for this text chunk,
                # or continue to find more if multiple characters move.
                # Let's continue in case multiple characters are mentioned moving.


# Function to parse options from response text
def parse_options(response_text: str, separator: str):
    """Parses narrative text and options based on a separator."""
    options_string = ""
    options_list = []
    narrative_part = response_text

    if separator in response_text:
        parts = response_text.split(separator, 1)
        narrative_part = parts[0].strip()
        if len(parts) > 1:
            options_string = parts[1].strip()
            # Parse options_string into a list
            option_lines = options_string.split('\n')
            for line in option_lines:
                line = line.strip()
                if not line: # Skip empty lines
                    continue
                # Revised regex: Match the start (optional whitespace, number, dot, whitespace)
                # and capture everything *after* that.
                # The previous regex `[^\w\s]*\s*` was inside the capture group, which was wrong.
                # Let's match the prefix and take the rest of the string.
                match = re.match(r'^\s*\d+\.\s*', line)
                if match:
                    # If it's a numbered list item, take the text after the number and dot
                    option_text = line[match.end():].strip()
                    if option_text: # Ensure option text is not empty after stripping
                        options_list.append(option_text)
                elif line:
                     # If it's not a numbered list item but is not empty, add the whole line as a fallback
                     # This might include lines that are just emojis or other unexpected formats
                     options_list.append(line)


    return narrative_part, options_string, options_list # Return all three for potential debugging

# Function to export story as text
def export_story(chat_messages: list):
    """Formats the chat history into a readable story text."""
    story_text = "# My Interactive Adventure\n\n"

    for msg in chat_messages:
        if msg["role"] == "assistant":
            story_text += f"{msg['content']}\n\n"
        elif msg["role"] == "user":
            # Clean up the "I choose: " prefix for the export
            user_content = msg['content']
            if user_content.startswith("I choose: "):
                 user_content = user_content[len("I choose: "):]
            story_text += f"*[I chose: {user_content}]*\n\n"

    return story_text
