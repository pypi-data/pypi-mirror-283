#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  8/31/2021 6:42 PM
@Desc    :  Runner line.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import unittest
import warnings
from argparse import *
from copy import copy

from airtest.core.android.adb import ADB
from airtest.core.api import auto_setup
from airtest.core.api import connect_device
from airtest.core.api import device
from airtest.core.api import log
from airtest.core.api import shell
from airtest.core.api import start_app
from airtest.core.api import stop_app
from airtest.core.error import AirtestError
from airtest.core.error import DeviceConnectionError
from airtest.core.helper import device_platform
from airtest.core.helper import G
from airtest.core.settings import Settings as ST
from airtest.utils.compat import script_dir_name
from airtest.utils.compat import script_log_dir
from poco.exceptions import PocoException
from popups.dismiss import popup
from popups.dismiss import UT

from utx.core.css import report
from utx.core.css.custom_report import air_cmd
from utx.core.css.custom_report import gen_one_report
from utx.core.css.custom_report import gen_summary
from utx.core.css.custom_report import get_log_dir
from utx.core.css.custom_report import load_json_data
from utx.core.utils.error import UTXError
from utx.core.utils.tools import decryption
from utx.core.utils.tools import ios_device_info
from utx.core.utils.tools import plat


class AirtestCase(unittest.TestCase):
    PROJECT_ROOT = "."
    SCRIPTEXT = ".air"
    TPLEXT = ".png"

    @classmethod
    def setUpClass(cls):
        cls.args = args

        setup_by_args(args)

        # setup script exec scope
        cls.scope = copy(globals())
        cls.scope["exec_script"] = cls.exec_other_script

    def setUp(self):
        if self.args.log and self.args.recording:
            try:
                device().start_recording(mode="ffmpeg")
            except AirtestError:
                traceback.print_exc()

    def tearDown(self):
        if self.args.log and self.args.recording:
            try:
                if isinstance(
                    self.args.recording, str
                ) and self.args.recording.endswith(".mp4"):
                    output_name = os.path.basename(self.args.recording)
                    # output_name = dev.serialno + "_" + basename if len(G.DEVICE_LIST) > 1 else basename
                else:
                    output_name = f"recording_{device().serialno}.mp4"
                output = os.path.join(self.args.log, output_name)
                device().stop_recording(output)
            except AirtestError:
                traceback.print_exc()

    def runTest(self):
        scriptpath, pyfilename = script_dir_name(self.args.script)
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        self.scope["__file__"] = pyfilepath
        with open(pyfilepath, encoding="utf8") as f:
            code = f.read()
        pyfilepath = pyfilepath.encode(sys.getfilesystemencoding())

        try:
            exec(compile(code.encode("utf-8"), pyfilepath, "exec"), self.scope)
        except Exception as err:
            log(err, desc="Final Error", snapshot=True if G.DEVICE_LIST else False)
            raise

    @classmethod
    def exec_other_script(cls, scriptpath):
        """run other script in test script"""

        warnings.simplefilter("always")
        warnings.warn("please use using() api instead.", PendingDeprecationWarning)

        def _sub_dir_name(scriptname):
            dirname = os.path.splitdrive(os.path.normpath(scriptname))[-1]
            dirname = (
                dirname.strip(os.path.sep)
                .replace(os.path.sep, "_")
                .replace(cls.SCRIPTEXT, "_sub")
            )
            return dirname

        def _copy_script(src, dst):
            if os.path.isdir(dst):
                shutil.rmtree(dst, ignore_errors=True)
            os.mkdir(dst)
            for f in os.listdir(src):
                srcfile = os.path.join(src, f)
                if not (os.path.isfile(srcfile) and f.endswith(cls.TPLEXT)):
                    continue
                dstfile = os.path.join(dst, f)
                shutil.copy(srcfile, dstfile)

        # find script in PROJECT_ROOT
        scriptpath = os.path.join(ST.PROJECT_ROOT, scriptpath)
        # copy submodule's images into sub_dir
        sub_dir = _sub_dir_name(scriptpath)
        sub_dirpath = os.path.join(cls.args.script, sub_dir)
        _copy_script(scriptpath, sub_dirpath)
        # read code
        pyfilename = os.path.basename(scriptpath).replace(cls.SCRIPTEXT, ".py")
        pyfilepath = os.path.join(scriptpath, pyfilename)
        pyfilepath = os.path.abspath(pyfilepath)
        with open(pyfilepath, encoding="utf8") as f:
            code = f.read()
        # replace tpl filepath with filepath in sub_dir
        code = re.sub(r"[\'\"](\w+.png)[\'\"]", r"\"%s/\g<1>\"" % sub_dir, code)
        exec(compile(code.encode("utf8"), pyfilepath, "exec"), cls.scope)


def setup_by_args(args):
    # init devices
    if isinstance(args.device, list):
        devices = args.device
    elif args.device:
        devices = [args.device]
    else:
        devices = []
        print("do not connect device")

    # set base dir to find tpl
    dirpath, _ = script_dir_name(args.script)

    # set log dir
    if args.log:
        args.log = script_log_dir(dirpath, args.log)
        print("save log in '%s'" % args.log)
    else:
        print("do not save log")

    # set snapshot quality
    if args.compress:
        compress = args.compress
    else:
        compress = ST.SNAPSHOT_QUALITY

    if args.no_image:
        ST.SAVE_IMAGE = False

    # guess project_root to be basedir of current .air path
    project_root = os.path.dirname(args.script) if not ST.PROJECT_ROOT else None

    auto_setup(dirpath, devices, args.log, project_root, compress)


def run_script(parsed_args, testcase_cls=AirtestCase):
    global args  # make it global deliberately to be used in AirtestCase & test scripts
    args = parsed_args
    suite = unittest.TestSuite()
    suite.addTest(testcase_cls())
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    # if not result.wasSuccessful():
    #     sys.exit(-1)


def custom_resize_method(w, h, sch_resolution, src_resolution):
    """
    Resolution Adaptation Rules
    :param w:
    :param h:
    :param sch_resolution:
    :param src_resolution:
    :return: device resolution
    """
    return int(w), int(h)


def run_air(
    devices,
    case,
    app_name,
    log_path,
    case_path,
    base_dir,
    static_dir=decryption("aHR0cHM6Ly9jZG4ub3BlbnV0eC5jbi9jL3N0YXRpYw=="),
    record=None,
):
    """
    //See also: https://www.theiphonewiki.com/wiki/Models

    :param devices: read device id
    :param case: case list
    :param record: whether to enable recording
    :param log_path: log_path
    :param case_path: case_path
    :param base_dir: base_dir
    :param app_name: app_name
    :param static_dir: use local style file when empty

    :return:
    """

    current_dev = connect_device(devices)
    current_dev.wake()

    if device_platform().lower() in "ios":
        _device = ios_device_info()
        model = _device["MarketName"]
        build_version = _device["ProductVersion"]
        dev = model + f" ios {build_version}".replace("\n", "").replace("\r", "")

    elif device_platform().lower() in "android":
        serialno = device().serialno
        model = ADB(serialno=serialno).get_model()
        build_version = shell("getprop ro.build.version.release")
        dev = model + f" Android {build_version}".replace("\n", "").replace("\r", "")
    else:
        print(f"{device_platform()} is unsupported platform on utx!")
        raise AirtestError("utx unsupported this platform!")

    UT.SYS = False
    UT.LOOP = 1
    popup(devices=devices)

    if os.path.isdir(log_path):
        pass
    else:
        os.makedirs(log_path)
        print(str(log_path) + "is created")

    if str(case).endswith(".air"):
        if plat() == "Windows":
            air_name = str(case).split("\\")[-1]
        else:
            air_name = str(case).split("/")[-1]

        if record:
            record = air_name.replace(".air", ".mp4")

        print(case)
        log = os.path.join(log_path + "/" + dev + "/" + air_name.replace(".air", ""))

        run_log = case + "/" + "log" + "/" + dev
        if not os.path.exists(run_log):
            os.makedirs(run_log)
        print(log)
        if os.path.isdir(log):
            pass
        else:
            os.makedirs(log)
            print(str(log) + "is created")
        output_file = log + "/" + "log.html"
        args = Namespace(
            device=devices,
            log=run_log,
            recording=record,
            script=case,
            compress=20,
            no_image=False,
        )
        try:
            run_script(args, AirtestCase)
        except (AirtestError, PocoException):
            pass
        finally:
            rpt = report.LogToHtml(
                case,
                run_log,
                script_name=air_name.replace(".air", ".py"),
                static_root=static_dir,
                plugins=["utx.mod.report.seleniumui", "utx.mod.report.pocoui"],
            )
            rpt.report("log_template.html", output_file=output_file, base_dir=base_dir)
            result = {"name": air_name.replace(".air", ""), "result": rpt.test_result}
        try:
            stop_app(app_name)
            time.sleep(2)
            start_app(app_name)
            time.sleep(2)
        except DeviceConnectionError:
            pass

        return result, dev


def run_web_air(
    case,
    log_path,
    case_path,
    base_dir,
    static_dir=decryption("aHR0cHM6Ly9jZG4ub3BlbnV0eC5jbi9jL3N0YXRpYw=="),
):
    """

    :param case:
    :param log_path:
    :param case_path:
    :param base_dir:
    :param static_dir:
    :return:
    """
    dev = "chrome"
    time.sleep(2)

    if os.path.isdir(log_path):
        pass
    else:
        os.makedirs(log_path)
        print(str(log_path) + "is created")

    if str(case).endswith(".air"):
        if plat() == "Windows":
            air_name = str(case).split("\\")[-1]
        else:
            air_name = str(case).split("/")[-1]
        print(case)
        log = os.path.join(log_path + "/" + dev + "/" + air_name.replace(".air", ""))

        run_log = case + "/" + "log" + "/" + dev
        if not os.path.exists(run_log):
            os.makedirs(run_log)
        print(log)
        if os.path.isdir(log):
            pass
        else:
            os.makedirs(log)
            print(str(log) + "is created")
        output_file = log + "/" + "log.html"
        args = Namespace(
            device=None,
            log=run_log,
            recording=None,
            script=case,
            compress=20,
            no_image=False,
        )
        try:
            run_script(args, AirtestCase)
        except UTXError:
            pass
        finally:
            rpt = report.LogToHtml(
                case,
                run_log,
                script_name=air_name.replace(".air", ".py"),
                static_root=static_dir,
                plugins=["utx.mod.report.seleniumui", "utx.mod.report.pocoui"],
            )
            rpt.report("log_template.html", output_file=output_file, base_dir=base_dir)
            result = {"name": air_name.replace(".air", ""), "result": rpt.test_result}

        return result, dev


def run_multi_air(
    devices: list,
    air: list,
    run_all=False,
    gen_report=False,
    suites_path=None,
    report_path=None,
):
    """
    run_all
            = True: run test fully
            = False: continue test with the progress in data.json
    :param report_path: report path
    :param suites_path: test script path
    :param devices: device list
    :param air: test script name
    :param run_all: True or False
    :param gen_report: True or False
    :return:
    """
    try:
        results = load_json_data(air, run_all, suites_path)
        tasks = run_on_multi_device(devices, air, results, run_all, suites_path)
        for task in tasks:
            status = task["process"].wait()
            results["tests"][task["dev"]] = gen_one_report(task["air"], task["dev"])
            results["tests"][task["dev"]]["status"] = status
            json.dump(results, open("data.json", "w"), indent=4)
        if gen_report:
            gen_summary(results, report_path)
    except UTXError:
        traceback.print_exc()


def run_on_multi_device(devices, air, results, run_all, suites_path=None):
    """
    Run airtest on multi-device
    :param suites_path: test script path
    :param devices: device list
    :param air: test script name
    :param results: progress data
    :param run_all: True or False
    :return: run tasks process
    """
    tasks = []
    for dev in devices:
        if (
            not run_all
            and results["tests"].get(dev)
            and results["tests"].get(dev).get("status") == 0
        ):
            print("Skip device %s" % dev)
            continue
        log_dir = get_log_dir(dev, air, suites_path)
        cmd = [air_cmd, "run", air, "--device", "Android:///" + dev, "--log", log_dir]
        try:
            tasks.append(
                {
                    "process": subprocess.Popen(cmd, cwd=suites_path),
                    "dev": dev,
                    "air": air,
                }
            )
        except subprocess.SubprocessError:
            traceback.print_exc()
    return tasks
