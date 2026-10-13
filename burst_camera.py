import cv2
import time
import os

# 🔴 IMPORTANT: Flask serves only from /static
IMAGE_DIR = "static/sos_images"

def capture_burst_images():
    # 📁 Create folder if not exists
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    # 🎥 Try default camera
    cap = cv2.VideoCapture(0)

    # 🔁 If camera 0 fails, try camera 1
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("❌ Cannot open camera")
        return []

    print("🔥 Warming up camera...")
    # ⏳ CAMERA WARM-UP (CRITICAL)
    for _ in range(10):
        cap.read()
        time.sleep(0.1)

    images = []
    print("📸 Capturing 3 burst images...")

    for i in range(3):
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            continue

        filename = f"{IMAGE_DIR}/sos_{int(time.time())}_{i}.jpg"

        # 🧪 Safety check
        if frame is not None and frame.size != 0:
            cv2.imwrite(filename, frame)
            images.append(filename)
            print(f"✅ Saved: {filename}")
        else:
            print("⚠️ Empty frame skipped")

        time.sleep(0.3)  # 300 ms delay

    cap.release()
    cv2.destroyAllWindows()

    print("✅ Burst capture completed")
    return images


# 🧪 Standalone test
if __name__ == "__main__":
    capture_burst_images()