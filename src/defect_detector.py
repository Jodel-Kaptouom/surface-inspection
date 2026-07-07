import cv2
import numpy as np

# Défaut              Algorithme                  Logique
# Rayure (Kratzer)    Filtre Canny Une rayure = contour fort et linéaire
# Tache (Fleck)       Seuillage (Threshold) Une tache = zone anormalement claire/sombre
# Texture (Strukturfehler) Variance locale Zone rugueuse = variance élevée


# 3te Fall : Texture (Strukturfehler) Variance locale Zone rugueuse = variance élevée
# Surface lisse  → pixels similaires entre eux → variance faible = Zone lisse :    [60, 61, 59, 62, 60]  → valeurs proches   → variance faible
# Surface rugueuse → pixels très différents    → variance élevée = Zone rugueuse : [60, 90, 30, 85, 25]  → valeurs dispersées → variance élevée

BLOCK_SIZE   = 4    # taille de chaque zone analysée
SEUIL_STRUCT = 200   # variance au-dessus = Strukturfehler

# 1. Charge test_images/texture_defect/texture_defect_001.png
image = cv2.imread("test_images/test_images/texture_defect/texture_defect_001.png")
# image = cv2.imread("test_images/test_images/ok/ok_001.png")
# 2. Convertit en niveaux de gris
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 3. Parcourt l'image par blocs de 16x16 pixels
#    → double boucle for sur y et x
#    → for y in range(0, h, BLOCK_SIZE):
#         for x in range(0, w, BLOCK_SIZE):
BlocError = 0
for y in range(0, gray.shape[0], BLOCK_SIZE):
    for x in range(0, gray.shape[1], BLOCK_SIZE):
        # 4. Pour chaque bloc :
        #    → extraire la région : region = gray[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
        region = gray[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
        #    → calculer variance avec cv2.meanStdDev()
        mean, stddev = cv2.meanStdDev(region)
        variance = stddev[0][0] ** 2
        #    → si variance > SEUIL_STRUCT → dessiner rectangle rouge sur l'image
        if variance > SEUIL_STRUCT:
            cv2.rectangle(image, (x, y), (x+BLOCK_SIZE, y+BLOCK_SIZE), (0, 0, 255), 1)
            BlocError += 1
# 5. Afficher l'image avec les zones suspectes encadrées en rouge
cv2.imshow("zones suspectes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 6. Afficher dans le terminal : nombre de blocs suspects
print("Nombre de blocs suspects :", BlocError)


