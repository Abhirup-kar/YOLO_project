# YOLO Intruder Detector

A simple, friendly project that uses a YOLO model to detect intruders from a live feed or video stream and save snapshots to help with review and evidence. This repo contains a lightweight Python app that loads a pretrained model and writes detected intruder images to the `intruder_snapshots/` folder.

## What this does

- Loads the YOLO model from `best.pt` and runs inference using `app.py`.
- When a person or intruder is detected, saves a timestamped snapshot into `intruder_snapshots/`.
- Minimal, easy-to-run script suitable for local testing and small deployments.

## Files of interest

- [app.py](app.py) — main application script to run detection.
- [best.pt](best.pt) — pretrained YOLO model used for inference.
- [requirements.txt](requirements.txt) — Python dependencies.
- `intruder_snapshots/` — directory where detected snapshots are saved.

## Requirements

- Python 3.8+ recommended
- A webcam or a video file for input

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick start

1. Make sure `best.pt` is present in the project root.
2. Plug in a webcam or prepare a video file.
3. Run the app:

```bash
python app.py
```

The script will start the detector and write snapshots to `intruder_snapshots/` when intruders are detected.

## Configuration

If you want to change the source (camera index or video file) or adjust detection thresholds, edit `app.py`. Look for clearly marked variables near the top of the file for `source`, `confidence`, or `save_path`.

## How snapshots are saved

Snapshots are named with a timestamp so you can easily trace when a detection occurred. The folder `intruder_snapshots/` is safe to inspect and archive.

## Troubleshooting

- No detections: verify the camera is accessible and `best.pt` is a compatible YOLO model. Try increasing lighting or adjusting confidence thresholds.
- Dependency issues: re-run `pip install -r requirements.txt` in a clean virtualenv.

## Extending this project

- Add email or SMS alerts when an intruder is detected.
- Integrate with a lightweight web UI to browse snapshots.
- Replace `best.pt` with a custom-trained model for your environment.

## License & Contact

This project is provided as-is for demonstration and personal use. If you'd like help customizing or deploying this, open an issue or message me.

---

Enjoy — and stay safe! 👋
