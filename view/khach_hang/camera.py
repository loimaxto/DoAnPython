import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import (
    QCamera,
    QCameraDevice,
    QImageCapture,
    QMediaCaptureSession,
    QMediaDevices, #Import QMediaDevices
)
from PyQt6.QtMultimediaWidgets import QVideoWidget

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera App")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Camera preview widget
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Capture button
        self.capture_button = QPushButton("Capture")
        self.capture_button.clicked.connect(self.capture_image)
        self.layout.addWidget(self.capture_button)

        # Image display label
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        # Camera setup
        self.camera = None
        self.image_capture = None
        self.media_capture_session = None
        self.setup_camera()

    def setup_camera(self):
        media_devices = QMediaDevices() #create an instance of QMediaDevices
        available_cameras = media_devices.videoInputs() #use the instance to get the video inputs.
        if not available_cameras:
            print("No cameras available.")
            return

        camera_device = available_cameras[0]
        self.camera = QCamera(camera_device)

        self.image_capture = QImageCapture(self.camera)

        self.media_capture_session = QMediaCaptureSession()
        self.media_capture_session.setCamera(self.camera)
        self.media_capture_session.setImageCapture(self.image_capture)
        self.media_capture_session.setVideoOutput(self.video_widget)

        self.camera.start()

    def capture_image(self):
        if self.image_capture:
            self.image_capture.capture()
            self.image_capture.imageCaptured.connect(self.display_image)

    def display_image(self, id, image):
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap.scaledToWidth(self.image_label.width()))

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())