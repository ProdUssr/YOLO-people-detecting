import os
from ultralytics import YOLO
import cv2

def detect_people_in_images(input_folder="RSK"):
    """
    Выполняет детекцию людей на всех изображениях 
    в указанной папке и сохраняет результаты.
    """
    print("[INFO] Подгружаем модель")
    model = YOLO('yolo26x.pt')
    
    print("[INFO] Собираем пути до изображений")
    image_paths = [os.path.join(input_folder, img) for img in os.listdir(input_folder)]
    
    print("[INFO] Детектируем людей")
    detected_images = []
    for image_path in image_paths:
        img = cv2.imread(image_path)
        
        # детектируем людей (в датасете COCO класс person под номером 0)
        results = model(img, classes=[0], conf=0.1, iou=0.25, imgsz=1984, end2end=False)[0]
        detected_images.append(results.plot(labels=False, conf=False))
        
    return detected_images
            
            
def show_images(images):
    """
    Выводит изображения в отдельное окно, в котором
    можно перелистывать фото используя клавиши A (перелистнуть влево) и
    D (перелиснуть вправо), чтобы выйти нужно нажать ESC
    """
    
    current_index = 0
    cv2.namedWindow('detected_people', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('detected_people', 1200, 800)
    cv2.imshow('detected_people', images[current_index])
    
    while True: 
        key = cv2.waitKey(0) & 0xFF
        if key == 27: # ESC - выход
            break
        
        elif key == 100 or key == 226: # D - переключение фотографии вправо
            current_index = (current_index + 1) % len(images)
            cv2.imshow('detected_people', images[current_index])
        
        elif key == 97 or key == 244: # A - переключение фотографии влево
            current_index = (current_index - 1) % len(images)
            cv2.imshow('detected_people', images[current_index])
    
    cv2.destroyAllWindows()
            


if __name__ == "__main__":
    detected_images = detect_people_in_images(input_folder="RSK")
    show_images(detected_images)