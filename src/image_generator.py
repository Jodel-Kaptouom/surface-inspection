"""
Surface Image Generator
=======================
Author : Baurel Kaptouom
Purpose: Generate synthetic automotive surface images for inspection testing.
         Simulates defect-free and defective surfaces (scratches, spots, texture anomalies).
         Used as test input for the defect detection pipeline.
"""

import cv2
import numpy as np
import os


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = "test_images"
IMAGE_SIZE = (512, 512)        # pixels (hauteur, largeur)
BASE_GRAY  = 60                # valeur grise de base (plastique noir mat)
NOISE_STD  = 6                 # intensité du bruit de texture


# ---------------------------------------------------------------------------
# Base surface generator
# ---------------------------------------------------------------------------

def generate_base_surface(size=IMAGE_SIZE, gray=BASE_GRAY, noise_std=NOISE_STD):
    """
    Generate a uniform surface with realistic texture noise.
    Simulates a dark plastic automotive interior component.
    """
    # Surface uniforme
    surface = np.full((size[0], size[1]), gray, dtype=np.float32)

    # Ajout bruit gaussien pour simuler texture réelle
    noise = np.random.normal(0, noise_std, size).astype(np.float32)
    surface = np.clip(surface + noise, 0, 255).astype(np.uint8)

    # Conversion en BGR (3 canaux) pour compatibilité OpenCV
    surface_bgr = cv2.cvtColor(surface, cv2.COLOR_GRAY2BGR)

    return surface_bgr


# ---------------------------------------------------------------------------
# Defect generators
# ---------------------------------------------------------------------------

def add_scratch(image, n_scratches=1):
    """
    Add linear scratch defects (Kratzer) to the surface.
    Simulates tool marks or handling damage.
    """
    result = image.copy()
    h, w = result.shape[:2]

    for _ in range(n_scratches):
        # Point de départ et direction aléatoires
        x1 = np.random.randint(50, w - 100)
        y1 = np.random.randint(50, h - 100)
        length = np.random.randint(80, 200)
        angle  = np.random.uniform(0, np.pi)

        x2 = int(x1 + length * np.cos(angle))
        y2 = int(y1 + length * np.sin(angle))

        # Rayure = ligne claire fine
        color     = (np.random.randint(160, 220),) * 3   # gris clair
        thickness = np.random.randint(1, 3)
        cv2.line(result, (x1, y1), (x2, y2), color, thickness)

    return result


def add_spot(image, n_spots=1):
    """
    Add circular spot defects (Flecken) to the surface.
    Simulates oil stains, dust contamination or material inclusions.
    """
    result = image.copy()
    h, w = result.shape[:2]

    for _ in range(n_spots):
        cx = np.random.randint(80, w - 80)
        cy = np.random.randint(80, h - 80)
        radius = np.random.randint(10, 35)

        # Tache = ellipse claire ou sombre
        bright = np.random.choice([True, False])
        color  = (np.random.randint(150, 210),) * 3 if bright else \
                 (np.random.randint(5, 25),) * 3
        cv2.ellipse(result, (cx, cy), (radius, radius // 2),
                    np.random.randint(0, 180), 0, 360, color, -1)

        # Bords doux avec flou gaussien
        result = cv2.GaussianBlur(result, (5, 5), 0)

    return result


def add_texture_defect(image):
    """
    Add a texture anomaly (Strukturfehler) — rough patch on smooth surface.
    Simulates material deformation, mold defects or surface degradation.
    """
    result = image.copy()
    h, w = result.shape[:2]

    # Zone rectangulaire avec texture différente
    x = np.random.randint(50, w - 150)
    y = np.random.randint(50, h - 150)
    bw = np.random.randint(60, 130)
    bh = np.random.randint(40, 100)

    # Texture rugueuse = bruit élevé dans la zone
    region = result[y:y+bh, x:x+bw].astype(np.float32)
    rough_noise = np.random.normal(0, 30, region.shape).astype(np.float32)
    region = np.clip(region + rough_noise, 0, 255).astype(np.uint8)
    result[y:y+bh, x:x+bw] = region

    return result


# ---------------------------------------------------------------------------
# Image set generator
# ---------------------------------------------------------------------------

def generate_dataset(output_dir=OUTPUT_DIR, n_per_class=5):
    """
    Generate a complete dataset of surface images:
    - n_per_class defect-free images (OK)
    - n_per_class images with scratches
    - n_per_class images with spots
    - n_per_class images with texture defects
    - n_per_class images with combined defects
    """
    os.makedirs(output_dir, exist_ok=True)

    categories = {
        "ok":              lambda img: img,
        "scratch":         lambda img: add_scratch(img, n_scratches=np.random.randint(1, 3)),
        "spot":            lambda img: add_spot(img, n_spots=np.random.randint(1, 3)),
        "texture_defect":  lambda img: add_texture_defect(img),
        "combined":        lambda img: add_spot(add_scratch(add_texture_defect(img))),
    }

    total = 0
    for category, transform in categories.items():
        cat_dir = os.path.join(output_dir, category)
        os.makedirs(cat_dir, exist_ok=True)

        for i in range(n_per_class):
            base  = generate_base_surface()
            image = transform(base)
            path  = os.path.join(cat_dir, f"{category}_{i+1:03d}.png")
            cv2.imwrite(path, image)
            total += 1

    print(f"✅  Dataset generated: {total} images in '{output_dir}/'")
    print(f"    Categories: {list(categories.keys())}")
    print(f"    Images per category: {n_per_class}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    np.random.seed(42)   # reproductibilité
    generate_dataset(n_per_class=10)

    # Aperçu rapide — ouvre une image de chaque catégorie
    print("\n📷  Preview — press any key to close each window")
    for category in ["ok", "scratch", "spot", "texture_defect", "combined"]:
        path = os.path.join(OUTPUT_DIR, category, f"{category}_001.png")
        img  = cv2.imread(path)
        cv2.imshow(f"Category: {category}", img)
        cv2.waitKey(0)
    cv2.destroyAllWindows()