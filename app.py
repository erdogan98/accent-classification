import os
import glob
import streamlit as st
import yt_dlp

from speechbrain.inference.classifiers import EncoderClassifier as LangIDClassifier
from speechbrain.pretrained import EncoderClassifier as AccentClassifier


# Caches the downloaded audio so you don't re-download the same URL repeatedly
@st.cache_data(show_spinner=False)
def download_extract_audio(url: str) -> str:
    output_dir = "./downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    wav_files = sorted(
        glob.glob(f"{output_dir}/*.wav"),
        key=os.path.getctime,
        reverse=True
    )
    if not wav_files:
        raise FileNotFoundError("No .wav file was found.")
    return wav_files[0]


# Load & cache models once
@st.cache_resource(show_spinner=False)
def load_models():
    lang_model = LangIDClassifier.from_hparams(
        source="speechbrain/lang-id-voxlingua107-ecapa",
        savedir="tmp/langid"
    )
    accent_model = AccentClassifier.from_hparams(
        source="Jzuluaga/accent-id-commonaccent_ecapa",
        savedir="tmp/accentid"
    )
    return lang_model, accent_model


def main():
    st.title("🌐 Language & Accent Identifier")

    url = st.text_input("Video URL", placeholder="https://www.youtube.com/…")
    if st.button("Analyze"):
        if not url:
            st.error("Please enter a video URL.")
            return

        with st.spinner("Downloading & extracting audio…"):
            try:
                wav_path = download_extract_audio(url)
            except Exception as e:
                st.error(f"Audio extraction failed: {e}")
                return

        lang_model, accent_model = load_models()

        with st.spinner("Detecting language…"):
            signal = lang_model.load_audio(wav_path)
            pred = lang_model.classify_batch(signal)
            detected = pred[3][0]  # e.g. "en: English"
            lang_code = detected.split(":")[0]

        st.markdown(f"**Detected language:** {detected}")

        if lang_code == "en":
            with st.spinner("Classifying accent…"):
                out_prob, score, index, label = accent_model.classify_file(wav_path)
            st.success(
                f"Predicted accent: **{label[0]}**  "
                f"(confidence {score.item():.3f})"
            )
        else:
            st.warning("Non-English audio detected — skipping accent classification.")

    st.markdown("---")
    st.markdown("Made by Erdoğan Kervanlı for REMWaste AI Agent Solutions Engineer Candidate Challenge")


if __name__ == "__main__":
    main()
