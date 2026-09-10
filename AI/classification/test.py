from PIL import Image
from classification import ClipZeroShotClassifier

clf = ClipZeroShotClassifier()
image = Image.open("my_object.jpg").convert("RGB")
result = clf.classify(image)
print(result.category, result.confidence)
