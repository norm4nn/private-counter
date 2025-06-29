from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')

results = model.predict(
    source='src/training/test1.jpg',
    save=True,
    save_txt=True,
    conf=0.5
)