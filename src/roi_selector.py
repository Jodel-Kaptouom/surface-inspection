import cv2 
import json
import os
image = cv2.imread("test_images/test_images/ok/ok_001.png")
# cv2.imshow("surface inspection", image)
# n = int (input ("combien de ROI voulez-vous sélectionner ? "))
# for i in range (n):
#     x,y,w,h = cv2.selectROIs("surface inspection", image)
#     print (f"ROI sélectionné → x_{i}={x}, y_{i}={y}, w_{i}={w}, h_{i}={h}")
#     ROI = image[y:y+h, x:x+w]
#     cv2.imshow(f"ROI{i}", ROI)
rois = cv2.selectROIs("Surface Inspection", image)

# 3. Afficher toutes les coordonnées + découper chaque ROI
rois_data = []
for i, (x, y, w, h) in enumerate(rois):
    print(f"ROI {i+1} → x={x}, y={y}, w={w}, h={h}")
    roi = image[y:y+h, x:x+w]
    cv2.imshow(f"ROI_{i+1}", roi)
     # Ajouter à la liste — pas encore écrire
    rois_data.append({
        "id":  i + 1,
        "x":   int(x),
        "y":   int(y),
        "w":   int(w),
        "h":   int(h)
    })
# 4. Écrire UNE SEULE FOIS après la boucle
os.makedirs("results", exist_ok=True)
with open("results/rois.json", "w") as f:
    json.dump(rois_data, f, indent=4)

print(f"\n✅ ROIs sauvegardées → results/rois.json")
cv2.waitKey(0)
cv2.destroyAllWindows()