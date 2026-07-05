import cv2
import numpy as np

# Défaut              Algorithme                  Logique
# Rayure (Kratzer)    Filtre Canny Une rayure = contour fort et linéaire
# Tache (Fleck)       Seuillage (Threshold) Une tache = zone anormalement claire/sombre
# Texture (Strukturfehler) Variance locale Zone rugueuse = variance élevée


# 1er Fall : Rayure (Kratzer)    Filtre Canny Une rayure = contour fort et linéaire
# 1. Charge test_images/scratch/scratch_001.png
# image = cv2.imread ("test_images/test_images/scratch/scratch_001.png")
image = cv2.imread("test_images/test_images/ok/ok_001.png")
image1 = image.copy()  # copie pour affichage final
# 2. Convertit en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. Applique le filtre Canny
edge = cv2.Canny(gray, 50, 150)
# 5. Décision :
# 6. Afficher le verdict sur l'image avec cv2.putText()
# → texte rouge si NICHT OK, vert si OK
SEUIL_KRATZER = 100  # pixels blancs
if np.sum(edge > 0) > SEUIL_KRATZER:
    résultat = "NICHT OK — Kratzer erkannt"
    image_verdict = cv2.putText(image, f"{résultat}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
else:
    résultat = "OK"
    image_verdict = cv2.putText(image, f"{résultat}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# 4. Affiche côte à côte :
canny_bgr = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
combined  = np.hstack([image1, canny_bgr, image_verdict])   
cv2.imshow("Original | Canny | Verdict", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 5. Affiche dans le terminal le nombre de pixels blancs détectés
print (f"nombre de pixels blancs détectés → {np.sum(edge > 0)}")
# Pixel = 0    → noir  → pas de contour détecté
# Pixel = 255  → blanc → contour détecté (rayure, bord)
# # edges est un tableau NumPy de valeurs 0 ou 255
# # edges > 0 crée un tableau de booléens
# edges = [0, 255, 0, 0, 255, 255, 0]
# edges > 0  →  [False, True, False, False, True, True, False]
# # En NumPy, True = 1 et False = 0
# # np.sum() additionne tous les 1
# np.sum([False, True, False, False, True, True, False])
# →  0 + 1 + 0 + 0 + 1 + 1 + 0
# →  3


# 7. Afficher côte à côte original | Canny | image avec verdict