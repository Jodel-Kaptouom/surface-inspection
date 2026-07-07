import os
import cv2
import numpy as np

# Défaut              Algorithme                  Logique
# Rayure (Kratzer)    Filtre Canny Une rayure = contour fort et linéaire
# Tache (Fleck)       Seuillage (Threshold) Une tache = zone anormalement claire/sombre
# Texture (Strukturfehler) Variance locale Zone rugueuse = variance élevée

# Zusammenfassung aller Lösungen : detect_kratzer, detect_fleck, detect_strukturfehler

SEUIL_KRATZER = 100
SEUIL_FLECK   = 500
SEUIL_STRUCT  = 200
BLOCK_SIZE    = 16


def detect_kratzer(image):
    """Detect scratch defects using Canny edge detection."""
    gray         = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges        = cv2.Canny(gray, 50, 150)
    white_pixels = int(np.sum(edges > 0))
    detected     = white_pixels > SEUIL_KRATZER
    return {
        "defect_type": "Kratzer",
        "detected":    detected,
        "pixels":      white_pixels,
        "verdict":     "NICHT OK - Kratzer erkannt" if detected else "OK"
    }


def detect_fleck(image):
    """Detect spot defects using binary thresholding."""
    gray         = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh    = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    white_pixels = int(np.sum(thresh > 0))
    detected     = white_pixels > SEUIL_FLECK
    return {
        "defect_type": "Fleck",
        "detected":    detected,
        "pixels":      white_pixels,
        "verdict":     "NICHT OK - Fleck erkannt" if detected else "OK"
    }


def detect_strukturfehler(image):
    """Detect texture defects using local variance analysis."""
    gray      = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    BlocError = 0

    for y in range(0, gray.shape[0], BLOCK_SIZE):
        for x in range(0, gray.shape[1], BLOCK_SIZE):
            region   = gray[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
            _, stddev = cv2.meanStdDev(region)
            variance  = stddev[0][0] ** 2
            if variance > SEUIL_STRUCT:
                BlocError += 1

    # Décision APRES la boucle
    detected = BlocError > 0
    return {
        "defect_type":  "Strukturfehler",
        "detected":     detected,
        "blockserror":  BlocError,
        "verdict":      "NICHT OK - Strukturfehler erkannt" if detected else "OK"
    }


# ---------------------------------------------------------------------------
# Test des 3 fonctions
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    tests = [
        ("test_images/test_images/scratch/scratch_001.png",        detect_kratzer),
        ("test_images/test_images/ok/ok_001.png",                  detect_kratzer),
        ("test_images/test_images/spot/spot_001.png",               detect_fleck),
        ("test_images/test_images/ok/ok_001.png",                  detect_fleck),
        ("test_images/test_images/texture_defect/texture_defect_001.png", detect_strukturfehler),
        ("test_images/test_images/ok/ok_001.png",                  detect_strukturfehler),
    ]

    for path, func in tests:
        image  = cv2.imread(path)
        result = func(image)
        print(f"{os.path.basename(path):<30} → {result['verdict']}")