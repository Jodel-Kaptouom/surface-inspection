import cv2

# Affiche une image de chaque catégorie
categories = {
    "good":    "test_images/mvtec/metal_nut/test/good/000.png",
    "scratch": "test_images/mvtec/metal_nut/test/scratch/000.png",
    "color":   "test_images/mvtec/metal_nut/test/color/000.png",
    "bent":    "test_images/mvtec/metal_nut/test/bent/000.png",
}

for name, path in categories.items():
    img = cv2.imread(path)
    cv2.imshow(f"MVTec — {name}", img)
    cv2.waitKey(0)

cv2.destroyAllWindows()