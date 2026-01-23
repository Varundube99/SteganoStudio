import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from huggingface_hub import hf_hub_download
import numpy as np
from PIL import Image
import os
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Image Processing App", page_icon="🖼️", layout="wide")

# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- STYLES ---
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0e0e10;
    color: #e5e5e5;
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #121214;
    border-right: 1px solid #1f1f1f;
    padding-top: 1rem;
}

/* App title */
.sidebar-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #00a8ff;
    margin-bottom: 2rem;
}

/* Navigation links */
.nav-link {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #e5e5e5;
    text-decoration: none;
    font-size: 1rem;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 12px;
    transition: background-color 0.2s ease, color 0.2s ease;
    cursor: pointer;
}
.nav-link:hover { background-color: #1f1f1f; }
.nav-link.active { background-color: #00a8ff; color: white !important; }
.icon { font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("""
<div class='sidebar-title'>Stegano Studio</div>
""", unsafe_allow_html=True)


options = ["🏠  Home", "🙈  Hide Image", "👁️  Reveal Image"]

# Function to update session state instantly 
def set_page():
    selected = st.session_state.nav_choice
    if "Home" in selected:
        st.session_state.page = "Home"
    elif "Hide" in selected:
        st.session_state.page = "Hide Image"
    elif "Reveal" in selected:
        st.session_state.page = "Reveal Image"


current_idx = 0
for i, opt in enumerate(options):
    if st.session_state.page in opt:
        current_idx = i
        break

# Radio input 
st.sidebar.radio(
    label="",
    options=options,
    index=current_idx,
    key="nav_choice",
    label_visibility="collapsed",
    on_change=set_page,
)

# --- CUSTOM STYLE  ---
st.markdown("""
<style>
/* Sidebar container */
[data-testid="stSidebar"] {
  background-color: #121214;
  border-right: 1px solid #1f1f1f;
  padding-top: 1rem;
}

/* Gradient title */
.sidebar-title {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(90deg, #00C6FF, #0072FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 2rem;
}

/* Hide radio circles */
div[role="radiogroup"] > label > div:first-child { display: none !important; }

/* Sidebar item layout */
div[role="radiogroup"] > label {
  display: flex !important;
  align-items: center;
  gap: 10px;
  background: transparent !important;
  color: #e5e5e5 !important;
  padding: 12px 16px !important;
  border-radius: 6px !important;
  margin-bottom: 12px !important;
  border: none !important;
  cursor: pointer !important;
  transition: all 0.25s ease !important;
  text-decoration: none !important;
  width: 100% !important;
  box-sizing: border-box !important;
  min-width: 180px !important;
}

/* Hover + Glow effect */
div[role="radiogroup"] > label:hover {
  background-color: #1f1f1f !important;
  box-shadow: 0 0 10px rgba(0, 168, 255, 0.25);
}

/* Active = sky blue */
div[role="radiogroup"] > label:has(input:checked) {
  background-color: #00A8FF !important;
  color: #ffffff !important;
  box-shadow: 0 0 14px rgba(0, 168, 255, 0.35);
  transform: translateY(-1px);
}

/* Icon alignment */
div[role="radiogroup"] > label p {
  margin: 0 !important;
  font-size: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# --- Configuration ---
IMG_HEIGHT = 64
IMG_WIDTH = 64
IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, 3)

# --- 1. Load Models  ---
@st.cache_resource
def load_steganography_models():
    repo_id = "dubevarun/stegano-models"
    token = st.secrets["HF_TOKEN"]

    encoder_path = hf_hub_download(
        repo_id=repo_id,
        filename="final_encoder.keras",
        token=token
    )

    decoder_path = hf_hub_download(
        repo_id=repo_id,
        filename="final_decoder.keras",
        token=token
    )

    encoder = load_model(
       encoder_path,
       compile=False,
       safe_mode=False
      )

    decoder = load_model(
        decoder_path,
        compile=False,
        safe_mode=False
      )


    return encoder, decoder


# --- 2. Image Preprocessing Function ---
def preprocess_image(image_file, target_size=(IMG_WIDTH, IMG_HEIGHT)):
    """Loads, resizes, and normalizes an uploaded image."""
    try:
        img = Image.open(image_file).convert('RGB')
        img = img.resize(target_size, Image.Resampling.LANCZOS)  # Resize to 64x64
        img_array = np.array(img, dtype=np.float32) / 255.0      # Normalize [0, 1]
        img_array = np.expand_dims(img_array, axis=0)            # Add batch dimension
        return img_array
    except Exception as e:
        st.error(f"Error preprocessing image: {e}")
        return None

# --- 3. Image Postprocessing Function ---
def postprocess_image(image_tensor):
    """Converts a model output tensor back to a displayable PIL Image."""
    img_array = np.squeeze(image_tensor, axis=0)
    img_array = (img_array * 255.0).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    return img

def render_home():
    
    st.markdown("""
    <style>
      :root {
        --ss-bg:#0e0e10;
        --ss-panel:#18181b;
        --ss-border:#26262a;
        --ss-text:#ededed;
        --ss-muted:#b8b8b8;
        --ss-accent:#00A8FF;
        --ss-shadow:0 8px 24px rgba(0,168,255,.12);
      }

      html, body, [data-testid="stAppViewContainer"] {
        background:var(--ss-bg)!important;
        color:var(--ss-text)!important;
        font-family:'Inter',sans-serif;
      }

      /* GENERAL TITLES */
      .section-title {
        font-size: clamp(22px, 3vw, 28px);
        font-weight:800;
        margin-top:40px;
        margin-bottom:16px;
      }

      .ss-card {
        background:var(--ss-panel);
        border:1px solid var(--ss-border);
        border-radius:16px;
        padding:22px;
        transition:all .25s ease;
        box-shadow:var(--ss-shadow);
      }
      .ss-card:hover {
        border-color:var(--ss-accent);
        transform:translateY(-2px);
      }

      .ss-grid-2 {
        display:grid;
        grid-template-columns:repeat(auto-fit, minmax(340px, 1fr));
        gap:22px;
        margin-top:10px;
      }

      .ss-grid-4 {
        display:grid;
        grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));
        gap:18px;
        margin-top:10px;
      }

      .ss-subtext { color:var(--ss-muted); font-size:15px; margin-top:4px; }

      .hero {
        display:flex;
        align-items:center;
        justify-content:space-between;
        background:var(--ss-panel);
        border:1px solid var(--ss-border);
        border-radius:18px;
        padding:30px 36px;
        box-shadow:var(--ss-shadow);
      }
      .hero img { width:240px; border-radius:12px; }

      .hero h1 {
        font-size:clamp(28px, 4vw, 36px);
        font-weight:800;
        margin-bottom:8px;
      }

      .hero p { font-size:15px; color:var(--ss-muted); }

      .ss-feature-icon { font-size:28px; margin-bottom:8px; }

      ul { padding-left:20px; }
      li { color:var(--ss-muted); margin:6px 0; font-size:15px; }
      b { color:#fff; }
    </style>
    """, unsafe_allow_html=True)

    # --- HERO INTRO  ---
    st.markdown("""
    <style>
       .hero-main-title {
          font-size: 2.3rem;
          font-weight: 800;
          margin-top: 80px;
          margin-bottom: 10px;
          color: transparent;
          background: linear-gradient(90deg, #ffcc00, #ff8a00, #ff007f);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          text-shadow: 0 0 25px rgba(255, 200, 50, 0.25);
          animation: flicker 4s infinite;
       }
       @keyframes flicker {
          0%, 18%, 22%, 25%, 53%, 57%, 100% { text-shadow: 0 0 20px rgba(255, 0, 150, 0.4); opacity: 1; }
          20%, 24%, 55% { opacity: 0.6; }
       }
    </style>

    <div style="text-align: center;">
        <h2 class="hero-main-title">Stegano Studio</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- WELCOME SECTION ---
    st.markdown("""
    <style>
        .hero-wrapper { text-align: left; padding: 40px 0 10px 0; }

        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: 0.8px;
            margin-bottom: 12px;
            background: linear-gradient(90deg, #00e0ff, #00ffa2, #00e0ff);
            background-size: 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientFlow 6s ease-in-out infinite;
            text-shadow: 0 0 25px rgba(0, 255, 255, 0.15);
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>

    <div class="hero-wrapper">
        <h1 class="hero-title">Welcome to Stegano Studio</h1>
    </div>
     """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .welcome-box {
      background: linear-gradient(145deg, #131418, #0d0e10);
      border: 1px solid rgba(0, 180, 255, 0.2);
      border-radius: 18px;
      padding: 36px 32px;
      margin-top: 12px;
      box-shadow: 0 0 30px rgba(0, 200, 255, 0.08);
      transition: all 0.3s ease;
      line-height: 1.65;
    }
    .welcome-box:hover {
      border-color: rgba(0, 200, 255, 0.45);
      box-shadow: 0 0 38px rgba(0, 200, 255, 0.15);
      transform: translateY(-3px);
    }
    .welcome-box p { color: #d0d4da; font-size: 1.05rem; letter-spacing: 0.3px; margin-bottom: 12px; }
    .welcome-box strong { color: #66e0ff; font-weight: 600; }
    .welcome-highlight {
      font-size: 1.1rem;
      background: linear-gradient(90deg, #00e0ff, #00ffa2);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-weight: 600;
    }
    </style>

    <div class="welcome-box">
      <p>
        Welcome to <span class="welcome-highlight">Stegano Studio</span> — a deep learning–powered environment for 
        <strong>AI-based image steganography</strong>. Conceal one image flawlessly within another with cutting-edge precision.
      </p>
      <p>
        Unlike conventional <strong>LSB or manual encoding</strong> techniques, Stegano Studio employs a 
        <strong>trained autoencoder neural network</strong> that learns to blend hidden data invisibly — ensuring 
        <strong>robust security</strong>, <strong>imperceptible distortion</strong>, and <strong>minimal detection risk</strong>.
      </p>
      <p>
        Whether you’re exploring <strong>AI-driven data protection</strong>, <strong>digital watermarking</strong>, 
        or <strong>covert communication</strong>, this platform offers a secure, intelligent, and elegant solution 
        for hiding information in plain sight.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # --- PURPOSE SECTION ---
    st.markdown("""
    <style>
        .section-title {
            font-size: 2rem;
            font-weight: 750;
            letter-spacing: 0.6px;
            margin: 0;
            padding: 800px 0 800px 0;  /* kept exactly as yours; responsive overrides below for small screens */
            display: block;
            background: linear-gradient(90deg, #9d5cff, #00b3ff, #9d5cff);
            background-size: 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: sectionGradient 7s ease-in-out infinite;
            text-shadow: 0 0 18px rgba(157, 92, 255, 0.18);
        }
        @keyframes sectionGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>

    <div style="padding: 40px 0;">
        <h2 class="section-title">Purpose</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* ---- Beautified Card Styling ---- */
    .info-box {
      background: var(--ss-panel);
      border: 1px solid rgba(0, 180, 255, 0.2);
      border-radius: 16px;
      padding: 28px 24px;
      box-shadow: 0 0 18px rgba(0, 180, 255, 0.05);
      text-align: center;
      transition: all 0.3s ease;
    }
    .info-box:hover {
      border-color: rgba(0, 200, 255, 0.45);
      transform: translateY(-4px);
      box-shadow: 0 0 25px rgba(0, 200, 255, 0.15);
    }
    .info-box h3 { margin-top: 10px; font-size: 1.3rem; color: #fff; letter-spacing: 0.4px; }
    .info-box p { color: #cfd2d7; font-size: 0.95rem; line-height: 1.55; margin-top: 10px; }
    .info-box p strong { color: #66e0ff; font-weight: 600; }
    .info-icon { font-size: 2rem; margin-bottom: 8px; display: block; color: #00e0ff;
                 filter: drop-shadow(0 0 6px rgba(0, 224, 255, 0.3)); }
    </style>

    <div style="display: flex; gap: 22px; justify-content: center; flex-wrap: wrap;">
      <div class="info-box" style="flex:1; min-width:250px; max-width:360px;">
        <div class="info-icon">🔒</div>
        <h3>Secure Hiding</h3>
        <p>Powered by a <strong>neural autoencoder</strong> that conceals one image within another with
          <strong>pixel-perfect precision</strong>. Hidden patterns blend seamlessly, invisible even
          under close inspection.</p>
      </div>

      <div class="info-box" style="flex:1; min-width:250px; max-width:360px;">
        <div class="info-icon">💡</div>
        <h3>Simple Interface</h3>
        <p><strong>Drag, drop, and conceal</strong> — that’s it. Stegano Studio removes complexity so you can focus on what matters:
          <strong>secure image embedding</strong> with zero code.</p>
      </div>

      <div class="info-box" style="flex:1; min-width:250px; max-width:360px;">
        <div class="info-icon">⚙️</div>
        <h3>High Accuracy</h3>
        <p>Produces <strong>visually identical</strong> container images with no loss in quality.  
          Even advanced <strong>steganalysis tools</strong> fail to spot the difference.</p>
      </div>

      <div class="info-box" style="flex:1; min-width:250px; max-width:360px;">
        <div class="info-icon">🎓</div>
        <h3>Academic Foundation</h3>
        <p>Backed by <strong>neural steganography research</strong> and trained on
          <strong>100k+ image pairs</strong>, uniting academic precision with real-world usability.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- MODEL EXPLANATION ----------
    st.markdown(
        """ <div style="padding: 40px 0;">
        <h2 class="section-title">Model Explanation</h2>
          </div>""",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.2, 1.2])  

    with col1:
        st.markdown(
            """
            <div class="ss-card" style="padding-top:20px;">
                <div style="display:flex; justify-content:center; align-items:center; gap:10px; margin-bottom:12px;">
                    <div style="background:#1f1f1f; padding:6px 14px; border-radius:8px; font-weight:600;">Secret</div>
                    <div style="font-size:22px; opacity:0.7;">➜</div>
                    <div style="background:#1f1f1f; padding:6px 14px; border-radius:8px; font-weight:600;">Container</div>
                    <div style="font-size:22px; opacity:0.7;">➜</div>
                    <div style="background:#1f1f1f; padding:6px 14px; border-radius:8px; font-weight:600;">Decoder</div>
                </div>
                <ul style="text-align:left; color:#b8b8b8; font-size:15px; line-height:1.6;">
                    <li><b>Encoder</b> merges the secret image into the cover to create a hidden container.</li>
                    <li><b>Decoder</b> extracts the secret back from the container with minimal loss.</li>
                    <li>Optimized for low visual distortion and accurate recovery.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        
        svg_card = """
        <div class="ss-card" style="text-align:center; padding:20px 10px;">
            <div style="display:flex; justify-content:center; margin-bottom:10px; width:100%;">
                <svg viewBox="0 0 820 220" width="100%" height="auto" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
                  <defs>
                    <linearGradient id="blueFill" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0" stop-color="#6F86FF"/>
                      <stop offset="1" stop-color="#5570FF"/>
                    </linearGradient>
                    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                      <feGaussianBlur in="SourceGraphic" stdDeviation="3.2" result="blur"/>
                      <feMerge>
                        <feMergeNode in="blur"/>
                        <feMergeNode in="SourceGraphic"/>
                      </feMerge>
                    </filter>
                    <style>
                      .edge{stroke:#7f97ff; stroke-opacity:.28; stroke-width:1.8; stroke-linecap:round}
                      .edgeStrong{stroke:#7f97ff; stroke-opacity:.5; stroke-width:1.9; stroke-linecap:round}
                      .node{fill:url(#blueFill); filter:url(#glow)}
                      .label{fill:#EAEAF0; font:14px "Poppins", ui-sans-serif}
                    </style>
                  </defs>

                  <!-- Encoder–Decoder Diagram -->
                  <g stroke="#6F86FF" stroke-opacity=".55" stroke-width="2" stroke-linecap="round">
                    <line x1="40" y1="70" x2="70" y2="70"/>
                    <line x1="40" y1="100" x2="70" y2="100"/>
                    <line x1="40" y1="130" x2="70" y2="130"/>
                  </g>

                  <g>
                    <circle class="node" cx="100" cy="70" r="7"/>
                    <circle class="node" cx="100" cy="100" r="7"/>
                    <circle class="node" cx="100" cy="130" r="7"/>
                  </g>

                  <g class="edge">
                    <line x1="70" y1="70" x2="94" y2="70"/>
                    <line x1="70" y1="100" x2="94" y2="100"/>
                    <line x1="70" y1="130" x2="94" y2="130"/>
                  </g>

                  <g>
                    <circle class="node" cx="150" cy="85"  r="7"/>
                    <circle class="node" cx="150" cy="115" r="7"/>
                  </g>

                  <g class="edge">
                    <line x1="106" y1="70"  x2="144" y2="85"/>
                    <line x1="106" y1="70"  x2="144" y2="115"/>
                    <line x1="106" y1="100" x2="144" y2="85"/>
                    <line x1="106" y1="100" x2="144" y2="115"/>
                    <line x1="106" y1="130" x2="144" y2="85"/>
                    <line x1="106" y1="130" x2="144" y2="115"/>
                  </g>

                  <rect x="210" y="75" width="70" height="70" rx="15" fill="url(#blueFill)" filter="url(#glow)"/>
                  <g class="edge">
                    <line x1="156" y1="85"  x2="210" y2="110"/>
                    <line x1="156" y1="115" x2="210" y2="110"/>
                  </g>

                  <g>
                    <circle class="node" cx="320" cy="110" r="7"/>
                    <circle class="node" cx="350" cy="110" r="7"/>
                  </g>

                  <g>
                    <line class="edge" x1="280" y1="110" x2="314" y2="110"/>
                    <line class="edgeStrong" x1="326" y1="110" x2="344" y2="110"/>
                  </g>

                  <g>
                    <circle class="node" cx="410" cy="85"  r="7"/>
                    <circle class="node" cx="410" cy="115" r="7"/>
                  </g>

                  <g class="edge">
                    <line x1="356" y1="110" x2="404" y2="85"/>
                    <line x1="356" y1="110" x2="404" y2="115"/>
                  </g>

                  <g>
                    <circle class="node" cx="460" cy="70"  r="7"/>
                    <circle class="node" cx="460" cy="100" r="7"/>
                    <circle class="node" cx="460" cy="130" r="7"/>
                  </g>

                  <g class="edge">
                    <line x1="416" y1="85"  x2="454" y2="70"/>
                    <line x1="416" y1="85"  x2="454" y2="100"/>
                    <line x1="416" y1="85"  x2="454" y2="130"/>
                    <line x1="416" y1="115" x2="454" y2="70"/>
                    <line x1="416" y1="115" x2="454" y2="100"/>
                    <line x1="416" y1="115" x2="454" y2="130"/>
                  </g>

                  <g filter="url(#glow)">
                    <circle cx="530" cy="110" r="18" fill="url(#blueFill)"/>
                    <circle cx="530" cy="110" r="8" fill="#0E0F13"/>
                  </g>

                  <g>
                    <line class="edgeStrong" x1="466" y1="100" x2="512" y2="110"/>
                  </g>

                  <text class="label" x="80"  y="180">Encoder</text>
                  <text class="label" x="235" y="180">Image</text>
                  <text class="label" x="410" y="180">Decoder</text>
                </svg>
            </div>
        </div>
        """
        st.components.v1.html(svg_card, height=220, scrolling=False)

    # --- LIMITATIONS SECTION ---
    st.markdown("""
    <style>
      /* --- Section Title --- */
      .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #00bfff;
        text-align: left;
        position: relative;
        margin-bottom: 3rem;
      }
      .section-title::after {
        content: '';
        display: block;
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #00e0ff, #007bff);
        margin: 0.5rem auto 0;
        border-radius: 2px;
      }

      /* --- Grid Layout --- */
      .ss-grid-3 {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 18px;
      }

      /* --- Card Styling --- */
      .ss-card {
        background: linear-gradient(145deg, #141416, #0e0e10);
        border: 1px solid #222;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 0 15px rgba(0, 200, 255, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: left;
      }
      .ss-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 0 25px rgba(0, 200, 255, 0.25);
      }

      /* --- Headings --- */
      .ss-card h4 {
        font-size: 1.2rem;
        color: #00e0ff;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
      }

      /* --- Icons --- */
      .ss-icon { font-size: 1.5rem; }

      /* --- Paragraph Text --- */
      .ss-card p {
        color: #d1d1d1;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
      }
    </style>

    <div style="padding: 40px 0;">
        <h2 class="section-title">Limitations & Future Work</h2>
    </div>

    <div class="ss-grid-3">
      <div class="ss-card">
        <h4><span class="ss-icon">🧩</span> Pixel Size</h4>
        <p>The current model is trained exclusively on 64×64 pixel datasets, limiting visual clarity on larger images.
           As a result, revealed outputs may appear soft or slightly pixelated when upscaled.</p>
      </div>

      <div class="ss-card">
        <h4><span class="ss-icon">⚠️</span> Compression Vulnerability</h4>
        <p>The model’s performance degrades with lossy compression, especially JPEG or WhatsApp re-encoding.
           To ensure precise recovery, use lossless formats such as PNG and avoid image resizing or filtering post-embedding.</p>
      </div>

      <div class="ss-card">
        <h4><span class="ss-icon">🚀</span> Future Work</h4>
        <p>Planned research includes:<br>
          – Training on higher-resolution datasets (128×128, 256×256).<br>
          – Implementing noise-resistant encoding layers.<br>
          – Optimizing decoder against compression and color shifts.<br>
          – Exploring adaptive architectures for real-time embedding.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- SIMPLE CLEAN FOOTER ---
    st.markdown("""
    <style>
        .footer-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 60px 20px 40px 20px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }
        .footer-container p { color: #b5b5b5; font-size: 0.9rem; margin: 8px 0; }
        .footer-container .footer-links { margin-top: 10px; color: #b5b5b5; }
        .footer-container a {
            color: #00b3ff; text-decoration: none; margin: 0 8px; transition: color 0.3s ease;
        }
        .footer-container a:hover { color: #9d5cff; }
        .footer-container .brand { font-weight: 700; color: #e2e2e2; }

        /* --- RESPONSIVE OVERRIDES (no visual change on desktop) --- */
        @media (max-width: 1024px) {
            /* shrink the huge purpose padding only on smaller screens */
            .section-title { padding: 120px 0 120px 0 !important; }
            .welcome-box { padding: 28px 22px; }
        }
        @media (max-width: 768px) {
            .hero-main-title { font-size: 2rem; margin-top: 48px; margin-bottom: 8px; }
            .hero-title { font-size: 2.2rem; }
            .welcome-box p { font-size: clamp(0.95rem, 2.6vw, 1.05rem); line-height: 1.7; }
            .ss-grid-4, .ss-grid-2 { gap: 16px; }
        }
        @media (max-width: 480px) {
            .hero-main-title { font-size: 1.8rem; }
            .hero-title { font-size: 1.9rem; }
            .section-title { font-size: 1.6rem; }
        }
    </style>

    <div class="footer-container">
        <p class="brand">© 2025 Stegano Studio</p>
        <div class="footer-links">
            <a href="#">Educational Tool</a> |
            <a href="https://mail.google.com/mail/?view=cm&fs=1&to=varundube99@gmail.com" target="_blank">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_hide_page(encoder):
    import io

    # --- THEME CSS ---
    st.markdown("""
    <style>
      :root {
        --ss-bg:#0e0e10;
        --ss-panel:#18181b;
        --ss-border:#26262a;
        --ss-text:#ededed;
        --ss-muted:#b8b8b8;
        --ss-accent:#00A8FF;
        --ss-shadow:0 8px 24px rgba(0,168,255,.12);
      }

      html, body, [data-testid="stAppViewContainer"] {
        background:var(--ss-bg)!important;
        color:var(--ss-text)!important;
        font-family:'Inter',sans-serif;
      }

      .ss-title { font-size: clamp(26px, 3vw, 32px); font-weight:800; margin:10px 0 6px 0; }
      .ss-subtext { color:var(--ss-muted); font-size:16px; margin-bottom:20px; }

      .ss-stepcard {
        background:var(--ss-panel);
        border:1px solid var(--ss-border);
        border-radius:14px;
        padding:20px 24px;
        margin:18px 0 40px 0;
        box-shadow:var(--ss-shadow);
      }
      .ss-stepcard h3 { margin:0 0 10px 0; font-size:20px; color:var(--ss-accent); }
      .ss-step { margin:6px 0; color:var(--ss-text); font-size:16px; }

      div[data-testid="stButton"] > button {
        background:var(--ss-accent); color:#fff; border:none; border-radius:10px; padding:12px 18px;
        font-weight:600; width:100%; transition:box-shadow .25s ease, transform .2s ease;
      }
      div[data-testid="stButton"] > button:hover { box-shadow:0 0 18px rgba(0,168,255,.35); transform:translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

    # --- PAGE CONTENT ---
    st.markdown('<h1 class="ss-title">Hide a Secret Image</h1>', unsafe_allow_html=True)

    # --- STEP GUIDE  ---
    st.markdown("""
    <style>
        .ss-stepcard {
            background: linear-gradient(145deg, #18181b, #0f0f11);
            border: 1px solid rgba(0, 200, 255, 0.08);
            border-radius: 18px;
            padding: 28px 32px;
            margin-top: 30px;
            box-shadow: 0 0 25px rgba(0, 200, 255, 0.08);
            transition: box-shadow 0.4s ease, transform 0.3s ease;
        }
        .ss-stepcard:hover { box-shadow: 0 0 35px rgba(0, 200, 255, 0.18); transform: translateY(-4px); }
        .ss-stepcard h3 {
            font-size: 1.4rem; color: #00e0ff; font-weight: 700; margin-bottom: 16px;
            text-shadow: 0 0 15px rgba(0, 224, 255, 0.25); display: flex; align-items: center; gap: 8px;
        }
        .ss-step {
            background: rgba(255, 255, 255, 0.02);
            border-left: 3px solid #00ffa2;
            border-radius: 10px; padding: 10px 16px; margin-bottom: 12px;
            font-size: 1rem; color: #d0d0d0; transition: all 0.3s ease;
        }
        .ss-step:hover { background: rgba(0, 255, 200, 0.06); transform: translateX(6px); border-left-color: #00e0ff; color: #ffffff; }
    </style>

    <div class="ss-stepcard">
      <h3>🧭 How to Use</h3>
      <div class="ss-step">1️⃣  Select your <b>Secret Image</b></div>
      <div class="ss-step">2️⃣  Select your <b>Cover Image</b> (where you want to hide it)</div>
      <div class="ss-step">3️⃣  Click <b>Generate</b> to hide your secret</div>
    </div>
    """, unsafe_allow_html=True)

    # --- UPLOADS DIRECTLY  ---
    col1, col2 = st.columns(2)
    with col1:
        secret_file = st.file_uploader("Upload your Secret Image", type=["jpg", "png", "jpeg"], key="secret")
    with col2:
        cover_file = st.file_uploader("Upload your Cover Image", type=["jpg", "png", "jpeg"], key="cover")

    # --- PROCESS IMAGES ---
    if secret_file and cover_file:
        st.markdown("<br><h4>Uploaded Images (resized to 64x64)</h4>", unsafe_allow_html=True)
        processed_secret_img = preprocess_image(secret_file)
        processed_cover_img = preprocess_image(cover_file)

        if processed_secret_img is not None and processed_cover_img is not None:
            colA, colB = st.columns(2)
            with colA:
                st.image(postprocess_image(processed_secret_img),
                         caption="Secret Image (64x64)", use_container_width=True)
            with colB:
                st.image(postprocess_image(processed_cover_img),
                         caption="Cover Image (64x64)", use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- GENERATE BUTTON ---
            if st.button("🔒 Generate Container Image", use_container_width=True):
                with st.spinner("Hiding secret image..."):
                    try:
                        # Encode secret into cover
                        container_tensor = encoder.predict([processed_secret_img, processed_cover_img])
                        container_image_pil = postprocess_image(container_tensor)

                        st.success("✅ Secret image hidden successfully!")
                        st.image(container_image_pil, caption="Container Image (Secret Hidden)",
                                 use_container_width=True)

                        # --- DOWNLOAD BUTTON ---
                        buf = io.BytesIO()
                        container_image_pil.save(buf, format="PNG")
                        buf.seek(0)  

                        st.download_button(
                            label="⬇️ Download Container Image (PNG)",
                            data=buf,
                            file_name="container_image.png",
                            mime="image/png",
                            use_container_width=True
                        )

                    except Exception as e:
                        st.error(f"❌ An error occurred during encoding: {e}")

def render_reveal_page(decoder):
    import io

    # --- THEME CSS ---
    st.markdown("""
    <style>
      :root {
        --ss-bg:#0e0e10;
        --ss-panel:#18181b;
        --ss-border:#26262a;
        --ss-text:#ededed;
        --ss-muted:#b8b8b8;
        --ss-accent:#00A8FF;
        --ss-shadow:0 8px 24px rgba(0,168,255,.12);
      }

      html, body, [data-testid="stAppViewContainer"] {
        background:var(--ss-bg)!important;
        color:var(--ss-text)!important;
        font-family:'Inter',sans-serif;
      }

      .ss-title { font-size: clamp(26px, 3vw, 32px); font-weight:800; margin:10px 0 6px 0; }
      .ss-subtext { color:var(--ss-muted); font-size:16px; margin-bottom:20px; }

      .ss-stepcard {
        background:var(--ss-panel);
        border:1px solid var(--ss-border);
        border-radius:14px;
        padding:20px 24px;
        margin:18px 0 40px 0;
        box-shadow:var(--ss-shadow);
      }
      .ss-stepcard h3 { margin:0 0 10px 0; font-size:20px; color:var(--ss-accent); }
      .ss-step { margin:6px 0; color:var(--ss-text); font-size:16px; }

      div[data-testid="stButton"] > button {
        background:var(--ss-accent);
        color:#fff;
        border:none;
        border-radius:10px;
        padding:12px 18px;
        font-weight:600;
        width:100%;
        transition:box-shadow .25s ease, transform .2s ease;
      }
      div[data-testid="stButton"] > button:hover {
        box-shadow:0 0 18px rgba(0,168,255,.35);
        transform:translateY(-1px);
      }
    </style>
    """, unsafe_allow_html=True)

    # --- PAGE CONTENT ---
    st.markdown('<h1 class="ss-title">Reveal a Secret Image</h1>', unsafe_allow_html=True)

    # --- STEP GUIDE  ---
    st.markdown("""
    <style>
        .ss-stepcard {
            background: linear-gradient(145deg, #18181b, #0f0f11);
            border: 1px solid rgba(0, 200, 255, 0.08);
            border-radius: 18px;
            padding: 28px 32px;
            margin-top: 30px;
            box-shadow: 0 0 25px rgba(0, 200, 255, 0.08);
            transition: box-shadow 0.4s ease, transform 0.3s ease;
        }
        .ss-stepcard:hover { box-shadow: 0 0 35px rgba(0, 200, 255, 0.18); transform: translateY(-4px); }
        .ss-stepcard h3 {
            font-size: 1.4rem; color: #00e0ff; font-weight: 700; margin-bottom: 16px;
            text-shadow: 0 0 15px rgba(0, 224, 255, 0.25); display: flex; align-items: center; gap: 8px;
        }
        .ss-step {
            background: rgba(255, 255, 255, 0.02);
            border-left: 3px solid #00ffa2;
            border-radius: 10px; padding: 10px 16px; margin-bottom: 12px;
            font-size: 1rem; color: #d0d0d0; transition: all 0.3s ease;
        }
        .ss-step:hover { background: rgba(0, 255, 200, 0.06); transform: translateX(6px); border-left-color: #00e0ff; color: #ffffff; }
    </style>

    <div class="ss-stepcard">
      <h3>🧭 How to Use</h3>
      <div class="ss-step">1️⃣  Upload your <b>Container Image</b> (the image with the hidden secret)</div>
      <div class="ss-step">2️⃣   Click <b>Reveal Secret Image</b></div>
      <div class="ss-step">3️⃣   Download the revealed secret</div>
    </div>
    """, unsafe_allow_html=True)

    # --- DIRECT UPLOAD (no outer boxes) ---
    container_file = st.file_uploader("Upload the Container Image", type=["jpg", "png", "jpeg"], key="container")

    # --- PROCESS IMAGE ---
    if container_file:
        processed_container_img = preprocess_image(container_file)
        if processed_container_img is not None:
            st.markdown("<br><h4>Uploaded Container (resized to 64x64)</h4>", unsafe_allow_html=True)
            st.image(postprocess_image(processed_container_img), caption="Uploaded Container", use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Reveal Secret Image", use_container_width=True):
                with st.spinner("Revealing secret image..."):
                    try:
                        revealed_tensor = decoder.predict(processed_container_img)
                        revealed_image_pil = postprocess_image(revealed_tensor)

                        st.success("Secret image revealed!")
                        st.image(revealed_image_pil, caption="Revealed Secret Image", use_container_width=True)

                        buf = io.BytesIO()
                        revealed_image_pil.save(buf, format="PNG")
                        byte_im = buf.getvalue()

                        st.download_button(
                            label="Download Revealed Image (as PNG)",
                            data=byte_im,
                            file_name="revealed_image.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"An error occurred during decoding: {e}")

# --- LOAD MODELS ONCE ---
encoder, decoder = load_steganography_models()

# --- ROUTING ---
if st.session_state.page == "Home":
    render_home()
elif st.session_state.page == "Hide Image":
    if encoder:
        render_hide_page(encoder)
    else:
        st.error("Encoder model is not loaded. Cannot render 'Hide Image' page.")
elif st.session_state.page == "Reveal Image":
    if decoder:
        render_reveal_page(decoder)
    else:
        st.error("Decoder model is not loaded. Cannot render 'Reveal Image' page.")
