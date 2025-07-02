import streamlit as st
import cv2
import av
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, VideoProcessorBase

# ==================================
# 1. Konfigurasi Halaman & CSS
# ==================================
st.set_page_config(
    page_title="YOLOv8 Real-Time Detection",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
div[data-testid="stVideo"] {
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    border: 2px solid #2c3e50;
}
</style>
""", unsafe_allow_html=True)


# ==================================
# 2. Memuat Model
# ==================================
@st.cache_resource
def load_yolo_model():
    """Memuat model YOLOv8 dan menyimpannya di cache."""
    model = YOLO('yolov8n.pt')
    return model

model = load_yolo_model()


# ==================================
# 3. Class Processor Video
# ==================================
class YoloVideoProcessor(VideoProcessorBase):
    def __init__(self, confidence_threshold: float):
        self.model = model
        self.confidence_threshold = confidence_threshold

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")
        results = self.model.track(
            source=image,
            persist=True,
            conf=self.confidence_threshold,
            verbose=False,
            tracker="bytetrack.yaml"
        )
        annotated_frame = results[0].plot()
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


# ==================================
# 4. Tata Letak & UI Aplikasi
# ==================================
col1, col2 = st.columns([0.4, 0.6], gap="large")

with col1:
    st.title("🤖 Deteksi Objek YOLOv8")
    st.markdown(
        "Aplikasi ini melakukan **deteksi dan pelacakan objek** secara *real-time*."
    )
    st.divider()

    st.subheader("⚙️ Pengaturan")
    confidence_threshold = st.slider(
        "**Tingkat Kepercayaan (Confidence)**",
        0.0, 1.0, 0.5, 0.05
    )
    st.divider()
    st.info("ℹ️ **Panduan:**\n1. Izinkan browser mengakses kamera.\n2. Tekan **START** untuk memulai.")


with col2:
    st.subheader("🎥 Tampilan Kamera Real-Time")

    # (FIX LENGKAP) Menambahkan server STUN dan TURN untuk koneksi paling andal
    RTC_CONFIG = RTCConfiguration({
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": ["turn:openrelay.metered.ca:80"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
            {
                "urls": ["turn:openrelay.metered.ca:443"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ]
    })

    webrtc_streamer(
        key="yolo-detection",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        video_processor_factory=lambda: YoloVideoProcessor(
            confidence_threshold=confidence_threshold
        ),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )