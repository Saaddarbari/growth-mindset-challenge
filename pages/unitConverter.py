import streamlit as st

# CSS for styling elements
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
        .stSelectbox label, .stNumberInput label {
            display:none;
        }
        .stButton>button {
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: rgb(37, 24, 219);
            color: white;
        }
        .result-box {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            color: #333;
            margin-top: 10px;
        }
    </style>
    <h1 class="responsive-title">🚀 Unit Converter</h1>
    """,
    unsafe_allow_html=True
)

# Sidebar message
st.sidebar.success("🌟 Be Silent And Let Your Success Shout")

# Unit conversion categories and units
categories = {
    "Length": ["Millimetre", "Centimetre", "Metre", "Kilometre", "Inch", "Foot", "Yard", "Mile"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Fuel Economy": ["Kilometre per liter", "Litre per 100 Kilometres"],
    "Digital Storage": ["Bit", "Byte", "Kilobit", "Kilobyte", "Megabit", "Megabyte", "Gigabit", "Gigabyte", "Terabit", "Terabyte"],
}

# Conversion factors
conversion_factors = {
    "Length": {
        "Millimetre": 0.001, "Centimetre": 0.01, "Metre": 1, "Kilometre": 1000,
        "Inch": 0.0254, "Foot": 0.3048, "Yard": 0.9144, "Mile": 1609.34
    },
    "Digital Storage": {
        "Bit": 1, "Byte": 8, "Kilobit": 1000, "Kilobyte": 8000,
        "Megabit": 1_000_000, "Megabyte": 8_000_000, "Gigabit": 1_000_000_000,
        "Gigabyte": 8_000_000_000, "Terabit": 1_000_000_000_000, "Terabyte": 8_000_000_000_000
    }
}

# Sidebar: Category selection
category = st.selectbox("Select Conversion Category:", list(categories.keys()))

# Dynamic unit options based on selected category
units = categories[category]

# Input: Value to convert
value_from = st.number_input(f"Enter Value in {units[0]}:", min_value=0.0, value=1.0, step=0.1, format="%.2f")

col1, col2, col3 = st.columns([3, 1, 3])
with col1:
    from_unit = st.selectbox("Select From Unit:", units)

# Equal sign
with col2:
    st.markdown("<h1 style='text-align:center'>=</h1>", unsafe_allow_html=True)

# To Unit selection
with col3:
    to_unit = st.selectbox("Select To Unit:", units)


def convert(value, from_unit, to_unit, category):
    """Function to perform unit conversion."""
    # Handle Temperature Separately (Uses Formulas Instead of Multiplication)
    if category == "Temperature":
        if from_unit == to_unit:
            return value  # No conversion needed
        
        if from_unit == "Celsius":
            return (value * 9/5) + 32 if to_unit == "Fahrenheit" else value + 273.15
        elif from_unit == "Fahrenheit":
            return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32

    # Special Case for Fuel Economy (Inverse Relation)
    if category == "Fuel Economy":
        if from_unit == "Litre per 100 Kilometres" and to_unit == "Kilometre per liter":
            return 100 / value
        elif from_unit == "Kilometre per liter" and to_unit == "Litre per 100 Kilometres":
            return 100 / value

    # Standard Multiplication-Based Conversion
    if category in conversion_factors:
        from_factor = conversion_factors[category].get(from_unit)
        to_factor = conversion_factors[category].get(to_unit)

        if from_factor is None or to_factor is None:
            return "Invalid conversion"

        return (value * from_factor) / to_factor


# Conversion button and result display
if st.button("Convert"):
    result = convert(value_from, from_unit, to_unit, category)

    if result is not None:
        try:
            result = float(result)  # Ensure it's a valid number
            st.markdown(
                f'<div class="result-box">{value_from:.2f} {from_unit} is equal to {result:.2f} {to_unit}</div>',
                unsafe_allow_html=True
            )
        except ValueError:
            st.error("Conversion failed. Please check your input values.")
    else:
        st.error("Invalid conversion. Please check your units.")
st.markdown(
    f'<div class="result-box">Devoloped by Saad Darbari</div>',
    unsafe_allow_html=True
)