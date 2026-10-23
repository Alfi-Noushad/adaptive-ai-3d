from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ClassificationResult:
    category: str
    confidence: float
    all_scores: Dict[str, float] = field(default_factory=dict)


DEFAULT_CATEGORIES = [
    "chair",
    "laptop",
    "phone",
    "water bottle",
    "table",
    "keyboard",
    "mouse",
    "backpack",
    "book",
]


class ClipZeroShotClassifier:
    def __init__(
        self, model_name: Optional[str] = None, categories: Optional[List[str]] = None
    ):
        self.model_name = model_name or "openai/clip-vit-base-patch32"
        self.categories = categories or DEFAULT_CATEGORIES
        self._model = None
        self._processor = None

    def _lazy_load(self):
        if self._model is None:
            from transformers import CLIPModel, CLIPProcessor

            self._model = CLIPModel.from_pretrained(self.model_name)
            self._processor = CLIPProcessor.from_pretrained(self.model_name)
            self._model.eval()

    def classify(self, image: Any) -> ClassificationResult:
        self._lazy_load()
        import torch

        prompts = [f"a photo of a {c}" for c in self.categories]
        inputs = self._processor(
            text=prompts, images=image, return_tensors="pt", padding=True
        )
        with torch.no_grad():
            outputs = self._model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).squeeze(0).tolist()

        all_scores = {cat: float(p) for cat, p in zip(self.categories, probs)}
        best_category = max(all_scores, key=all_scores.get)
        best_confidence = all_scores[best_category]

        return ClassificationResult(
            category=best_category,
            confidence=best_confidence,
            all_scores=all_scores,
        )


class StubImageClassifier:
    def __init__(
        self,
        forced_category: Optional[str] = None,
        categories: Optional[List[str]] = None,
    ):
        self.categories = categories or DEFAULT_CATEGORIES
        self.forced_category = forced_category or self.categories[0]

    def classify(self, image: Any) -> ClassificationResult:
        category = self.forced_category
        scores = {
            c: (0.9 if c == category else 0.1 / (len(self.categories) - 1))
            for c in self.categories
        }
        return ClassificationResult(
            category=category, confidence=scores[category], all_scores=scores
        )


if __name__ == "__main__":
    clf = StubImageClassifier(forced_category="chair")
    result = clf.classify(image=None)
    print("Stub result:", result)
