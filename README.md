# 🕵️‍♂️ Stegano Studio

<div align="center">

**AI-Powered Image Steganography using Deep Learning**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-blue?style=for-the-badge)](LICENSE)

[🌐 Live Demo](https://steganostudio.streamlit.app/) • [📖 Documentation](#-how-it-works) • [🐛 Report Bug](https://github.com/Varundube99/SteganoStudio/issues) • [💡 Request Feature](https://github.com/Varundube99/SteganoStudio/issues)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [How It Works](#-how-it-works)
- [Model Architecture](#️-model-architecture)
- [Application Pages](#️-application-pages)
- [Model Security & Deployment](#-model-security--deployment)
- [Project Structure](#-project-structure)
- [Live Deployment](#-live-deployment)
- [Limitations](#️-limitations)
- [Future Work](#-future-work)
- [Research Background](#-research-background)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Author](#️-author)
- [License](#-license)

---

## 📖 Overview

**Stegano Studio** is a deep learning–based image steganography system that allows users to hide one image inside another and later reveal it with minimal visual distortion.

Unlike traditional techniques such as **Least Significant Bit (LSB)** manipulation, this project uses a neural autoencoder architecture trained end-to-end to learn optimal hiding and recovery strategies directly from data.

The application features an interactive **Streamlit** interface, while trained models are securely hosted on **Hugging Face**, ensuring a clean separation between open-source application code and proprietary model weights.

---

## ✨ Key Features

- 🔒 **Hide a secret image** inside a cover image with minimal visual distortion
- 🔓 **Reveal the hidden image** with high fidelity reconstruction
- 🧠 **Deep learning–based autoencoder architecture** for optimal embedding
- 🎨 **Clean and interactive Streamlit UI** for easy usage
- 🔐 **Secure model loading** from Hugging Face with access token protection
- ⚡ **Fast inference** using TensorFlow/Keras optimized models
- 🌐 **Cloud deployment** available for instant access

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Varundube99/SteganoStudio.git
   cd SteganoStudio
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Hugging Face access (for local deployment):**
   - Create a `.streamlit/secrets.toml` file
   - Add your Hugging Face token:
     ```toml
     HUGGINGFACE_TOKEN = "your_token_here"
     ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

6. **Access the application:**
   - Open your browser and navigate to `http://localhost:8501`

> ⚠️ **Note:** Model weights are not included in this repository and are loaded securely from Hugging Face at runtime. For local deployment, you'll need Hugging Face access credentials.

---

## 🧠 How It Works

The system consists of two jointly trained neural networks:

### **Encoder Network**
- **Input:** 
  - Secret image (the image to hide)
  - Cover image (the image that will contain the secret)
- **Output:** 
  - Container image that visually resembles the cover image while encoding the secret image

### **Decoder Network**
- **Input:** 
  - Container image (the encoded image)
- **Output:** 
  - Reconstructed secret image (the revealed hidden image)

Both networks are optimized jointly to minimize visual distortion while preserving accurate recovery of the hidden image. The training process uses a combination of reconstruction loss and perceptual loss to ensure both visual quality and accurate decoding.

---

## 🏗️ Model Architecture

```
Secret Image + Cover Image
        ↓
    [Encoder]
        ↓
  Container Image
        ↓
    [Decoder]
        ↓
  Revealed Image
```

### Technical Details

- **Input size:** 64 × 64 × 3 (RGB images)
- **Framework:** TensorFlow / Keras
- **Model format:** `.keras`
- **Architecture:** Convolutional Autoencoder with skip connections
- **Training:** End-to-end optimization with joint loss function

---

## 🖥️ Application Pages

### 🏠 **Home**
- Project overview and introduction
- Model architecture explanation
- Limitations and future scope
- Quick navigation to other pages

### 🔒 **Hide Image**
- Upload secret image (the image to hide)
- Upload cover image (the host image)
- Generate container image with embedded secret
- Download container image as PNG format

### 🔓 **Reveal Image**
- Upload container image (the encoded image)
- Decode and reveal the hidden secret image
- Download revealed image
- View reconstruction quality metrics

---

## 🔐 Model Security & Deployment

To protect originality and trained model weights:

- ✅ Models are **NOT** stored in the GitHub repository
- ✅ Models are hosted **privately** on Hugging Face
- ✅ Access is controlled using **Hugging Face access tokens**
- ✅ Tokens are managed via **Streamlit Secrets** (for local deployment)

This ensures:
- 🔓 **Open-source application code** for transparency and collaboration
- 🔒 **Private and protected model weights** to preserve intellectual property
- 🛡️ **No accidental leakage** of proprietary models
- 🔑 **Secure access control** for authorized users only

---

## 📁 Project Structure

```
SteganoStudio/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .streamlit/           # Streamlit configuration
    └── secrets.toml      # Hugging Face token (not in repo)
```

---

## 🌐 Live Deployment

The project is deployed on **Streamlit Cloud** and is publicly accessible:

### 🔗 [https://steganostudio.streamlit.app/](https://steganostudio.streamlit.app/)

**No local setup is required for basic usage!**

Simply open the link, upload images, and start hiding or revealing secrets. The live deployment handles all model loading and inference automatically.

---

## ⚠️ Limitations

- **Resolution constraint:** Model trained only on 64 × 64 images
- **Upscaling artifacts:** Output may appear pixelated when upscaled
- **Compression sensitivity:** Not robust to heavy JPEG compression
- **Image format:** Best results achieved using PNG format (lossless)
- **Processing requirements:** Avoid resizing or recompressing container images
- **Single image processing:** Currently supports one image at a time

**Best Practices:**
- Use PNG format for both input and output images
- Avoid resizing container images before decoding
- Use images close to 64×64 resolution for optimal results

---

## 🚀 Future Work

- [ ] Training on higher resolutions (128 × 128, 256 × 256)
- [ ] Compression-resistant steganography (JPEG-aware training)
- [ ] Noise-aware loss functions for better robustness
- [ ] Batch processing support for multiple images
- [ ] Improved robustness to image transformations
- [ ] Real-time video steganography support
- [ ] Advanced encryption options for additional security
- [ ] Performance optimization for faster inference
- [ ] Mobile app development
- [ ] API endpoint for programmatic access

---

## 📚 Research Background

This project is inspired by research in **neural steganography** and **autoencoder-based image embedding**.

Traditional rule-based steganography techniques (like LSB manipulation) are often fragile and easily detectable. Neural approaches, on the other hand, learn optimal hiding strategies directly from data, resulting in:

- **Better visual quality** of container images
- **Higher capacity** for hidden information
- **Improved robustness** to various image processing operations
- **Adaptive encoding** based on image content

### Related Research Areas
- Deep learning-based steganography
- Adversarial steganography
- Neural image compression
- Generative adversarial networks (GANs) for steganography

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Model loading fails**
- **Solution:** Ensure your Hugging Face token is correctly set in `.streamlit/secrets.toml`
- **Solution:** Check your internet connection for model download

**Issue: Images appear pixelated**
- **Solution:** This is expected for 64×64 resolution. Use images close to this size for best results

**Issue: Decoded image is distorted**
- **Solution:** Ensure the container image hasn't been resized or recompressed
- **Solution:** Use PNG format instead of JPEG

**Issue: Streamlit app won't start**
- **Solution:** Verify all dependencies are installed: `pip install -r requirements.txt`
- **Solution:** Check Python version (requires 3.8+)


---

## 👨‍💻 Author

**Varun Dubey**

- 🎓 AI / ML Enthusiast
- 📧 Email: [varundube99@gmail.com](mailto:varundube99@gmail.com)
- 💼 GitHub: [@Varundube99](https://github.com/Varundube99)

---

## 📜 License

This project is intended for **educational and research purposes**.

- ✅ Application code is open-source
- 🔒 Model weights are proprietary and intentionally excluded from this repository
- 📝 See individual file headers for specific licensing information

---

<div align="center">

**Made with ❤️ using Streamlit, TensorFlow, and Deep Learning**

⭐ **Star this repo if you find it helpful!** ⭐

[⬆ Back to Top](#-stegano-studio)

</div>
