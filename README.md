#### Stegano Studio

AI-Powered Image Steganography using Deep Learning



---



📌 Overview



Stegano Studio is a deep learning–based image steganography application that enables users to hide one image inside another and later reveal it with minimal visual distortion.



Unlike traditional techniques such as Least Significant Bit (LSB) manipulation, this project uses a neural autoencoder architecture trained end-to-end to embed and extract images in a visually imperceptible and robust manner.



The application is built using Streamlit for the frontend, while trained models are securely hosted on Hugging Face, ensuring strong separation between application code and proprietary model weights.



---



✨ Key Features



\- Hide a secret image inside a cover image

\- Reveal the hidden image with high fidelity

\- Deep learning–based autoencoder approach

\- Clean and interactive Streamlit UI

\- Secure model loading from Hugging Face (no models in GitHub)

\- Fast inference using TensorFlow / Keras



---



🧠 How It Works



The system consists of two trained neural networks:



 Encoder

\- Takes two inputs:

&nbsp; - Secret image

&nbsp; - Cover image

\- Outputs a container image that visually resembles the cover image while encoding the secret.



 Decoder

\- Takes the container image as input

\- Reconstructs the hidden secret image



Both networks are trained jointly to minimize visual distortion while preserving accurate recovery of the secret image.



---



🏗️ Architecture



Secret Image + Cover Image → Encoder → Container Image → Decoder → Revealed Image



\- Input size: 64 × 64 × 3

\- Framework: TensorFlow / Keras

\- Model format: .keras



---



🖥️ Application Pages



 Home

\- Project overview

\- Model explanation

\- Limitations and future work



 Hide Image

\- Upload secret image

\- Upload cover image

\- Generate container image

\- Download result as PNG



 Reveal Image

\- Upload container image

\- Decode and reveal secret image

\- Download revealed image



---



🔐 Model Security \& Deployment



To protect originality and trained weights:



\- Models are NOT stored in the GitHub repository

\- Models are hosted privately on Hugging Face

\- Access is controlled via Hugging Face access tokens

\- Tokens are managed using Streamlit Secrets



This ensures:

\- Open-source application code

\- Private and protected model weights

\- No accidental leakage of intellectual property



---



📁 Project Structure



.

├── app.py

├── requirements.txt

├── README.md

└── .streamlit/

&nbsp;   └── secrets.toml



---



⚙️ Installation \& Local Setup



 Clone the repository



git clone https://github.com/Varundube99/SteganoStudio.git  

cd your-repo-name



 Install dependencies



pip install -r requirements.txt



 Configure Hugging Face token



▶️ Run the Application



You can access the live deployed version of \*\*Stegano Studio\*\* here:



https://steganostudio.streamlit.app/



No local setup is required for basic usage.  

Simply open the link, upload images, and start hiding or revealing secrets.

---



☁️ Streamlit Cloud Deployment



1\. Connect the GitHub repository

2\. Add HF\_TOKEN under App → Settings → Secrets

3\. Deploy the app



Models are downloaded from Hugging Face at runtime and cached for performance.



---



⚠️ Limitations



\- Model trained only on 64×64 images

\- Output may appear pixelated when upscaled

\- Not robust to heavy JPEG compression

\- Avoid resizing or recompressing container images

\- Best results with PNG images



---



🚀 Future Work



\- Training on higher resolutions (128×128, 256×256)

\- Compression-resistant steganography

\- Noise-aware loss functions

\- Batch processing support

\- Improved robustness to image transformations



---



📚 Research Background



This project is inspired by research in neural steganography and autoencoder-based image embedding.



Traditional rule-based steganography techniques are fragile, while neural approaches learn optimal hiding strategies directly from data.



---



🧑‍💻 Author



Varun Dubey  

AI / ML Enthusiast  

Email: mailto:varundube99@gmail.com




---



📜 License



This project is intended for educational and research purposes.

Model weights are proprietary and intentionally excluded from this repository.





