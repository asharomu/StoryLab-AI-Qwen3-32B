import streamlit as st

# --- Page Styling (CSS) ---
def apply_custom_css():
    """Applies the main custom CSS for the application."""
    st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background-color: #f9f9f9;
        }

        .chat-title {
        text-align: center;
        margin-bottom: 20px;
        color: #333;
        font-size: 60px;
        font-weight: bold;
        }

        /* Chat container */
        .chat-container {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            max-height: 70vh;
            overflow-y: auto;
        }

        /* AI message styling */
        .ai-message {
            background-color: #f0f7ff;
            padding: 15px;
            border-radius: 15px 15px 15px 0px;
            margin: 10px 0;
            border-left: 3px solid #4361ee; /* Default theme color */
            font-size: 16px;
            line-height: 1.5;
            max-width: 85%;
            word-wrap: break-word; /* Ensure long words wrap */
        }

        /* User message styling */
        .user-message {
            background-color: #e9f7ef;
            padding: 15px;
            border-radius: 15px 15px 0px 15px;
            margin: 10px 0 10px auto;
            border-right: 3px solid #27ae60;
            font-size: 16px;
            line-height: 1.5;
            max-width: 85%;
            text-align: right;
            word-wrap: break-word; /* Ensure long words wrap */
        }

        /* Option button styling */
        .chat-option-button {
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 20px;
            padding: 8px 15px;
            margin: 5px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
            display: inline-block;
        }

        .chat-option-button:hover {
            background-color: #e9ecef;
            transform: translateY(-2px);
        }

        /* Styling for the options container */
        .options-container {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
            background-color: #f8f9fa;
            border-left: 3px solid #6c757d; /* Default */
        }

        /* Chat input styling */
        .chat-input {
            border-radius: 20px;
            border: 1px solid #ddd;
            padding: 10px 15px;
        }

        /* Turn indicator */
        .turn-indicator {
            color: #6c757d;
            font-size: 12px;
            text-align: center;
            margin: 5px 0;
        }

        /* Loading indicator */
        .loading-dots {
            text-align: center;
            color: #6c757d;
            font-size: 24px;
            margin: 10px 0;
        }

        /* Restart button */
        /* Note: This style might be overridden by Streamlit's default button style */
        .restart-button {
            background-color: #f8d7da;
            color: #721c24;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            float: right;
            margin: 10px;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }

        /* Character status cards */
        .character-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
            text-align: center;
            transition: all 0.3s;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .character-card:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }

        .character-name {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 5px;
        }

        .character-role {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }

        .character-location {
            font-size: 14px;
            color: #333;
            margin-top: 5px;
        }

        /* Timeline item styling */
        .timeline-item {
            padding: 10px;
            border-left: 2px solid #4361ee; /* Default theme color */
            margin-bottom: 10px;
            background-color: #f8f9fa;
            border-radius: 0 5px 5px 0;
        }

        .timeline-turn {
            font-weight: bold;
            color: #4361ee; /* Default theme color */
        }

        .timeline-content {
            font-size: 14px;
            color: #333;
        }

        /* Typing animation for AI messages */
        .typing-effect {
            display: inline-block;
            white-space: normal;
            overflow: hidden;
            border-right: 2px solid #333; /* Blinking caret */
            animation: typing 2s steps(40, end), blink-caret 0.75s step-end infinite;
            /* Animation re-enabled */
        }

        /* Re-enable keyframes */
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }

        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: #333 }
        }


        /* Export button styling */
        /* Note: This style might be overridden by Streamlit's default button style */
        .export-button {
            background-color: #4361ee; /* Default theme color */
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            display: block;
            margin: 10px auto;
        }

        .export-button:hover {
            background-color: #3651d4; /* Default darker theme color */
            transform: scale(1.05);
        }

        /* Character recommendation cards */
        .char-recommendation {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #fff;
            transition: all 0.2s;
        }

        .char-recommendation:hover {
            border-color: #4361ee; /* Default theme color */
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .char-recommendation.selected {
            border-color: #4361ee; /* Default theme color */
            background-color: #f0f7ff;
            box-shadow: 0 4乎px 8px rgba(0,0,0,0.1);
        }

        .char-rec-name {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 5px;
        }

        .char-rec-role {
            font-style: italic;
            color: #666;
            margin-bottom: 5px;
        }

        .char-rec-desc {
            font-size: 14px;
            color: #333;
        }

        /* Setup container styling */
        .setup-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .setup-header {
            text-align: center;
            margin-bottom: 20px;
            color: #333;
        }

        .character-edit {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }

        /* Start button styling */
        /* Note: This style might be overridden by Streamlit's default button style */
        .start-button {
            background-color: #4361ee; /* Default theme color */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin-top: 20px;
        }

        .start-button:hover {
            background-color: #3651d4; /* Default darker theme color */
            transform: scale(1.02);
        }

        /* Option emoji styling */
        /* Not directly used in CSS, but good to keep in mind for button content */
        .option-emoji {
            font-size: 1.2em;
            margin-right: 8px;
        }
    </style>
    """, unsafe_allow_html=True)


# --- Apply Theme Colors ---
def apply_theme_colors(theme):
    """Applies theme-specific colors via CSS."""
    if theme == "Fantasy":
        primary_color = "#4361ee" # Blue
        secondary_color = "#3f8efc"
        ai_bg_color = "#f0f7ff" # Light Blue
        user_bg_color = "#e9f7ef" # Light Green
        user_border_color = "#27ae60" # Green
        options_border_color = "#6c757d" # Gray
    elif theme == "Sci-Fi":
        primary_color = "#2ec4b6" # Teal
        secondary_color = "#20a4f3" # Lighter Blue
        ai_bg_color = "#e0f7fa" # Light Cyan
        user_bg_color = "#e9f7ef" # Light Green (reused)
        user_border_color = "#27ae60" # Green (reused)
        options_border_color = "#6c757d" # Gray (reused)
    elif theme == "Horror":
        primary_color = "#800020" # Dark Red/Maroon
        secondary_color = "#420516" # Even Darker Red
        ai_bg_color = "#fff0f0" # Very Light Red
        user_bg_color = "#f0e0d0" # Light Brown
        user_border_color = "#a0522d" # Sienna
        options_border_color = "#333333" # Dark Gray
    elif theme == "Mystery":
        primary_color = "#5f0f40" # Dark Purple
        secondary_color = "#9a031e" # Burgundy
        ai_bg_color = "#f8f0ff" # Very Light Purple
        user_bg_color = "#f0f0f0" # Light Gray
        user_border_color = "#606060" # Medium Gray
        options_border_color = "#404040" # Darker Gray
    elif theme == "Medieval":
        primary_color = "#8b4513" # SaddleBrown
        secondary_color = "#a0522d" # Sienna
        ai_bg_color = "#f5f5dc" # Beige
        user_bg_color = "#f0e68c" # Khaki
        user_border_color = "#b8860b" # DarkGoldenRod
        options_border_color = "#708090" # SlateGray
    elif theme == "Western":
        primary_color = "#d2691e" # Chocolate
        secondary_color = "#b0c4de" # LightSteelBlue
        ai_bg_color = "#fff8dc" # Cornsilk
        user_bg_color = "#f5deb3" # Wheat
        user_border_color = "#8b4513" # SaddleBrown
        options_border_color = "#a9a9a9" # DarkGray
    else: # Default or fallback
        primary_color = "#4361ee"
        secondary_color = "#3f8efc"
        ai_bg_color = "#f0f7ff"
        user_bg_color = "#e9f7ef"
        user_border_color = "#27ae60"
        options_border_color = "#6c757d"


    # Apply theme colors via CSS override
    st.markdown(f"""
    <style>
        .ai-message {{
            border-left-color: {primary_color};
            background-color: {ai_bg_color};
        }}
        .user-message {{
            border-right-color: {user_border_color};
            background-color: {user_bg_color};
        }}
        .options-container {{
            border-left-color: {options_border_color};
        }}
        /* Target Streamlit buttons */
        .stButton button {{
            background-color: {primary_color};
            color: white;
            border: none; /* Override default border */
        }}
        .stButton button:hover {{
            background-color: {secondary_color};
            color: white; /* Ensure text stays white on hover */
        }}
        /* Specific overrides for elements using theme colors */
        .character-card {{
            border-color: {primary_color};
        }}
        .character-name {{
            color: {primary_color};
        }}
        .timeline-item {{
            border-left-color: {primary_color};
        }}
        .timeline-turn {{
            color: {primary_color};
        }}
        /* Note: .export-button and .start-button might need !important if not overriding */
        .export-button, .stDownloadButton button {{
            background-color: {primary_color} !important;
            color: white !important;
        }}
        .export-button:hover, .stDownloadButton button:hover {{
            background-color: {secondary_color} !important;
        }}
        .start-button, .stFormSubmitButton button[kind="primary"] {{
             background-color: {primary_color} !important;
            color: white !important;
        }}
         .start-button:hover, .stFormSubmitButton button[kind="primary"]:hover {{
            background-color: {secondary_color} !important;
        }}
        .char-recommendation.selected {{
            border-color: {primary_color};
            /* background-color: #f0f7ff; /* Keep light blue or make theme-based */
        }}
        .char-recommendation:hover {{
            border-color: {primary_color};
        }}
    </style>
    """, unsafe_allow_html=True)
