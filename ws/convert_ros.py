from pathlib import Path
import tempfile
from rosbags.highlevel import AnyReader
from rosbags.image import message_to_cvimage
import argparse
import numpy as np, cv2
import os, subprocess, shutil



def make_video(out, pics="pics"):
    out_dir = Path(f"video/{out}.mp4")
    files = sorted(Path(pics).glob("*.png"), key=lambda p: int(p.stem))
    if len(files) == 1:
        subprocess.run(["ffmpeg","-y","-loop","1","-t","3","-i",str(files[0]),
                        "-vf","scale=ceil(iw/2)*2:ceil(ih/2)*2",
                        "-c:v","libx264","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",out_dir], check=True)
        return
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
        for a,b in zip(files, files[1:]):
            f.write(f"file '{a.as_posix()}'\n")
            dt = max((int(b.stem)-int(a.stem))/1e9, 1/1000)
            f.write(f"duration {dt:.9f}\n")
        f.write(f"file '{files[-1].as_posix()}'\n")
        lst = f.name
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,
                    "-vsync","vfr","-vf","scale=ceil(iw/2)*2:ceil(ih/2)*2",
                    "-c:v","libx264","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",out_dir], check=True)
    Path(lst).unlink(missing_ok=True)

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
