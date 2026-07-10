# Détection de couleur (Farbfehler)
'''Exemples réels chez DRÄXLMAIER :

Zone décolorée sur plastique noir → teinte brunâtre/grisâtre
Tache de peinture mauvaise couleur
Variation de teinte entre 2 zones
Couleur référence (surface OK) : BGR = (60, 60, 60)
Couleur zone suspecte          : BGR = (60, 85, 60)
                                              ↑
                              canal vert trop élevé = déviation
Différence = |85 - 60| = 25 → au-dessus du seuil → Farbfehler

En OpenCV — espace HSV

On travaille en HSV (Hue, Saturation, Value) plutôt qu'en BGR car :

H (Teinte) — la vraie couleur (rouge, vert, bleu...)
S (Saturation) — intensité de la couleur
V (Luminosité) — clarté
'''

import cv2
import numpy as np

# Référence couleur surface saine (à calibrer)
# REF_HUE        = 0      # teinte neutre (gris = pas de teinte)
# REF_SATURATION = 0     # saturation très faible (surface grise)
# SEUIL_HUE      = 1     # déviation de teinte tolérée
# SEUIL_SAT      = 10     # déviation de saturation tolérée
SEUIL_MAX_SAT  = 50     # saturation maximale tolérée

def detect_farbfehler(image):
    """
    Detect color deviation defects using HSV color space.
    Args:
        image: BGR image (numpy array)
    Returns:
        dict with keys: defect_type, detected, hue_diff, sat_diff, verdict
    """
    # 1. Convertir en HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # # 2. Calculer la moyenne HSV de toute la zone
    # mean_h, mean_s, mean_v = cv2.mean(hsv)[:3]  # On ne prend que H, S, V

    # # 3. Calculer la différence avec la référence
    # hue_diff = abs (mean_h - REF_HUE)
    # sat_diff = abs (mean_s - REF_SATURATION)

    #  # 4. Décision :
    # detected = hue_diff > SEUIL_HUE or sat_diff > SEUIL_SAT

    # 2. Extraire canal S (saturation) uniquement
    s_channel = hsv[:, :, 1]
    # 3. Valeur maximale de saturation dans l'image
    max_saturation = float(np.max(s_channel))
    mean_saturation = float(np.mean(s_channel))
 
    # 4. Décision basée sur le maximum
    detected = max_saturation > SEUIL_MAX_SAT  # pixel le plus saturé

    # 5. Retourner le dict :

    return {
        "defect_type": "Farbfehler",
        "detected": detected,
        "max_sat": round(max_saturation, 2),
        "mean_sat": round(mean_saturation, 2),
        "verdict": "NICHT OK - Farbfehler erkannt" if detected else "OK"
    }

if __name__ == "__main__":
    for name, path in [
        ("OK",           "test_images/ok/ok_001.png"),
        ("Color Defect", "test_images/color_defect/color_defect_001.png"),
    ]:
        img = cv2.imread(path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        s   = hsv[:, :, 1]
        print(f"{name:<15} → max_S={np.max(s):.2f}  mean_S={np.mean(s):.2f}")

# if __name__ == "__main__":
#     for name, path in [
#         ("OK",           "test_images/ok/ok_001.png"),
#         ("Color Defect", "test_images/color_defect/color_defect_001.png"),
#     ]:
#         img = cv2.imread(path)
#         hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#         mean_h, mean_s, mean_v, _ = cv2.mean(hsv)
#         print(f"{name:<15} → H={mean_h:.2f}  S={mean_s:.2f}  V={mean_v:.2f}")

    print("Surface OK   :", detect_farbfehler(cv2.imread("test_images/ok/ok_001.png")))
    print("Surface Color Defect :", detect_farbfehler(cv2.imread("test_images/color_defect/color_defect_001.png")))