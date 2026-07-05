import cv2
import numpy as np

# Défaut              Algorithme                  Logique
# Rayure (Kratzer)    Filtre Canny Une rayure = contour fort et linéaire
# Tache (Fleck)       Seuillage (Threshold) Une tache = zone anormalement claire/sombre
# Texture (Strukturfehler) Variance locale Zone rugueuse = variance élevée


# 2te Fall : # Tache (Fleck)       Seuillage (Threshold) Une tache = zone anormalement claire/sombre

# 1. Charge test_images/spot/spot_001.png
# image = cv2.imread("test_images/test_images/spot/spot_001.png")
image = cv2.imread("test_images/test_images/ok/ok_001.png")
image1 = image.copy()
# 2. Convertit en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 3. Applique un threshold
thresh_value = 100
_, thresh = cv2.threshold (gray, thresh_value, 255, cv2.THRESH_BINARY)
#    → cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
#    → pixels > 100 deviennent blancs, reste noir
# 4. Compte les pixels blancs
white_pixels = np.sum(gray > thresh_value)
# 5. Décision : si pixels > 500 → "NICHT OK — Fleck erkannt"
if white_pixels > 500:
    image_verdict = cv2.putText(image, "NICHT OK, Fleck erkannt", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
else: 
    image_verdict = cv2.putText(image, "OK — Keine Flecken", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# 6. Affiche côte à côte : Original | Threshold | Verdict
thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
combined = np.hstack([image1, thresh_bgr, image_verdict])
cv2.imshow("Original | Threshold | Verdict", combined)
# 7. Affiche le verdict dans le terminal 
print (f"verdict → { 'NICHT OK — Fleck erkannt' if white_pixels > 500 else 'OK — Keine Flecken' }")
cv2.waitKey(0)
cv2.destroyAllWindows()