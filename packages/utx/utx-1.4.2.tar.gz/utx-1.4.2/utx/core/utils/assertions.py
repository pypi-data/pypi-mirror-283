#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2023/12/25 7:35 PM
@Desc    :  calc_diff line.
"""
import os

from airtest.aircv.cal_confidence import *
from airtest.core.api import *
from airtest.core.assertions import assert_less_equal
from airtest.core.helper import log
from airtest.core.settings import Settings as ST

from utx.core.utils.tools import display

auto_setup(__file__)


def assert_confidence(img, confidence=0.9):
    """
    断言两张图片的相似度
    :param img: 基准图片
    :param confidence: 阈值
    :return:
    """
    snapshot(filename="diff.png", msg="获取当前页面actual截图")

    resolution = display()
    log(arg=resolution, desc=f"获取当前设备分辨率: {resolution}")

    logdir = ST.LOG_DIR or "."
    expect_img = os.path.join(os.path.dirname(os.path.dirname(logdir)), img)
    actual_img = os.path.join(logdir, "diff.png")

    expect = cv2.resize(cv2.imread(expect_img), resolution)
    actual = cv2.resize(cv2.imread(actual_img), resolution)

    actual_confidence = cal_ccoeff_confidence(expect, actual)
    log("图片相似度为: %.2f" % actual_confidence)

    assert_less_equal(confidence, actual_confidence, "图片阈值对比")


def assert_error_confidence(confidence=0.2, rgb=True):
    """
    同大小彩图计算相似度 实际图与空白图对比 相似度越高，说明实际图越异常
    :param rgb: 是否使用rgb计算
    :param confidence: 阈值 默认0.2
    :return:
    """
    sleep(4)
    snapshot(filename="diff.png", msg="获取当前页面actual截图")

    resolution = display()
    log(arg=resolution, desc=f"获取当前设备分辨率: {resolution}")

    logdir = ST.LOG_DIR or "."
    actual_img = os.path.join(logdir, "diff.png")

    expect_img = os.path.join(os.path.dirname(__file__), "white.png")

    expect = cv2.resize(cv2.imread(expect_img), resolution)
    actual = cv2.resize(cv2.imread(actual_img), resolution)

    if rgb:
        actual_confidence = cal_rgb_confidence(expect, actual)
    else:
        actual_confidence = cal_ccoeff_confidence(expect, actual)
    log("图片相似度为: %.2f" % actual_confidence)

    assert_less_equal(actual_confidence, confidence, "图片阈值对比")
