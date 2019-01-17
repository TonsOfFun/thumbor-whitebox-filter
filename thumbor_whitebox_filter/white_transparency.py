#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from PIL import Image
from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):
    @filter_method(
        BaseFilter.PositiveNumber,#threshold_low
        BaseFilter.PositiveNumber,#threshold_high
    )
    def white_transparency(self, threshold_low=220, threshold_high=255):
        pil_image = self.engine.image.convert('RGB')
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        im = open_cv_image[:, :, ::-1].copy()

        # Add Border
        row, col= im.shape[:2]
        bottom= im[row-2:row, 0:col]
        mean= cv2.mean(bottom)[0]

        bordersize=10
        img=cv2.copyMakeBorder(im, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[mean,mean,mean] )

        im_in = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        th, im_th = cv2.threshold(im_in, threshold_low, threshold_high, cv2.THRESH_BINARY_INV);

        # Copy the thresholded image.
        im_floodfill = im_th.copy()

        # Mask used to flood filling.
        # Notice the size needs to be 2 pixels more than the image.
        h, w = im_th.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)

        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0,0), 255);

        # Invert floodfilled image
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        # Combine the two images to get the foreground.
        im_out = im_th | im_floodfill_inv

        # Display images.
        masked_output = cv2.bitwise_and(img, img, mask = im_out)
        masked_rgb = cv2.cvtColor(masked_output, cv2.COLOR_BGR2RGB)
        masked_rgba = cv2.cvtColor(masked_rgb, cv2.COLOR_RGB2RGBA)
        masked_rgba[np.all(masked_rgba == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]

        self.engine.image = Image.fromarray(masked_rgba)
