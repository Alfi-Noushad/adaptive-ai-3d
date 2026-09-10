from dataclasses import dataclass, asdict
from typing import Any, Dict

import cv2
import numpy as np


@dataclass
class ImageEvaluationResult:
    resolution: float
    blur: float
    noise: float
    lighting: float
    background_complexity: float
    occlusion: float
    object_size: float
    object_visibility: float
    overall_score: float


class ImageEvaluator:
    def __init__(self):
        self._yolo = None

    # ---------------------------------------------------------
    # Load image
    # ---------------------------------------------------------

    def _load_image(self, image: Any) -> np.ndarray:
        if isinstance(image, np.ndarray):
            return image

        if isinstance(image, str):
            img = cv2.imread(image)

            if img is None:
                raise ValueError(f"Could not load image: {image}")

            return img

        try:
            from PIL import Image

            if isinstance(image, Image.Image):
                image = image.convert("RGB")
                image = np.array(image)

                return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        except ImportError:
            pass

        raise TypeError("Input must be a file path, NumPy array, or PIL Image.")

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    @staticmethod
    def _clamp(value: float) -> float:
        return float(max(0.0, min(100.0, value)))

    # ---------------------------------------------------------
    # 1. Resolution
    # ---------------------------------------------------------

    def evaluate_resolution(self, image: np.ndarray) -> float:
        height, width = image.shape[:2]

        pixels = width * height

        if pixels < 100_000:
            score = 20

        elif pixels < 300_000:
            score = 40

        elif pixels < 700_000:
            score = 60

        elif pixels < 1_500_000:
            score = 80

        else:
            score = 100

        return float(score)

    # ---------------------------------------------------------
    # 2. Blur
    # ---------------------------------------------------------

    def evaluate_blur(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        variance = cv2.Laplacian(gray, cv2.CV_64F).var()

        if variance < 20:
            score = 10

        elif variance < 50:
            score = 30

        elif variance < 100:
            score = 50

        elif variance < 200:
            score = 70

        elif variance < 500:
            score = 85

        else:
            score = 100

        return float(score)

    # ---------------------------------------------------------
    # 3. Noise
    # ---------------------------------------------------------

    def evaluate_noise(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        noise = gray - blurred

        noise_level = np.std(noise)

        if noise_level < 3:
            score = 100

        elif noise_level < 6:
            score = 90

        elif noise_level < 10:
            score = 75

        elif noise_level < 15:
            score = 55

        elif noise_level < 25:
            score = 30

        else:
            score = 10

        return float(score)

    # ---------------------------------------------------------
    # 4. Lighting
    # ---------------------------------------------------------

    def evaluate_lighting(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        brightness = np.mean(gray)

        dark_pixels = np.mean(gray < 30)

        bright_pixels = np.mean(gray > 225)

        # Ideal average brightness is around 120–150.

        brightness_difference = abs(brightness - 135)

        brightness_score = max(0, 100 - brightness_difference * 0.8)

        dark_penalty = dark_pixels * 100

        bright_penalty = bright_pixels * 100

        score = brightness_score - dark_penalty - bright_penalty

        return self._clamp(score)

    # ---------------------------------------------------------
    # 5. Background Complexity
    # ---------------------------------------------------------

    def evaluate_background_complexity(self, image: np.ndarray) -> float:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 100, 200)

        edge_density = np.mean(edges > 0)

        # More edges usually means a more complex scene.

        if edge_density < 0.02:
            score = 100

        elif edge_density < 0.05:
            score = 85

        elif edge_density < 0.10:
            score = 70

        elif edge_density < 0.20:
            score = 50

        elif edge_density < 0.30:
            score = 30

        else:
            score = 10

        return float(score)

    # ---------------------------------------------------------
    # YOLO
    # ---------------------------------------------------------

    def _load_yolo(self):
        if self._yolo is None:
            try:
                from ultralytics import YOLO

                self._yolo = YOLO("yolo11n.pt")

            except ImportError:
                raise ImportError(
                    "Ultralytics is required for "
                    "object-related evaluation.\n\n"
                    "Install it using:\n"
                    "pip install ultralytics"
                )

    # ---------------------------------------------------------
    # Detect objects
    # ---------------------------------------------------------

    def _detect_objects(self, image: np.ndarray):
        self._load_yolo()

        results = self._yolo(image, verbose=False)

        objects = []

        height, width = image.shape[:2]

        image_area = height * width

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                box_width = x2 - x1
                box_height = y2 - y1

                area = box_width * box_height

                area_ratio = area / image_area

                objects.append(
                    {
                        "confidence": confidence,
                        "box": (x1, y1, x2, y2),
                        "area_ratio": area_ratio,
                    }
                )

        return objects

    # ---------------------------------------------------------
    # 6. Object Size
    # ---------------------------------------------------------

    def evaluate_object_size(self, objects) -> float:
        if not objects:
            return 0.0

        largest_object = max(obj["area_ratio"] for obj in objects)

        percentage = largest_object * 100

        if percentage < 1:
            score = 10

        elif percentage < 3:
            score = 30

        elif percentage < 8:
            score = 50

        elif percentage < 15:
            score = 70

        elif percentage < 30:
            score = 85

        else:
            score = 100

        return float(score)

    # ---------------------------------------------------------
    # 7. Object Visibility
    # ---------------------------------------------------------

    def evaluate_object_visibility(self, objects) -> float:
        if not objects:
            return 0.0

        confidences = [obj["confidence"] for obj in objects]

        average_confidence = np.mean(confidences)

        return self._clamp(average_confidence * 100)

    # ---------------------------------------------------------
    # Calculate IoU
    # ---------------------------------------------------------

    @staticmethod
    def _iou(box_a, box_b):
        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        x1 = max(ax1, bx1)
        y1 = max(ay1, by1)

        x2 = min(ax2, bx2)
        y2 = min(ay2, by2)

        intersection = max(0, x2 - x1) * max(0, y2 - y1)

        area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)

        area_b = max(0, bx2 - bx1) * max(0, by2 - by1)

        union = area_a + area_b - intersection

        if union == 0:
            return 0

        return intersection / union

    # ---------------------------------------------------------
    # 8. Occlusion
    # ---------------------------------------------------------

    def evaluate_occlusion(self, objects) -> float:
        if len(objects) <= 1:
            if not objects:
                return 0.0

            return self._clamp(objects[0]["confidence"] * 100)

        overlaps = []

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                overlap = self._iou(objects[i]["box"], objects[j]["box"])

                overlaps.append(overlap)

        if not overlaps:
            return 100.0

        average_overlap = np.mean(overlaps)

        score = 100 - (average_overlap * 100)

        return self._clamp(score)

    # ---------------------------------------------------------
    # Complete Evaluation
    # ---------------------------------------------------------

    def evaluate(self, image: Any) -> ImageEvaluationResult:
        image = self._load_image(image)

        resolution = self.evaluate_resolution(image)

        blur = self.evaluate_blur(image)

        noise = self.evaluate_noise(image)

        lighting = self.evaluate_lighting(image)

        background_complexity = self.evaluate_background_complexity(image)

        # Object-based metrics

        objects = self._detect_objects(image)

        object_size = self.evaluate_object_size(objects)

        object_visibility = self.evaluate_object_visibility(objects)

        occlusion = self.evaluate_occlusion(objects)

        # Overall score

        scores = [
            resolution,
            blur,
            noise,
            lighting,
            background_complexity,
            occlusion,
            object_size,
            object_visibility,
        ]

        overall_score = np.mean(scores)

        return ImageEvaluationResult(
            resolution=round(resolution, 2),
            blur=round(blur, 2),
            noise=round(noise, 2),
            lighting=round(lighting, 2),
            background_complexity=round(background_complexity, 2),
            occlusion=round(occlusion, 2),
            object_size=round(object_size, 2),
            object_visibility=round(object_visibility, 2),
            overall_score=round(overall_score, 2),
        )


# =============================================================
# Example
# =============================================================

if __name__ == "__main__":
    evaluator = ImageEvaluator()

    result = evaluator.evaluate("blur.jpg")

    print("\nImage Evaluation")
    print("========================")

    result_dict = asdict(result)

    for name, score in result_dict.items():
        print(f"{name:25s}: {score:.2f}")
