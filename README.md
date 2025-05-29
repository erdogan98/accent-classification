# Accent ID Streamlit Application

A simple Streamlit app that downloads audio from a public video URL, identifies the language, and (if English) classifies the speaker's accent using SpeechBrain models.

## Note
When you first click the "Analyze" button Please wait couple of minutes(based on your internet speed) for the model weights to be downloaded.

## Requirements

* **Python 3.11**
* `Git` (optional, for cloning the repository)

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. **Create and activate a virtual environment**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running the App

```bash
streamlit run app.py
```

Paste any public video URL (e.g., YouTube/Loom/Vimeo) into the input field and click **Analyze**. The app will:

1. Download and extract audio to WAV.
2. Detect the language using the VoxLingua107 model.
3. If the language is English, classify the accent.

## Supported Accents

The accent recognition model can identify the following accents:

* African
* Australian
* Bermudian
* Canadian
* English (UK)
* Hong Kong
* Indian
* Irish
* Malaysian
* New Zealand
* Philippine
* Scottish
* Singaporean
* South Atlantic
* US (American)
* Welsh

## References

* [Accent ID CommonAccent ECAPA on Hugging Face](https://huggingface.co/Jzuluaga/accent-id-commonaccent_ecapa)
