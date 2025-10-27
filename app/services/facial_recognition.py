"""
Facial Recognition Service
Handles face detection and recognition in images and videos
"""
import logging
from pathlib import Path

import cv2

logger = logging.getLogger(__name__)


class FacialRecognitionService:
    """Service for detecting and recognizing faces in images and videos"""

    def __init__(self, cascade_path=None, confidence_threshold=0.5):
        """
        Initialize the facial recognition service

        Args:
            cascade_path: Path to Haar Cascade XML file
            confidence_threshold: Minimum confidence for face detection
        """
        self.confidence_threshold = confidence_threshold
        self.face_cascade = None

        if cascade_path and Path(cascade_path).exists():
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            logger.info(f"Loaded face cascade from {cascade_path}")
        else:
            # Try to load default OpenCV cascade
            try:
                self.face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                )
                logger.info("Loaded default face cascade")
            except Exception as e:
                logger.error(f"Failed to load face cascade: {e}")

    def detect_faces_in_image(self, image_path):
        """
        Detect faces in a single image

        Args:
            image_path: Path to the image file

        Returns:
            dict: Detection results with faces and annotated image path
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")

            # Convert to grayscale for detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            # Draw rectangles around faces
            face_data = []
            for i, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(
                    image, f'Face {i+1}', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )

                face_data.append({
                    'face_id': i + 1,
                    'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                    'confidence': 1.0  # Haar cascades don't provide confidence scores
                })

            # Save annotated image
            output_path = Path(image_path).parent / f"annotated_{Path(image_path).name}"
            cv2.imwrite(str(output_path), image)

            return {
                'success': True,
                'faces_detected': len(faces),
                'faces': face_data,
                'annotated_image': str(output_path),
                'original_image': str(image_path)
            }

        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return {
                'success': False,
                'error': str(e),
                'faces_detected': 0
            }

    def detect_faces_in_video(self, video_path, frame_skip=5):
        """
        Detect faces in a video file

        Args:
            video_path: Path to the video file
            frame_skip: Process every Nth frame

        Returns:
            dict: Detection results with face counts per frame
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                raise ValueError(f"Could not open video: {video_path}")

            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Setup output video
            output_path = Path(video_path).parent / f"annotated_{Path(video_path).name}"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

            frame_results = []
            frame_count = 0
            total_faces = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Process every Nth frame
                if frame_count % frame_skip == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(
                        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                    )

                    # Draw rectangles
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    if len(faces) > 0:
                        frame_results.append({
                            'frame': frame_count,
                            'timestamp': frame_count / fps,
                            'faces_count': len(faces)
                        })
                        total_faces += len(faces)

                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()

            return {
                'success': True,
                'total_frames': total_frames,
                'processed_frames': len(frame_results),
                'total_faces_detected': total_faces,
                'frames_with_faces': frame_results,
                'annotated_video': str(output_path),
                'original_video': str(video_path)
            }

        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def is_available(self):
        """Check if the service is properly initialized"""
        return self.face_cascade is not None
