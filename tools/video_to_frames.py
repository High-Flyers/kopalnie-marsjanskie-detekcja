import cv2
import argparse
import os


def cut_to_frames(input_file: str, output_dir: str, count_from: int = 0) -> None:
    if not os.path.isfile(input_file):
        raise ValueError(f"{input_file=} is not a valid file path.")
    if not os.path.isdir(output_dir):
        raise ValueError(f"{output_dir=} is not a valid directory path.")
    vidcap = cv2.VideoCapture(input_file)
    success, img = vidcap.read()
    count = count_from
    while success:
        cv2.imwrite(f"{output_dir}/frame{count:04}.jpg", img)
        success, img = vidcap.read()
        count += 1


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--input", help="path to video file")
    a.add_argument("--output", help="path to output directory")
    args = a.parse_args()
    try:
        cut_to_frames(args.input, args.output)
    except ValueError as e:
        print(e)