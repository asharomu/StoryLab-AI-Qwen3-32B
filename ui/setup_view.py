import streamlit as st

# Import data and config needed for setup
from data import get_character_recommendations
from config import GENRE_OPTIONS

# --- Character Selection Interface ---
def show_character_selection():
    """Displays the interface for selecting and customizing characters before starting the story."""
    st.markdown("<div class='setup-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='setup-header'>Choose Your Characters</h2>", unsafe_allow_html=True)

    # Theme selection for setting the initial story genre
    selected_genre = st.selectbox("Select a genre for your story", GENRE_OPTIONS, key="setup_genre_select")

    # Convert genre to lowercase for dictionary lookup
    genre_key = selected_genre.lower().replace("-", "_") # Handle hyphens like Sci-Fi -> sci_fi

    # Get character recommendations for this genre
    all_recommendations = get_character_recommendations()
    # Use .get with a default fallback (e.g., fantasy) in case a genre key doesn't match recommendations
    recommendations = all_recommendations.get(genre_key, all_recommendations.get("fantasy", [])) # Fallback to empty list if even fantasy is missing

    # Initialize characters in session state if not present or if genre changes?
    # Let's keep selected_characters persistent until the user explicitly restarts or starts the story.
    if 'selected_characters' not in st.session_state:
        st.session_state.selected_characters = []
        # Pre-select the default characters from the initial genre selection
        if recommendations:
             # Select first two by default if available
             for char in recommendations[:2]:
                st.session_state.selected_characters.append({
                    "name": char["name"],
                    "role": char["role"],
                    "location": "Starting Location" # Default starting location
                })
        # Store the initially selected genre to manage recommendations on rerun
        st.session_state.setup_genre = selected_genre
        st.rerun() # Rerun to show selected characters

    # If the genre selectbox changes, add logic here if you want it to reset selections
    # if st.session_state.setup_genre != selected_genre:
    #      st.session_state.selected_characters = []
    #      st.session_state.setup_genre = selected_genre
    #      st.rerun()


    # Display character recommendations
    st.subheader("Recommended Characters")

    # Create columns for character recommendations (max 2 per row for cards)
    rec_cols = st.columns(2)

    for i, char in enumerate(recommendations):
        with rec_cols[i % 2]:
            # Check if this character is already selected
            is_selected = any(c["name"] == char["name"] for c in st.session_state.selected_characters)

            # Create the card class with selected status
            card_class = "char-recommendation selected" if is_selected else "char-recommendation"

            # Use a unique key for the card markdown itself if needed, but button keys are sufficient for actions
            st.markdown(f"""
            <div class='{card_class}'>
                <div class='char-rec-name'>{char["name"]}</div>
                <div class='char-rec-role'>{char["role"]}</div>
                <div class='char-rec-desc'>{char["description"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Add/Remove buttons below the card
            button_key = f"rec_action_{char['name'].replace(' ', '_')}_{i}" # Ensure unique key
            if is_selected:
                # Ensure we don't remove if only 2 characters are left among selected
                if len(st.session_state.selected_characters) > 2:
                    if st.button(f"Remove {char['name']}", key=button_key):
                        # Remove character from selected list by name
                        st.session_state.selected_characters = [c for c in st.session_state.selected_characters if c["name"] != char["name"]]
                        st.rerun()
                else:
                     st.button(f"Remove {char['name']}", key=button_key, disabled=True, help="You need at least two characters.")

            else:
                if st.button(f"Add {char['name']}", key=button_key):
                    # Add character to selected list if not already added (double check)
                    if not any(c["name"] == char["name"] for c in st.session_state.selected_characters):
                         st.session_state.selected_characters.append({
                            "name": char["name"],
                            "role": char["role"],
                            "location": "Starting Location"
                         })
                         st.rerun()


    # --- Custom character creation (now in a form) ---
    st.subheader("Create Custom Character")

    # Start the form
    with st.form(key="custom_character_form", clear_on_submit=True): # clear_on_submit=True handles clearing inputs

        col1, col2 = st.columns(2)
        with col1:
            # Inputs inside the form
            custom_name = st.text_input("Character Name", key="custom_name_input_form") # Use unique key within form
        with col2:
            # Inputs inside the form
            custom_role = st.text_input("Character Role", key="custom_role_input_form") # Use unique key within form

        # The button to submit the form
        submitted = st.form_submit_button("Add Custom Character")

        # Logic that runs *after* the form is submitted
        if submitted:
            if custom_name and custom_role:
                # Add custom character to selected list
                st.session_state.selected_characters.append({
                    "name": custom_name,
                    "role": custom_role,
                    "location": "Starting Location"
                })
                # No need to manually clear inputs here, clear_on_submit=True does it
                st.rerun() # Rerun to update the displayed list of selected characters
            else:
                 st.warning("Please enter both a name and a role for the custom character.")

    # --- End of Custom character creation form ---


    # Display currently selected characters for editing/review
    st.subheader("Your Selected Characters")

    if not st.session_state.selected_characters:
        st.info("No characters selected yet. Please add at least two characters.")
    else:
        # Display each selected character with edit options
        for i, char in enumerate(st.session_state.selected_characters):
            # Use unique keys for expander and inputs
            expander_key = f"char_edit_expander_{i}"
            # Keys for inputs *outside* the form need to be unique per item
            name_input_key = f"edit_name_input_{i}"
            role_input_key = f"edit_role_input_{i}"
            update_button_key = f"update_char_button_{i}"
            remove_button_key = f"remove_selected_char_button_{i}"

            # No 'key' argument for st.expander as per previous fix
            with st.expander(f"{char['name']} - {char['role']}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    # Make inputs stateful
                    new_name = st.text_input("Name", value=char["name"], key=name_input_key)
                with col2:
                    # Make inputs stateful
                    new_role = st.text_input("Role", value=char["role"], key=role_input_key)

                # Update button
                if st.button("Update Character Details", key=update_button_key): # Unique key
                    st.session_state.selected_characters[i]["name"] = new_name
                    st.session_state.selected_characters[i]["role"] = new_role
                    st.rerun() # Rerun to reflect changes

                # Remove button
                # Ensure at least 2 characters remain after removal
                if len(st.session_state.selected_characters) > 2:
                    if st.button("Remove Character", key=remove_button_key): # Unique key
                        st.session_state.selected_characters.pop(i)
                        st.rerun() # Rerun to update the list
                else:
                     st.button("Remove Character", key=remove_button_key, disabled=True, help="You need at least two characters to start.")


    # Button to start the adventure
    if len(st.session_state.selected_characters) >= 2:
        if st.button("Start Your Adventure", key="start_adventure_button", use_container_width=True): # Unique key
            # Convert selected characters to character status format
            st.session_state.character_status = {}
            for char in st.session_state.selected_characters:
                st.session_state.character_status[char["name"]] = {
                    "role": char["role"],
                    "location": char["location"] # Use the default starting location
                }

            # Set story started flag
            st.session_state.story_started = True

            # Set theme based on the genre selected at the top of the setup page
            st.session_state.theme = selected_genre

            # Clear selected_characters from state if you don't want them persisting after start
            # del st.session_state.selected_characters

            st.rerun() # Rerun to switch to the main chat interface
    else:
        st.warning("Please select at least two characters to begin your adventure.")

    st.markdown("</div>", unsafe_allow_html=True)
