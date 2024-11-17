import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Julegaveønskeseddel Skattejagt", page_icon="🎄")

# [Previous CSS styles remain unchanged]
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to bottom, #1e4258, #0e2a3f);
        color: #ffffff;
    }
    .horizontal-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        gap: 10px;
        margin: 20px 0;
        max-width: 1200px;
    }
    .number-input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
    }
    .number-input-container label {
        font-size: 0.9em;
        color: #ffffff;
    }
    .number-input {
        width: 60px !important;
        text-align: center;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stHorizontalBlock"] {
        gap: 10px;
    }
    .story-container, .challenge-container {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .success-message {
        background-color: rgba(0, 255, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .error-message {
        background-color: rgba(255, 0, 0, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        text-align: center;
        animation: shake 0.5s;
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    .wishlist {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .challenge-steps {
        margin: 10px 0;
    }
    .challenge-steps ol {
        margin-left: 20px;
        padding-left: 0;
    }
    .challenge-steps li {
        margin-bottom: 10px;
        line-height: 1.5;
    }
    .stDownloadButton {
        background-color: rgba(255, 255, 255, 0);
        color: #29292b !important;
        border-color: #ff9800 !important;
    }
    .stDownloadButton:hover {
        border-color: #f57c00 !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'solved' not in st.session_state:
    st.session_state.solved = False
if 'show_error' not in st.session_state:
    st.session_state.show_error = False

# Helper functions
def check_middelfart_sequence(inputs):
    correct_sequence = [17, 18, 19, 21, 14, 8, 10, 12, 13]  # len 9
    return all(int(inp) == correct for inp, correct in zip(inputs, correct_sequence))

def check_aarhus_sequence(inputs):
    correct_sequence = [9, 4, 12, 6, 8, 11, 3, 5, 7, 10, 2]  # len 11
    return all(int(inp) == correct for inp, correct in zip(inputs, correct_sequence))

# Title is always shown
st.markdown("# 🎄 Den Magiske Julegaveønskeseddel Skattejagt 🎅")

if not st.session_state.solved:
    # Show introduction and instructions only when puzzle is not solved
    st.markdown("""
    <div class="story-container">
        <h2>🧝‍♂️ Historien om den Drillesyge Nisse</h2>
        <p>Kære Familie,</p>
        <p>Noget magisk (og lidt drillende) er sket! En lille drilsk julenisse ved navn Tinker har taget min ønskeseddel 
        og gemt den væk! Han efterlod en besked om, at I kun kan låse min ønskeseddel op ved at 
        gennemføre denne særlige juleorienterings-udfordring.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="challenge-container">
        <h3>🎯 Sådan Gennemfører du Udfordringen:</h3>
        <div class="challenge-steps">
            <ol>
                <li>Vælg din by (Middelfart eller Aarhus)</li>
                <li>Download din rute som PDF nedenfor</li>
                <li>Følg sporet af magiske juleposter i din valgte by</li>
                <li>Ved hver post finder du et særligt nummer</li>
                <li>Indtast disse numre i felterne nedenfor i den rækkefølge, du finder dem</li>
                <li>Når alle de rigtige numre er indtastet, vil Tinkers magi afsløre min ønskeseddel!</li>
            </ol>
        </div>
        <p>❄️ Tag varmt tøj på, omfavn julestemningen, og god fornøjelse med dette magiske eventyr! ❄️</p>
    </div>
    """, unsafe_allow_html=True)

    expander = st.expander("Se forklaring", expanded=True)
    expander.write('''
    Posterne er stationære træpæle (se billede nedenfor). 
    For at låse ønskesedlen op skal du notere postnummeret (venstre side) og ikke koden (højre side).
    ''')
    
    # Use raw GitHub URL for the image
    expander.image("https://raw.githubusercontent.com/FPWRasmussen/JuleTur2024/main/images/post.jpg")

    city = st.selectbox("🎄 Vælg din magiske rute:", ["Middelfart", "Aarhus"])

    # Use raw GitHub URLs for PDFs
    pdf_urls = {
        "Middelfart": "https://raw.githubusercontent.com/FPWRasmussen/JuleTur2024/main/maps/Middelfart.pdf",
        "Aarhus": "https://raw.githubusercontent.com/FPWRasmussen/JuleTur2024/main/maps/Aarhus.pdf"
    }

    # Download PDF content
    response = requests.get(pdf_urls[city])
    pdf_content = response.content

    btn = st.download_button(
        label="Download PDF",
        data=pdf_content,
        file_name=f"{city}.pdf",
        mime="application/pdf",
    )

    st.markdown("<h3>✨ Indtast de magiske numre, du finder:</h3>", unsafe_allow_html=True)

    if city == "Middelfart":
        num_fields = 9
        cols = st.columns(num_fields)
        inputs = []
        
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"Post {i+1}")
                inputs.append(st.text_input("", key=f"m{i}", label_visibility="collapsed"))
        
        if all(inputs):
            try:
                if check_middelfart_sequence(inputs):
                    st.session_state.solved = True
                    st.session_state.show_error = False
                    st.rerun()
                else:
                    st.session_state.show_error = True
            except ValueError:
                st.session_state.show_error = True
        else:
            st.session_state.show_error = False

    elif city == "Aarhus":
        num_fields = 11
        cols = st.columns(num_fields)
        inputs = []
        
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"Post {i+1}")
                inputs.append(st.text_input("", key=f"a{i}", label_visibility="collapsed"))
        
        if all(inputs):
            try:
                if check_aarhus_sequence(inputs):
                    st.session_state.solved = True
                    st.session_state.show_error = False
                    st.rerun()
                else:
                    st.session_state.show_error = True
            except ValueError:
                st.session_state.show_error = True
        else:
            st.session_state.show_error = False

    if st.session_state.show_error:
        st.markdown("""
            <div class="error-message">
                <h4>🎅 Ho ho ho! De numre ser ikke helt rigtige ud!</h4>
                <p>Tjek numrene og prøv igen!</p>
            </div>
        """, unsafe_allow_html=True)

else:
    # Only show success message and wishlist when solved
    st.markdown("""
        <div class="success-message">
            <h2>🎉 Tillykke! Du har Brudt Tinkers Fortryllelse! 🎄</h2>
            <p>Nissens magi er forsvundet, og ønskesedlen er blevet afsløret!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="wishlist">
            <h2>🎁 Min Juleønskeseddel 🎁</h2>
            <ul>
                <li>Natbukser (M)</li>
                <li>Kuffert (~70L)</li>
                <li>Sokker med mønster/symboler (43)</li>
                <li>Skærebræt af træ</li>
                <li>Bagekogebog</li>
                <li>Blender</li>
                <li>Badehåndklæder</li>
                <li>Hvid t-shirt (M, rund udskæring)</li>
                <li>Fleecetrøje (M, mørk)</li>
                <li>Genopladelige AA batterier + oplader</li>
                <li>Margrethe skål med låg</li>
                <li>Gymnastikringe</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.snow()

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; font-size: 12px;'>
        Lavet med ❤️ og Julemagi 🎄
    </div>
""", unsafe_allow_html=True)