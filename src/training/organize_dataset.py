import os
import shutil

base_path = 'src/training'
splits = ['train', 'valid', 'test']

for split in splits:
    src_folder = f'{base_path}/dataset/{split}'
    image_dst = f'{base_path}/dataset/images/{split}'
    label_dst = f'{base_path}/dataset/labels/{split}'
    os.makedirs(image_dst, exist_ok=True)
    os.makedirs(label_dst, exist_ok=True)

    for file in os.listdir(src_folder):
        if file.endswith('.jpg') or file.endswith('.png'):
            shutil.move(os.path.join(src_folder, file), os.path.join(image_dst, file))
        elif file.endswith('.txt'):
            shutil.move(os.path.join(src_folder, file), os.path.join(label_dst, file))
