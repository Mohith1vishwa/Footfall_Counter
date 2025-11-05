# AI Assignment: Footfall Counter using Computer Vision

## Objective
Develop a system that:
1. Detects humans in a video
2. Tracks movement frame-by-frame
3. Defines a **virtual ROI line**
4. Counts **entry/exit** by crossing ROI

**All requirements met.**

---

## Solution
- **Detection**: YOLOv8 (`person` class)
- **Tracking**: SORT algorithm
- **ROI**: **Green horizontal line at 65% height**
- **Counting**: Bottom of bounding box crosses line
- **Direction**: Top to Bottom = ENTER, Bottom to Top = EXIT

---

## Features
- Fixed **65% green ROI line** (visible from start)
- **No user input** required
- High accuracy using **bottom of person**
- Real-time IN/OUT display
- Output video saved
- Final result printed

---

## How to Run
```bash
pip install -r requirements.txt
python footfall_counter.py