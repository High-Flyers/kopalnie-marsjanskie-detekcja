import sys
import traceback
import numpy as np
import cv2
import imagezmq

try:
    with imagezmq.ImageHub() as image_hub:
        while True:  # receive images until Ctrl-C is pressed
            sent_from, jpg_buffer = image_hub.recv_jpg()
            image = cv2.imdecode(np.frombuffer(jpg_buffer, dtype="uint8"), -1)
            cv2.imshow(sent_from, image)  # display images 1 window per sent_from
            cv2.waitKey(1)
            image_hub.send_reply(b"OK")
except (KeyboardInterrupt, SystemExit):
    pass
except Exception as ex:
    print("Traceback error:", ex)
    traceback.print_exc()
finally:
    cv2.destroyAllWindows()
    sys.exit()
