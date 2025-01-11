import torch
import cv2
import json

#loaded a pre trained object detection model that is YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

#dataset
image_path = "input_image.jpg"
image = cv2.imread(image_path)

#this is for object detection
results = model(image)
detections = results.pandas().xyxy[0]

#this is processing the object detection for json output
output = []
for _, row in detections.iterrows():
    object_data = {
        "object": row['name'],
        "confidence": float(row['confidence']),
        "bbox": [row['xmin'], row['ymin'], row['xmax'], row['ymax']],
        "subobject": []
    }

    #sub object detection for example detecting TIRE inside CAR
    if row['name'] == "car":
        subobject_data = {
            "object": "tire",
            "confidence": 0.85,
            "bbox": [row['xmin'] + 10, row['ymin'] + 10, row['xmin'] + 50, row['ymin'] + 50]
        }
        object_data["subobject"].append(subobject_data)
    output.append(object_data)

with open("detections.json", "w") as json_file:
    json.dump(output, json_file, indent=4)

print(json.dumps(output, indent=4))



#json structure for detected objects
{
  "object": "Car",
  "id": 1,
  "bbox": [x1, y1, x2, y2],
  "subobject": {
    "object": "Tire",
    "id": 1,
    "bbox": [x1, y1, x2, y2]
  }
}

