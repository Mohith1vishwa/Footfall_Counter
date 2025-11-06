# AI Assignment: Footfall Counter using Computer Vision

## Objective
Develop a system that:
1. Detects humans in a video
2. Tracks movement frame-by-frame
3. Defines a **virtual ROI line**
4. Counts **entry/exit** by crossing ROI

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

## Output
- Annotated Video:https://github.com/user-attachments/assets/f1d111f2-ec73-4a74-ae98-3522613024f7
- Screenshot of the count : <img width="1919" height="1002" alt="Screenshot 2025-11-06 235904" src="https://github.com/user-attachments/assets/00bf849c-1c18-4bef-a30d-5f8ef3139be9" />


## Video Source
- Pixabay — Airport People Crowd Busy:
-https://pixabay.com/videos/airport-people-crowd-busy-36510/

---

## How to Run
```bash
pip install -r requirements.txt
python footfall_counter.py

