# import cv2
# import torch
# from ultralytics import YOLO
# from torchvision.transforms import transforms
# import os
# import time

# def process_frame(frame, detections):
#   if isinstance(detections, torch.Tensor) and detections.shape[0] > 0:
#     class_mapping = {0: 'eye move', 1: 'hand move', 2: 'mobile use', 3: 'looking side', 4: 'normal'}
#     confidences = detections[:, 4]
#     class_ids = torch.argmax(detections[:, 5:], dim=1).tolist()

#     max_score_idx = torch.argmax(confidences).item()
#     max_score = confidences[max_score_idx].item()
#     max_class_idx = class_ids[max_score_idx]

#     object_class = class_mapping[max_class_idx]
#     x1, y1, x2, y2 = get_bounding_box_from_tensor(detections[max_score_idx])

#     screenshot = frame.copy()
#     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#     return object_class, max_score, x1, y1, x2, y2, screenshot
#   else:
#     return None, None, None, None, None, None, None

# def get_bounding_box_from_tensor(detection):
#   x_center, y_center, width, height = detection[:4]
#   x1 = int(x_center - width / 2)
#   y1 = int(y_center - height / 2)
#   x2 = int(x_center + width / 2)
#   y2 = int(y_center + height / 2)
#   return x1, y1, x2, y2

# def capture_video(duration, screenshot_path):
#     cap = cv2.VideoCapture(0)  

#     start_time = cv2.getTickCount()

#     model = YOLO('C:/Users/grvn1/OneDrive/Desktop/Career-Recommendation-System-API/data/best.pt')
#     transform = transforms.Compose([transforms.ToPILImage(), transforms.Resize((320, 320)), transforms.ToTensor()])

#     last_detection_time = start_time

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         if (cv2.getTickCount() - last_detection_time) / cv2.getTickFrequency() >= 2:
#             input_tensor = transform(frame).unsqueeze(0)
#             detections = model(input_tensor)

#             moment_class, score, x1, y1, x2, y2, screenshot = process_frame(frame, detections)

#             if moment_class is not None and score is not None and screenshot is not None:
#                 timestamp = int(time.time())
#                 filename = f'{screenshot_path}/screenshot_{timestamp}.jpg'
#                 try:
#                     cv2.imwrite(filename, screenshot)
#                     print(f"Moment Class: {moment_class}, Score: {score}, Saved to: {filename}")
#                 except Exception as e:
#                     print(f"Error saving screenshot: {e}")
#                     print(f"Path provided: {screenshot_path}")
#                     print(f"Filename: {filename}")

#             last_detection_time = cv2.getTickCount()

#         cv2.imshow('Video', frame)

#         current_time = cv2.getTickCount()
#         if (current_time - start_time) / cv2.getTickFrequency() >= duration:
#             break

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# screenshot_path = 'data\screenshots'  
# capture_video(duration=60, screenshot_path=screenshot_path)