import argparse
from pathlib import Path
from rosbags.convert import convert
from rosbags.typesys import Stores, get_typestore
import subprocess

def run_convert(path:Path, out:Path):
    metadata = path / "metadata.yaml"
    if metadata.exists() and path.is_dir():
        print("Already in ros2 bag")
        return 1
    elif path.is_file() and (path.suffix.lower() == ".bag" or path.suffix.lower() == ".mcap"):
        dst_typestore = get_typestore(Stores.ROS2_JAZZY)
        convert(
            srcs=[path],
            dst=out,
            dst_storage="sqlite3",     
            dst_version=8,
            compress=None,
            compress_mode="file",       
            default_typestore=None,
            typestore=dst_typestore,
            exclude_topics=(),
            include_topics=(),
            exclude_msgtypes=(),
            include_msgtypes=(),
        )

def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--bag", type=Path, help="path to any ros type bag file")
    p.add_argument("--out", type=Path, help="result dir file")
    return p
        
def main():
    args = parser().parse_args()
    run_convert(args.bag, args.out)
    subprocess.run(["./topics.bash", args.out])
if __name__ == "__main__":
    main()