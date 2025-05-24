import streamlit as st

# --- Display Character Status ---
def display_character_status():
    """Displays character status cards in the main area."""
    if 'character_status' not in st.session_state or not st.session_state.character_status:
        return # Don't display if no characters are set up

    st.subheader("🧙‍♂️ Character Status")

    # Calculate number of columns based on character count
    num_characters = len(st.session_state.character_status)
    # Use st.columns directly, it returns a list of column objects
    cols = st.columns(min(num_characters, 3)) # Max 3 columns per row

    # Display each character in a column
    for i, (char_name, char_info) in enumerate(st.session_state.character_status.items()):
        col_index = i % len(cols) # Ensure index stays within the number of columns created
        with cols[col_index]:
            st.markdown(f"""
            <div class="character-card">
                <div class="character-name">{char_name}</div>
                <div class="character-role">{char_info["role"]}</div>
                <div class="character-location">📍 {char_info["location"]}</div>
            </div>
            """, unsafe_allow_html=True)
