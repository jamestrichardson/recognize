"""
Object Detection Service
Handles object detection in images and videos using YOLO or other models
"""
import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class ObjectDetectionService:
    """Service for detecting objects in images and videos"""

    def __init__(self, weights_path=None, config_path=None, names_path=None,
                 confidence_threshold=0.5, nms_threshold=0.4):
        """
        Initialize the object detection service

        Args:
            weights_path: Path to YOLO weights file
            config_path: Path to YOLO config file
            names_path: Path to class names file
            confidence_threshold: Minimum confidence for detection
            nms_threshold: Non-maximum suppression threshold
        """
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.net = None
        self.classes = []
        self.output_layers = []

        # Try to load YOLO model if paths provided
        if all([weights_path, config_path, names_path]):
            self._load_yolo_model(weights_path, config_path, names_path)

    def _load_yolo_model(self, weights_path, config_path, names_path):
        """Load YOLO model from files"""
        try:
            if Path(weights_path).exists() and Path(config_path).exists():
                self.net = cv2.dnn.readNet(str(weights_path), str(config_path))
                layer_names = self.net.getLayerNames()
                self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
                logger.info("Loaded YOLO model successfully")

            if Path(names_path).exists():
                with open(names_path, 'r') as f:
                    self.classes = [line.strip() for line in f.readlines()]
                logger.info(f"Loaded {len(self.classes)} object classes")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")

    def detect_objects_in_image(self, image_path):
        """
        Detect objects in a single image

        Args:
            image_path: Path to the image file

        Returns:
            dict: Detection results with objects and annotated image path
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")

            height, width = image.shape[:2]

            # Create blob and perform detection
            blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            outputs = self.net.forward(self.output_layers)

            # Process detections
            boxes = []
            confidences = []
            class_ids = []

            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > self.confidence_threshold:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Apply non-maximum suppression
            indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)

            # Draw boxes and collect results
            detected_objects = []
            if len(indices) > 0:
                for i in indices.flatten():
                    x, y, w, h = boxes[i]
                    label = self.classes[class_ids[i]] if class_ids[i] < len(self.classes) else "Unknown"
                    confidence = confidences[i]

                    # Draw bounding box
                    color = (0, 255, 0)
                    cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(image, f'{label} {confidence:.2f}', (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    detected_objects.append({
                        'class': label,
                        'confidence': confidence,
                        'bbox': {'x': x, 'y': y, 'width': w, 'height': h}
                    })

            # Save annotated image
            output_path = Path(image_path).parent / f"annotated_{Path(image_path).name}"
            cv2.imwrite(str(output_path), image)

            return {
                'success': True,
                'objects_detected': len(detected_objects),
                'objects': detected_objects,
                'annotated_image': str(output_path),
                'original_image': str(image_path)
            }

        except Exception as e:
            logger.error(f"Error detecting objects: {e}")
            return {
                'success': False,
                'error': str(e),
                'objects_detected': 0
            }

    def detect_objects_in_video(self, video_path, frame_skip=5):
        """
        Detect objects in a video file

        Args:
            video_path: Path to the video file
            frame_skip: Process every Nth frame

        Returns:
            dict: Detection results with object counts per frame
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
            object_summary = {}

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Process every Nth frame
                if frame_count % frame_skip == 0:
                    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
                    self.net.setInput(blob)
                    outputs = self.net.forward(self.output_layers)

                    boxes = []
                    confidences = []
                    class_ids = []

                    for output in outputs:
                        for detection in output:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]

                            if confidence > self.confidence_threshold:
                                center_x = int(detection[0] * width)
                                center_y = int(detection[1] * height)
                                w = int(detection[2] * width)
                                h = int(detection[3] * height)
                                x = int(center_x - w / 2)
                                y = int(center_y - h / 2)

                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)

                    # Apply NMS
                    indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)

                    frame_objects = []
                    if len(indices) > 0:
                        for i in indices.flatten():
                            x, y, w, h = boxes[i]
                            label = self.classes[class_ids[i]] if class_ids[i] < len(self.classes) else "Unknown"

                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x, y-10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            frame_objects.append(label)
                            object_summary[label] = object_summary.get(label, 0) + 1

                    if frame_objects:
                        frame_results.append({
                            'frame': frame_count,
                            'timestamp': frame_count / fps,
                            'objects': frame_objects
                        })

                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()

            return {
                'success': True,
                'total_frames': total_frames,
                'processed_frames': len(frame_results),
                'object_summary': object_summary,
                'frames_with_objects': frame_results,
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
        return self.net is not None
