"""Gray-world white balance and gamma correction with OpenCV and NumPy."""
import argparse
import os
import sys

import cv2
import numpy as np


def white_balance(img):
    """Gray-world white balance: scale each channel so all channel means match."""
    channels = cv2.split(img.astype(np.float32))
    means = [c.mean() for c in channels]
    target = sum(means) / 3
    balanced = [np.clip(c * (target / m), 0, 255) for c, m in zip(channels, means)]
    return cv2.merge(balanced).astype(np.uint8)


def gamma_correction(img, gamma):
    """Apply out = in ** (1 / gamma). gamma > 1 brightens, gamma < 1 darkens."""
    normalized = img / 255.0
    corrected = np.power(normalized, 1.0 / gamma)
    return np.clip(corrected * 255, 0, 255).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", default="images/sample.jpg", help="input image path")
    parser.add_argument("--gamma", type=float, default=2.2, help="gamma value (default: 2.2)")
    parser.add_argument("--out", default="results", help="output folder (default: results)")
    parser.add_argument("--show", action="store_true", help="also open preview windows")
    args = parser.parse_args()

    img = cv2.imread(args.image)
    if img is None:
        sys.exit(f"Error: could not open image '{args.image}'.")

    balanced = white_balance(img)
    corrected = gamma_correction(balanced, args.gamma)

    os.makedirs(args.out, exist_ok=True)
    cv2.imwrite(os.path.join(args.out, "original.jpg"), img)
    cv2.imwrite(os.path.join(args.out, "balanced.jpg"), balanced)
    cv2.imwrite(os.path.join(args.out, "gamma.jpg"), corrected)
    cv2.imwrite(os.path.join(args.out, "comparison.jpg"), np.hstack([img, balanced, corrected]))
    print(f"Saved results to '{args.out}/'")

    if args.show:
        cv2.imshow("Original", img)
        cv2.imshow("White balanced", balanced)
        cv2.imshow("Gamma corrected", corrected)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
