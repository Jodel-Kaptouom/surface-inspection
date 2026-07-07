import cv2
import numpy as np
import json
import os
import sys
sys.path.append(os.path.dirname(__file__))  # ajoute src/ au path
from defect_detector import detect_kratzer, detect_fleck, detect_strukturfehler

def load_image(path):
    """Charge et retourne une image BGR"""
    image = cv2.imread(path)
     # 2. Vérifier que l'image existe (image is None → erreur)
    if image is None:
        raise FileNotFoundError(f"Image non trouvee : {path}")
    return image 

def load_rois(path):
    """Charge et retourne la liste des ROIs depuis un fichier JSON"""
    # 1. Ouvrir le fichier JSON en lecture
    # 2. Charger le contenu avec json.load()
    with open (path, "r") as f:
        data = json.load(f)
    # 3. Retourner la liste
    return data

def run_inspection(image, rois):
    """
    Pour chaque ROI :
    - Extraire la zone de l'image
    - Lancer les 3 détecteurs
    - Collecter les résultats
    Retourne une liste de résultats
    """
    results = []

    for roi in rois:
        # 1. Extraire les coordonnées
        x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]

        # 2. Découper la zone (crop)
        region = image[y:y+h, x:x+w]

        # 3. Lancer les 3 détecteurs sur la région
        kratzer_result = detect_kratzer(region)
        fleck_result = detect_fleck(region)
        struktur_result = detect_strukturfehler(region)
        global_verdict ="NICHT OK" if ( kratzer_result["detected"] or fleck_result["detected"]   or struktur_result["detected"]) else "OK"

        # 4. Construire un dict résultat pour cette ROI :
        results.append({
               "roi_id":   roi["id"],
               "kratzer":  kratzer_result,
               "fleck":    fleck_result,
               "struktur":  struktur_result,
               "global":   global_verdict
           })
        # 5. Ajouter à results

    return results

def annotate_image(image, rois, results):
    """
    Dessine sur l'image :
    - Rectangle vert si ROI OK
    - Rectangle rouge si ROI NICHT OK
    - Verdict texte sur chaque ROI
    Retourne l'image annotée
    """
    for roi, result in zip(rois, results):
        x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]

        # Couleur selon verdict
        couleur = (0, 255, 0) if result["global"] == "OK" else (0, 0, 255)

        # Rectangle
        cv2.rectangle(image, (x, y), (x+w, y+h), couleur, 2)

        # Verdict texte
        cv2.putText(image,
                    f"ROI {roi['id']} - {result['global']}",
                    (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, couleur, 1)

    return image

def print_report(results):
    """Affiche le rapport complet dans le terminal"""
    print("\n--- Inspection Report ---")
    for result in results:
        roi_id = result["roi_id"]
        kratzer_verdict = result["kratzer"]["verdict"]
        fleck_verdict = result["fleck"]["verdict"]
        struktur_verdict = result["struktur"]["verdict"]
        global_verdict = result["global"]

        print(f"ROI {roi_id}:")
        print(f"  - Kratzer: {kratzer_verdict}")
        print(f"  - Fleck: {fleck_verdict}")
        print(f"  - Strukturfehler: {struktur_verdict}")
        print(f"  - Global Verdict: {global_verdict}\n")
    pass

if __name__ == "__main__":
    # 1. Charger l'image
    image = load_image("test_images/test_images/scratch/scratch_001.png")

    # 2. Charger les ROIs
    rois = load_rois("results/rois.json")

    # 3. Lancer l'inspection
    results = run_inspection(image, rois)

    # 4. Annoter l'image
    image_annote = annotate_image(image, rois, results)

    # 5. Afficher le rapport dans le terminal
    print_report(results)

    # 6. Afficher l'image annotée
    cv2.imshow("Surface — Inspection", image_annote)
    cv2.waitKey(0)
    cv2.destroyAllWindows()