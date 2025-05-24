import streamlit as st
from cerebras.cloud.sdk import Cerebras
import json
import re
from .helpers import update_character_status, extract_locations_from_text, parse_options

# --- Initialize Cerebras Client ---
@st.cache_resource
def get_cerebras_client(api_key):
    """Initializes and caches the Cerebras client."""
    if not api_key:
        st.error(
            "Cerebras API key not found. Please set the CEREBRAS_API_KEY environment variable or use Streamlit Secrets.")
        return None
    try:
        client = Cerebras(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Failed to initialize Cerebras client: {e}")
        return None

# --- Define Functions (Tools) ---
# These definitions are part of the core AI interaction logic
available_functions_def = [
    {
        "type": "function",
        "function": {
            "name": "move_character",
            "description": "Move a character to a specified location in the narrative world.",
            "parameters": {
                "type": "object",
                "properties": {
                    "character_name": {
                        "type": "string",
                        "description": "The name of the character to move.",
                    },
                    "location": {
                        "type": "string",
                        "description": "The destination location.",
                    },
                },
                "required": ["character_name", "location"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "speak_to_character",
            "description": "Have one character speak a message to another character.",
            "parameters": {
                "type": "object",
                "properties": {
                    "speaking_character": {
                        "type": "string",
                        "description": "The name of the character who is speaking.",
                    },
                    "target_character": {
                        "type": "string",
                        "description": "The name of the character being spoken to.",
                    },
                    "message": {
                        "type": "string",
                        "description": "The message to be delivered.",
                    },
                },
                "required": ["speaking_character", "target_character", "message"],
            },
        }
    },
]

# Mapping of function names to the actual Python functions
# These are simulation actions, not real-world actions
available_functions_map = {
    "move_character": lambda character_name, location: f"SIMULATION ACTION: {character_name} is moving to {location}.",
    "speak_to_character": lambda speaking_character, target_character, message: f"SIMULATION ACTION: {speaking_character} says to {target_character}: '{message}'",
}


# --- Core Narrative Step Function ---
def run_narrative_step(client, user_input_to_model: str, narrative_history: list,
                       available_functions: list, available_functions_map: dict):
    """
    Sends the conversation history and user input to the AI model,
    handles function calls, and returns the AI's response and updated history.
    """
    # Append the user message as a dictionary
    messages_for_api = narrative_history + [{"role": "user", "content": user_input_to_model}]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages_for_api,
            model="qwen-3-32b", # Use the model name directly or pass from config if preferred
            tools=available_functions,
            tool_choice="auto",
        )
    except Exception as e:
        st.error(f"An error occurred during API call: {e}")
        return "An error occurred while processing your request.", narrative_history

    response_message = chat_completion.choices[0].message

    # Handle function calls first
    if response_message.tool_calls:
        # Append the assistant message with tool_calls as a dictionary to history
        narrative_history.append({
            "role": response_message.role,
            "content": response_message.content, # Content might be empty if only a tool call
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                } for tc in response_message.tool_calls
            ]
        })

        # Assuming only one tool call for simplicity as in the original code
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        try:
            function_args = json.loads(tool_call.function.arguments)

            # Update character status based on function call using helper
            update_character_status(function_name, function_args)

        except json.JSONDecodeError:
            error_message = "Error processing function call arguments."
            st.error(error_message)
            return error_message, narrative_history
        except Exception as e:
            error_message = f"Error parsing function arguments for {function_name}: {e}"
            st.error(error_message)
            return error_message, narrative_history


        if function_name in available_functions_map:
            try:
                # Execute the function using the map
                function_to_call = available_functions_map[function_name]
                function_response_content = function_to_call(**function_args)

                # Add the tool response message to history
                narrative_history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response_content,
                    }
                )

                # Call the model again with the updated history including tool response
                second_response = client.chat.completions.create(
                    messages=narrative_history,
                    model="qwen-3-32b", # Use the model name
                    tools=available_functions, # Provide tools again just in case
                    tool_choice="auto", # Allow further tool calls if needed
                )
                full_response_content = second_response.choices[0].message.content
                # Add the second assistant response to history
                narrative_history.append({
                    "role": second_response.choices[0].message.role,
                    "content": full_response_content
                })

                # Try to extract location information from the *final* narrative text using helper
                extract_locations_from_text(full_response_content)

                return full_response_content, narrative_history

            except Exception as e:
                error_message = f"An error occurred while performing the action: {function_name}. Details: {e}"
                st.error(error_message)
                return error_message, narrative_history
        else:
            error_message = f"The AI tried to use an unknown action: {function_name}."
            st.error(error_message)
            return error_message, narrative_history
    else:
        # If no function call, just process the text response
        full_response_content = response_message.content
        narrative_history.append({
            "role": response_message.role,
            "content": full_response_content
        })

        # Try to extract location information from the narrative text using helper
        extract_locations_from_text(full_response_content)

        return full_response_content, narrative_history

