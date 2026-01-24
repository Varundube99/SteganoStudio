
🕵️‍♂️ STEAGANO STUDIO
AI-Powered Image Steganography using Deep Learning
=================================================

OVERVIEW
--------
Stegano Studio is a deep learning–based image steganography system that allows users
to hide one image inside another and later reveal it with minimal visual distortion.

Unlike traditional techniques such as Least Significant Bit (LSB) manipulation,
this project uses a neural autoencoder architecture trained end-to-end to learn
optimal hiding and recovery strategies directly from data.

The application features an interactive Streamlit interface, while trained models
are securely hosted on Hugging Face, ensuring a clean separation between open-source
application code and proprietary model weights.

🚀QUICK START
-----------
1. Clone the repository:
   git clone https://github.com/Varundube99/SteganoStudio.git
   cd SteganoStudio

2. Install dependencies:
   pip install -r requirements.txt

3. Run the Streamlit app:
   streamlit run app.py

⚠️NOTE:
Model weights are not included in this repository and are loaded securely from
Hugging Face at runtime.

✨KEY FEATURES
------------
- Hide a secret image inside a cover image
- Reveal the hidden image with high fidelity
- Deep learning–based autoencoder architecture
- Clean and interactive Streamlit UI
- Secure model loading from Hugging Face
- Fast inference using TensorFlow / Keras

🧠HOW IT WORKS
------------
The system consists of two jointly trained neural networks:

ENCODER:
- Takes two inputs:
  * Secret image
  * Cover image
- Outputs a container image that visually resembles the cover image while encoding
  the secret image.

DECODER:
- Takes the container image as input
- Reconstructs the hidden secret image

Both networks are optimized jointly to minimize visual distortion while preserving
accurate recovery of the hidden image.

🏗️MODEL ARCHITECTURE
------------------
Secret Image + Cover Image
        -> Encoder
        -> Container Image
        -> Decoder
        -> Revealed Image

Technical Details:
- Input size: 64 x 64 x 3
- Framework: TensorFlow / Keras
- Model format: .keras

🖥️APPLICATION PAGES
-----------------
HOME:
- Project overview
- Model explanation
- Limitations and future scope

HIDE IMAGE:
- Upload secret image
- Upload cover image
- Generate container image
- Download container image as PNG

REVEAL IMAGE:
- Upload container image
- Decode and reveal secret image
- Download revealed image

🔐MODEL SECURITY & DEPLOYMENT
---------------------------
To protect originality and trained model weights:
- Models are NOT stored in the GitHub repository
- Models are hosted privately on Hugging Face
- Access is controlled using Hugging Face access tokens
- Tokens are managed via Streamlit Secrets

This ensures:
- Open-source application code
- Private and protected model weights
- No accidental leakage of intellectual property

📁PROJECT STRUCTURE
-----------------
SteganoStudio/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml

🌐LIVE DEPLOYMENT
---------------
The project is deployed on Streamlit Cloud and is publicly accessible:

https://steganostudio.streamlit.app/

No local setup is required for basic usage.
Simply open the link, upload images, and start hiding or revealing secrets.

⚠️LIMITATIONS
-----------
- Model trained only on 64 x 64 images
- Output may appear pixelated when upscaled
- Not robust to heavy JPEG compression
- Avoid resizing or recompressing container images
- Best results achieved using PNG format

🚀 FUTURE WORK
-----------
- Training on higher resolutions (128 x 128, 256 x 256)
- Compression-resistant steganography
- Noise-aware loss functions
- Batch processing support
- Improved robustness to image transformations

📚RESEARCH BACKGROUND
-------------------
This project is inspired by research in neural steganography and autoencoder-based
image embedding.

Traditional rule-based steganography techniques are often fragile, while neural
approaches learn optimal hiding strategies directly from data.

👨‍💻AUTHOR
------
Varun Dubey
AI / ML Enthusiast
Email: varundube99@gmail.com

📜LICENSE
-------
This project is intended for educational and research purposes.
Model weights are proprietary and intentionally excluded from this repository.
