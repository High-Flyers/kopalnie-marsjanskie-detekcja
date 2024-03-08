Narzędzia i kod wspierający tworzenie modelu do detekcji obrazu na konkurs kopalnie marsjańskie w ramach Droniady 2024

Komenda do uruchomienia modelu do trenowania:
```sh
yolo task=detect mode=train model=yolov8n.pt imgsz=640 data=kopalnie_v8.yaml epochs=50 batch=16 name={name} cache 
```
Komenda powinna być uruchomiona z poziomu katalogu zawierającego plik `kopalnie_v8.yaml` (katalog `model`).