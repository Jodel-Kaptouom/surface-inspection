# Automotive Surface Inspection System
### Vision-Based Quality Control Pipeline for Automotive Interior Components

![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Language](https://img.shields.io/badge/language-Python%20%7C%20C%23-blue)
![Library](https://img.shields.io/badge/library-OpenCV-green)
![Context](https://img.shields.io/badge/context-Automotive%20QA-red)

---

## Motivation

This project simulates the core workflow of an **Applikationsingenieur für 
Bildverarbeitungssysteme** in an automotive production environment.

The goal is to build a complete surface inspection pipeline — from ROI definition 
through defect detection to real-time analysis — mirroring the tasks performed in 
industrial quality control systems for automotive interior components 
(dashboards, door panels, trim parts).

---

## What This System Does

A camera captures images of automotive surface components on a production line.
The system automatically detects surface defects and classifies each part as
**OK** or **NICHT OK** in real time.

```
Surface image captured
        ↓
ROI Definition          ← define inspection zones
        ↓
Defect Detection
   ├── Oberflächendefekte (scratches, marks)
   ├── Strukturfehler    (texture anomalies)
   └── Farbfehler        (color deviations)
        ↓
Annotated result image  ← defects highlighted in red
        ↓
Quality report          ← logs + statistics
```
---

## Development Approach — 3 Phases

### Phase 1 — Synthetic Images (Algorithm Development)
Generate controlled test images with known defects to develop
and validate detection algorithms under defined conditions.

### Phase 2 — MVTec Dataset (Real Industrial Surfaces)
Validate algorithms on real industrial surface images from the
MVTec Anomaly Detection dataset — the standard benchmark for
industrial surface inspection.

### Phase 3 — Real-Time Webcam Pipeline
Deploy the detection pipeline on a live webcam feed,
simulating a real production line camera setup.

---

## Repository Structure
## Repository Structure

```
surface-inspection/

├── README.md
├── src/
│   ├── image_generator.py     # Phase 1: synthetic test image generation
│   ├── roi_selector.py        # ROI definition (manual + automatic)
│   ├── defect_detector.py     # Defect detection algorithms
│   ├── color_analyzer.py      # Color deviation analysis
│   └── pipeline.py            # Full inspection pipeline (Mode 1 + Mode 2
├── docs/
│   ├── requirements.md        # System requirements specification
│   └── system_design.md       # Pipeline architecture
├── test_images/               # Generated + MVTec test images
│   ├── ok/                    # Defect-free reference surfaces
│   ├── scratch/               # Scratch defects (Kratzer)
│   ├── spot/                  # Spot defects (Flecken)
│   ├── texture_defect/        # Texture anomalies (Strukturfehler)
│   └── combined/              # Multiple defect types
├── results/                   # Annotated output images + inspection logs
└── validation/
└── test_cases.md          # Test scenarios mapped to requirements
```
---

## Defect Types

| Type | German term | Description |
|---|---|---|
| Scratch | Kratzer | Linear marks from handling or tooling |
| Spot | Fleck | Circular stains — oil, dust, material inclusion |
| Texture anomaly | Strukturfehler | Rough patch on smooth surface — mold or material defect |
| Color deviation | Farbfehler | Local color shift — coating or pigmentation issue |

---

## Operating Modes

### Mode 1 — Single Image Analysis
```bash
python src/pipeline.py --mode image --input test_images/scratch/scratch_001.png
```
Analyzes one image and produces an annotated result + inspection report.

### Mode 2 — Real-Time Webcam
```bash
python src/pipeline.py --mode webcam
```
Processes live webcam feed and detects defects frame by frame.

---

## Status

| Module | Status |
|---|---|
| Synthetic image generation | ✅ Complete |
| ROI definition | 🔄 In progress |
| Defect detection algorithms | 🔄 In progress |
| Color analysis | 🔄 In progress |
| Full pipeline (Mode 1) | 🔄 In progress |
| Real-time webcam (Mode 2) | 🔄 In progress |
| C# result viewer | 🔄 In progress |
| MVTec validation | 🔄 In progress |

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python 3.x | Core algorithm development |
| OpenCV | Image processing pipeline |
| NumPy | Image data manipulation |
| C# / Visual Studio | Result visualization interface |
| MVTec AD Dataset | Real industrial surface validation |

---

## Connection to Industrial Practice

This project directly maps to the responsibilities of an
**Applikationsingenieur für Bildverarbeitungssysteme**:

| Industrial task | Project implementation |
|---|---|
| ROI definition | `roi_selector.py` |
| Algorithmenentwicklung (Oberfläche, Struktur, Farbe) | `defect_detector.py`, `color_analyzer.py` |
| Inbetriebnahme + Fehleranalyse | `pipeline.py` + inspection logs |
| Echtzeit-Inspektion | Mode 2 — real-time webcam pipeline |
| Dokumentation | `docs/` + `validation/` |

---

## Author

**Jodel Baurel Kaptouom Fotso**
M.Eng. Elektrotechnik & Informationstechnik — HAWK Göttingen
[GitHub](https://github.com/Jodel-Kaptouom) | 
[LinkedIn](https://www.linkedin.com/in/jodel-baurel-kaptouom-fotso/)

*Developed as preparation for a position as 
Applikationsingenieur für Bildverarbeitungssysteme 
in the automotive industry.*