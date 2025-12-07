import numpy as np
import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2 as cv


class LutTransformer:
    def __init__(self, lut_img: np.ndarray):
        self.lut = lut_img
        self.lut_size = lut_img.shape[0]
        lut_slices = np.hsplit(lut_img, self.lut_size)
        self.lut_3d = np.stack(lut_slices, axis=0)

    def apply(self, image: np.ndarray) -> np.ndarray:
        if image.dtype == np.float32 or image.dtype == np.float64:
            image = np.clip(image, 0.0, None)
            img = self._compress_hdr(image)
        else:
            img = image.astype(np.float32) / 255.0

        remapped = self._remap(img)
        img_floor = np.floor(remapped).astype(np.uint8)
        img_ceil = np.clip(img_floor + 1, None, self.lut_size - 1)
        img_fract = remapped - img_floor

        del remapped

        b0 = img_floor[..., 0].astype(np.uint8)
        g0 = img_floor[..., 1].astype(np.uint8)
        r0 = img_floor[..., 2].astype(np.uint8)
        b1 = img_ceil[..., 0].astype(np.uint8)
        g1 = img_ceil[..., 1].astype(np.uint8)
        r1 = img_ceil[..., 2].astype(np.uint8)
        b2 = img_fract[..., 0].astype(np.float32)
        g2 = img_fract[..., 1].astype(np.float32)
        r2 = img_fract[..., 2].astype(np.float32)
        del img_floor, img_ceil, img_fract

        point_000 = self.lut_3d[b0, g0, r0, :]
        point_001 = self.lut_3d[b0, g0, r1, :]
        point_010 = self.lut_3d[b0, g1, r0, :]
        point_011 = self.lut_3d[b0, g1, r1, :]
        point_100 = self.lut_3d[b1, g0, r0, :]
        point_101 = self.lut_3d[b1, g0, r1, :]
        point_110 = self.lut_3d[b1, g1, r0, :]
        point_111 = self.lut_3d[b1, g1, r1, :]
        del b0, g0, r0, b1, g1, r1

        line_00 = self._linear_interpolate(point_000, point_001, r2)
        line_01 = self._linear_interpolate(point_010, point_011, r2)
        line_10 = self._linear_interpolate(point_100, point_101, r2)
        line_11 = self._linear_interpolate(point_110, point_111, r2)
        del (
            point_000,
            point_001,
            point_010,
            point_011,
            point_100,
            point_101,
            point_110,
            point_111,
            r2,
        )

        plane_0 = self._linear_interpolate(line_00, line_01, g2)
        plane_1 = self._linear_interpolate(line_10, line_11, g2)
        del line_00, line_01, line_10, line_11, g2

        cube = self._linear_interpolate(plane_0, plane_1, b2)
        del plane_0, plane_1, b2

        result = cv.cvtColor(cube, cv.COLOR_BGRA2RGBA)
        return result

    def _compress_hdr(self, image: np.ndarray) -> np.ndarray:
        max_pq = 100.0

        N = 2610.0 / (4096.0 * 4.0)
        M = (2523.0 * 128.0) / 4096.0
        C_1 = 3424.0 / 4096.0
        C_2 = (2413.0 * 32.0) / 4096.0
        C_3 = (2392.0 * 32.0) / 4096.0

        l_col = image / max_pq
        pow_col = l_col**N
        del l_col
        num = C_1 + C_2 * pow_col
        den = 1.0 + C_3 * pow_col
        del pow_col

        linear_pq = (num / den) ** M
        del num, den
        result = np.clip(linear_pq, 0.0, 1.0)

        return result

    def _remap(self, image: np.ndarray) -> np.ndarray:
        remapped = image * (self.lut_size - 1)
        remapped = np.clip(remapped, 0, self.lut_size - 1)
        return remapped

    def _linear_interpolate(
        self, point_x: np.ndarray, point_y: np.ndarray, red_channel: np.ndarray
    ) -> np.ndarray:
        return (1.0 - red_channel[..., None]) * point_x + red_channel[
            ..., None
        ] * point_y
