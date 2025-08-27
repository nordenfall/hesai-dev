from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.image import message_to_cvimage
import cv2
import os

bag_dir = Path("data/convert/out")
topic = "/Logitech_webcam/image_raw/compressed"
result = Path("result")

with AnyReader([bag_dir]) as reader:
    conns = [c for c in reader.connections if c.topic == topic]
    for conn, ts, raw in reader.messages(connections=conns):
        msg = reader.deserialize(raw, conn.msgtype)  
        fmt = (getattr(msg, "format", "") or "").lower()
        ext = "jpg" if "jp" in fmt else ("png" if "png" in fmt else "bin")
        (result / f"{ts}.{ext}").write_bytes(msg.data)
    

        
