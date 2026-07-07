import cv2
import numpy as np

# Défaut              Algorithme                  Logique
# Rayure (Kratzer)    Filtre Canny Une rayure = contour fort et linéaire
# Tache (Fleck)       Seuillage (Threshold) Une tache = zone anormalement claire/sombre
# Texture (Strukturfehler) Variance locale Zone rugueuse = variance élevée

# Zusammenfassung aller Lösungen : detect_kratzer, detect_fleck, detect_strukturfehler

SEUIL_KRATZER = 100

def detect_kratzer(image):
    """
    Detect scratch defects (Kratzer) using Canny edge detection.
    
    Args:
        image: BGR image (numpy array)
    Returns:
        dict with keys: defect_type, detected, pixels, verdict
    """
    # 1. Convertir en gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2. Appliquer Canny (50, 150)
    edges = cv2.Canny(gray, 50,150)
    # 3. Compter pixels blancs
    white_pixels = np.sum (edges>0)
    # 4. Décision : detected = pixels > SEUIL_KRATZER
    if white_pixels > SEUIL_KRATZER:
        detected = True
        verdict = "NICHT OK- Kratzer erkannt"
    else:
        detected = False
        verdict = "OK"
    # 5. Retourner le dictionnaire :
    return {
        "defect_type": "Kratzer",
        "detected": detected,
        "pixels": white_pixels,
        "verdict": verdict
    }
    #    {
    #        "defect_type": "Kratzer",
    #        "detected":    True/False,
    #        "pixels":      nombre de pixels,
    #        "verdict":     "NICHT OK - Kratzer erkannt" ou "OK"
    #    }
# Test
def detect_fleck(image):
    """
    Detect spot defects (Fleck) using thresholding.
    
    Args:
        image: BGR image (numpy array)
    Returns:
        dict with keys: defect_type, detected, pixels, verdict
    """
    # 1. Convertir en gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2. Appliquer un seuillage adaptatif (ou global)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # 3. Compter pixels blancs
    white_pixels = np.sum(thresh > 0)
    # 4. Décision : detected = pixels > SEUIL_FLECK (à définir)
    SEUIL_FLECK = 500
    if white_pixels > SEUIL_FLECK:
        detected = True
        verdict = "NICHT OK - Fleck erkannt"
    else:
        detected = False
        verdict = "OK"
    # 5. Retourner le dictionnaire :
    return {
        "defect_type": "Fleck",
        "detected": detected,
        "pixels": white_pixels,
        "verdict": verdict
    }
def detect_strukturfehler(image):
    """
    Detect texture defects (Strukturfehler) using local variance.
    
    Args:
        image: BGR image (numpy array)
    Returns:
        dict with keys: defect_type, detected, pixels, verdict
    """
    BLOCK_SIZE   = 16    # taille de chaque zone analysée
    SEUIL_STRUCT = 200   # variance au-dessus = Strukturfehler
    # 1. Convertir en gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2. Calculer la variance locale (par exemple avec un filtre de Sobel ou un filtre de Laplacien)
    BlocError = 0
    for y in range (0, gray.shape[0], BLOCK_SIZE):
        for x in range (0, gray.shape[1], BLOCK_SIZE):
            region = gray[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
            mean, stddev = cv2.meanStdDev(region)
            variance = stddev[0][0] ** 2
            if variance > SEUIL_STRUCT:
                BlocError += 1
                detected = True
                verdict = "NICHT OK - Strukturfehler erkannt"
            else:
                detected = False
                verdict = "OK"
    # 3. Décision : detected = variance > SEUIL_STRUKTURFEHLER (à définir)
    return {
        "defect_type": "Strukturfehler",
        "detected": detected,
        "blockserror": int(BlocError),
        "verdict": verdict
    }
if __name__ == "__main__":
    image = cv2.imread("test_images/test_images/scratch/scratch_001.png")
    result = detect_kratzer(image)
    print(result)