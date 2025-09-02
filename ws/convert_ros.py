from pathlib import Path
import shutil
from rosbags.highlevel import AnyReader
from rosbags.image import message_to_cvimage
import argparse
import numpy as np, cv2
import os, subprocess



def make_video(out, pics="pics", frame_rate=20):
    out_dir = Path(f"video/{out}.mp4")
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    
    files = sorted(Path(pics).glob("*.png"), key=lambda p: p.stem)
    
    if files:
        subprocess.run([
            "ffmpeg", "-y", "-framerate", str(frame_rate),
            "-pattern_type", "glob", "-i", f"{pics}/*.png",
            "-vf", "scale=ceil(iw/2)*2:ceil(ih/2)*2",
            "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(out_dir)
        ], check=True)
    shutil.rmtree(Path(pics))
    print("Done")

def extract_pictures(p: Path, out: Path, topic: str):
    os.makedirs("pics", exist_ok=True)
    with AnyReader([p]) as reader:
        conns = [c for c in reader.connections if c.topic == topic]
        ref_type = conns[0].msgtype
        print("extracting images...")
        if ref_type.endswith("CompressedImage"):
            for c, ts, raw in reader.messages(conns):
                message = reader.deserialize(raw, c.msgtype)
                img = cv2.imdecode(np.frombuffer(message.data, np.uint8), cv2.IMREAD_UNCHANGED)
                cv2.imwrite(str(Path("pics") / f"{ts}.png"), img)
        elif ref_type.endswith("Image"):
            for c, ts, raw in reader.messages(conns):
                m = reader.deserialize(raw, c.msgtype)
                img = message_to_cvimage(m)
                enc = (m.encoding or "").lower()
                if enc.startswith("rgb"):
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite(str(Path("pics") / f"{ts}.png"), img)
    print("rendering video...")
    make_video(out)

def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--bag", type=Path, required=True)
    p.add_argument("--out", type=Path, default="video")
    p.add_argument("--topic", type=str, required=True)
    return p

def main():
    args = parser().parse_args()
    extract_pictures(args.bag, args.out, args.topic)

if __name__ == "__main__":
    main()
