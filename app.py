import streamlit as st
import cv2
import av
import numpy as np
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration, VideoProcessorBase

# ==================================
# 1. Konfigurasi Halaman & CSS
# ==================================
st.set_page_config(
    page_title="YOLOv8 Real-Time Detection",
    page_icon="🚀",
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
    model = YOLO('yolov8n.pt')  # yolov8n.pt adalah model tercepat
    return model

model = load_yolo_model()


# ==================================
# 3. Class Processor Video dengan Optimasi
# ==================================
# Variabel untuk optimasi bisa diubah di sini
RESIZE_WIDTH = 640  # Perkecil gambar ke lebar 640 pixel
PROCESS_EVERY_N_FRAME = 3  # Hanya proses setiap 3 frame

class YoloVideoProcessor(VideoProcessorBase):
    def __init__(self, confidence_threshold: float):
        self.model = model
        self.confidence_threshold = confidence_threshold
        # (OPTIMASI) Variabel untuk menyimpan hasil terakhir dan menghitung frame
        self.last_results = None
        self.frame_count = 0

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """Menerima, memproses (dengan optimasi), dan mengembalikan frame."""
        image = frame.to_ndarray(format="bgr24")
        self.frame_count += 1

        # (OPTIMASI) Hanya proses jika ini adalah frame ke-N
        if self.frame_count % PROCESS_EVERY_N_FRAME == 0:
            # (OPTIMASI) Perkecil ukuran gambar sebelum deteksi
            h, w, _ = image.shape
            aspect_ratio = h / w
            new_h = int(RESIZE_WIDTH * aspect_ratio)
            resized_image = cv2.resize(image, (RESIZE_WIDTH, new_h))

            # Lakukan pelacakan objek pada gambar yang sudah dikecilkan
            results = self.model.track(
                source=resized_image,
                persist=True,
                conf=self.confidence_threshold,
                verbose=False,
                tracker="bytetrack.yaml"
            )

            # Simpan hasil terakhir
            self.last_results = results

            # Gambar hasil deteksi pada gambar ASLI (bukan yang di-resize)
            # Ini akan membuat bounding box diskalakan kembali ke ukuran asli
            annotated_frame = self.last_results[0].plot(img=image)
        else:
            # Jika frame ini dilewati, gunakan hasil deteksi terakhir
            if self.last_results:
                annotated_frame = self.last_results[0].plot(img=image)
            else:
                # Jika belum ada deteksi sama sekali, tampilkan frame asli
                annotated_frame = image

        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


# ==================================
# 4. Tata Letak & UI Aplikasi
# ==================================
col1, col2 = st.columns([0.4, 0.6], gap="large")

with col1:
    st.title("🚀 Deteksi Objek YOLOv8")
    st.markdown(
        "Aplikasi ini melakukan **deteksi objek** secara *real-time* "
        "dengan optimasi untuk performa lebih lancar."
    )
    st.divider()

    st.subheader("⚙️ Pengaturan")
    confidence_threshold = st.slider(
        "**Tingkat Kepercayaan**",
        0.0, 1.0, 0.5, 0.05
    )
    st.divider()
    st.info("ℹ️ **Panduan:**\n1. Izinkan browser mengakses kamera.\n2. Tekan **START** untuk memulai.")


with col2:
    st.subheader("🎥 Tampilan Kamera Real-Time")

    RTC_CONFIG = RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
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