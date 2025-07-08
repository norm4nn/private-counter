import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image
from redis import Redis

from utils.db import get_db_connection, add_file, is_file_processed
from utils.nc import get_nextcloud_app, get_setings

redis_conn = Redis(host='localhost', port=6379, db=0)
QUEUED_SET = "queued_files"

from ultralytics import YOLO


def result_to_digits(results):
    """
    Przetwarza wyniki detekcji YOLO i zwraca listę cyfr jako string.
    """
    if not results or len(results) == 0:
        return ""

    # Sprawdź, czy wyniki są typu list
    if isinstance(results, list):
        results = results[0]  # Pobierz pierwszy wynik, jeśli jest lista

    if hasattr(results, 'boxes'):
        return process_boxes(results.boxes)

    return ""

def process_boxes(boxes):
    """
    Przetwarza boxy detekcji i zwraca listę cyfr jako string.
    """
    digits = []
    if boxes is not None and len(boxes) > 0:
        # Pobierz współrzędne x dla wszystkich boxów i klasy
        box_data = []
        for box in boxes:
            x1 = float(box.xyxy[0][0])  # lewy górny x
            cls = int(box.cls[0]) if hasattr(box, 'cls') else int(box.cls)
            box_data.append((x1, cls))
        # Posortuj po x (od lewej do prawej)
        box_data.sort(key=lambda x: x[0])
        # Dodaj klasy do listy cyfr
        digits.extend(str(cls) for _, cls in box_data)

    digits_str = ''.join(digits)
    digits_str = digits_str[:-3] + "." + digits_str[-3:] if len(digits_str) > 3 else digits_str
    return digits_str


def process_file(file_path: str):
    redis_conn.srem(QUEUED_SET, file_path)

    model = YOLO(Path(__file__).parent.parent / "model" / "best.pt")
    nc = get_nextcloud_app()
    db = get_db_connection()

    if is_file_processed(db, file_path):
        print(f"[WORKER] File already processed: {file_path}")
        db.close()
        return

    print(f"[WORKER] Processing: {file_path}")

    # Download the image from Nextcloud
    img_stream = BytesIO()
    nc.files.download2stream(file_path, img_stream)
    img_stream.seek(0)
    img = Image.open(img_stream)

    # Perform inference
    results = model.predict(source=img)
    digits = result_to_digits(results)
    img_stream.close()

    # Save the results in a CSV file
    upload_path = get_setings(nc, "upload_path", "/output.csv")
    stream = BytesIO()
    nc.files.download2stream(upload_path, stream)
    stream.write((",".join([file_path, digits, datetime.datetime.now().strftime("%Y-%m-%d %H:%i:%s")]) + "\n").encode())
    stream.seek(0)
    nc.files.upload_stream(upload_path, stream)
    stream.close()

    add_file(db, file_path)
    db.close()

    print(f"[WORKER] Done: {file_path}")

