from ultralytics import YOLO

model = YOLO('../../runs/detect/train3/weights/last.pt')
model.train(data='data.yaml', epochs=20, imgsz=640, batch=16, device=[0], resume=True)

