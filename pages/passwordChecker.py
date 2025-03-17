import streamlit as st
import re

# Page configuration
st.set_page_config(page_title="Password Strength Meter", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .responsive-title {
            text-align: center;
            font-size:50px !important;
        }
        @media (max-width: 600px) {
            .responsive-title {
                font-size:30px !important;
            }
        }
    </style>
    <h1 class="responsive-title">🚀 Password Strength Meter</h1>
    """,
    unsafe_allow_html=True
)

# Sidebar message
st.sidebar.success("🌟 Be Silent And Let Your Success Shout")

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", "green", feedback
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", "orange", feedback
    else:
        return "❌ Weak Password - Improve it using the suggestions above.", "red", feedback

# User input
password = st.text_input("Enter your password:", type="password")
if password:
    strength, color, suggestions = check_password_strength(password)
    
    # Display strength
    st.markdown(f"<h3 style='color: {color};'>{strength}</h3>", unsafe_allow_html=True)
    
    # Show suggestions
    if suggestions:
        for suggestion in suggestions:
            st.write(suggestion)
