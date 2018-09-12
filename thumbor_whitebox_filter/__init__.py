#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

__version__ = '0.0.11'

try:
    from thumbor_whitebox_filter.white_transparency import Filter  # NOQA
except ImportError:
    logging.exception('Could not import thumbor_whitebox_filter.')
