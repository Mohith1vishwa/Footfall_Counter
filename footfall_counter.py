"""
AI ASSIGNMENT: FOOTFALL COUNTER USING COMPUTER VISION
YOLOv8 + SORT + 65% GREEN ROI LINE
NO USER INTERACTION | HIGH ACCURACY
"""

import cv2
import numpy as np
from ultralytics import YOLO

# Load SORT tracker from same folder
try:
    from sort import Sort
except ImportError:
    print("ERROR: sort.py not found! Place it in the same folder.")
    exit(1)

# ============================= CONFIG =============================
VIDEO_PATH = "airport_crowd.mp4"          # Your test video
OUTPUT_PATH = "output_with_counts.mp4"
CONFIDENCE_THRESHOLD = 0.5
LINE_HEIGHT_RATIO = 0.65                # 65% of frame height
# =================================================================

def main():
    # Initialize YOLO and SORT
    model = YOLO('yolov8n.pt')          # Use yolov8s.pt for better accuracy
    tracker = Sort()

    # Open input video
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video {VIDEO_PATH}")
        return

    # Video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    # Output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

    # === FIXED 65% GREEN ROI LINE ===
    line_y = int(height * LINE_HEIGHT_RATIO)
    line_start = (0, line_y)
    line_end = (width, line_y)

    # Counters and tracking history
    in_count = out_count = 0
    entered_ids = set()
    exited_ids = set()
    prev_bottom_y = {}  # Tracks bottom Y of each person's bounding box

    print(f"Green ROI line fixed at {LINE_HEIGHT_RATIO*100}% height (Y={line_y})")
    print("Counting: Top→Bottom = ENTER | Bottom→Top = EXIT")
    print("Processing video...")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        # === 1. Person Detection with YOLOv8 ===
        results = model(frame, classes=0, verbose=False)[0]
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            if conf >= CONFIDENCE_THRESHOLD:
                detections.append([x1, y1, x2, y2])

        # === 2. Multi-Object Tracking with SORT ===
        tracks = tracker.update(np.array(detections)) if detections else np.empty((0, 5))

        # === 3. Process Each Tracked Person ===
        for track in tracks:
            x1, y1, x2, y2, track_id = map(int, track)
            bottom_y = y2  # Use bottom of bounding box (more accurate than center)

            # Draw bounding box and ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID:{track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            # Optional: Mark bottom point
            cv2.circle(frame, ((x1 + x2) // 2, bottom_y), 5, (0, 0, 255), -1)

            # === 4. Count Crossing Using Bottom of Person ===
            if track_id in prev_bottom_y:
                prev_by = prev_bottom_y[track_id]

                # ENTER: Person moves from above to below the line
                if prev_by < line_y <= bottom_y and track_id not in entered_ids:
                    in_count += 1
                    entered_ids.add(track_id)
                    print(f"[FRAME {frame_idx}] ENTER | ID:{track_id} | Y:{prev_by}→{bottom_y}")

                # EXIT: Person moves from below to above the line
                elif prev_by > line_y >= bottom_y and track_id not in exited_ids:
                    out_count += 1
                    exited_ids.add(track_id)
                    print(f"[FRAME {frame_idx}] EXIT  | ID:{track_id} | Y:{prev_by}→{bottom_y}")

            prev_bottom_y[track_id] = bottom_y

        # === 5. Draw GREEN ROI Line ===
        cv2.line(frame, line_start, line_end, (0, 255, 0), 3)
        cv2.putText(frame, "ROI LINE (65%)", (10, line_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # === 6. Display Real-time Counts ===
        cv2.putText(frame, f"IN: {in_count}", (15, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        cv2.putText(frame, f"OUT: {out_count}", (15, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

        # Save and display frame
        out.write(frame)
        cv2.imshow("Footfall Counter - 65% Line", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # === Cleanup & Final Report ===
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("\n" + "="*60)
    print("FINAL FOOTFALL COUNT")
    print(f"People ENTERED : {in_count}")
    print(f"People EXITED  : {out_count}")
    print(f"Output saved   : {OUTPUT_PATH}")
    print(f"ROI Line at    : Y = {line_y} ({LINE_HEIGHT_RATIO*100}% of height)")
    print("="*60)


if __name__ == "__main__":
    main()