#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  9/14/2021 4:36 PM
@Desc    :  Custom Report line.
"""
import json
import os
import shutil
import subprocess
import sys
import time
import traceback

import jinja2
from jinja2 import Environment
from jinja2 import FileSystemLoader

air_cmd = os.path.join(os.path.dirname(sys.executable), "airtest")

CUSTOM_HTML_TPL = "summary_template_v2.html"
CONCURRENT_HTML_TPL = "concurrent_template.html"
CUSTOM_STATIC_DIR = os.path.dirname(__file__)


def gen_report(results=None, report_path=None, report_name="utx_summary.html"):
    """
    gen_report
    :param report_name: custom name
    :param results: results list
    :param report_path: report_path
    :return: custom report html
    """
    format_list = []
    for i in results:
        if i not in format_list:
            format_list.append(i)

    for f in format_list:
        result = []
        for res in f["result"]:
            if res not in result:
                result.append(res)
        f["result"] = result

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(CUSTOM_STATIC_DIR),
        extensions=(),
        autoescape=True,
    )
    template = env.get_template(CUSTOM_HTML_TPL, CUSTOM_STATIC_DIR)
    html = template.render({"results": format_list})
    output_file = os.path.join(report_path, report_name)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(output_file)


def gen_one_report(air, dev):
    """
    Build one test report for one air script
    :param air: test script
    :param dev: device
    :return: report data dict
    """
    try:
        log_dir = get_log_dir(dev, air)
        log = os.path.join(log_dir, "log.txt")
        if os.path.isfile(log):
            cmd = [
                air_cmd,
                "report",
                air,
                "--log_root",
                log_dir,
                "--outfile",
                os.path.join(log_dir, "log.html"),
                "--lang",
                "zh",
            ]
            ret = subprocess.call(cmd, cwd=os.path.join(os.getcwd(), "suites"))
            return {"status": ret, "path": os.path.join(log_dir, "log.html")}
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except subprocess.SubprocessError:
        traceback.print_exc()
    return {"status": -1, "device": dev, "path": ""}


def gen_summary(data, report_path=None, report_name="utx_summary.html"):
    """
    Build summary test report
    :param data: test data
    :param report_path: report path
    :param report_name: report name
    :return:
    """
    try:
        summary = {
            "time": "%.3f" % (time.time() - data["start"]),
            "success": [item["status"] for item in data["tests"].values()].count(0),
            "count": len(data["tests"]),
        }
        summary.update(data)
        summary["start"] = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(data["start"])
        )
        env = Environment(loader=FileSystemLoader(os.getcwd()), trim_blocks=True)
        html = env.get_template(CONCURRENT_HTML_TPL, CUSTOM_STATIC_DIR).render(
            data=summary
        )
        output_file = os.path.join(report_path, report_name)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(output_file)
    except subprocess.SubprocessError:
        traceback.print_exc()


def clear_log_dir(air, suites_path=None):
    """
    Remove folder test_blackjack.air/log
    :param air: test script name
    :param suites_path: test script path
    :return: None
    """
    log = os.path.join(suites_path, air, "log")
    if os.path.exists(log):
        shutil.rmtree(log)


def load_json_data(air, run_all, suites_path=None):
    """
    Loading data
            if data.json exists and run_all=False, loading progress in data.json
            else return an empty data
    :param suites_path: test script path
    :param air: test script name
    :param run_all: True or False
    :return: progress data
    """
    json_file = os.path.join(suites_path, "data.json")
    if (not run_all) and os.path.isfile(json_file):
        data = json.load(open(json_file))
        data["start"] = time.time()
        return data
    else:
        clear_log_dir(air)
        return {"start": time.time(), "script": air, "tests": {}}


def get_log_dir(device, air, suites_path=None):
    """
    Create log folder based on device name under test_cases.air/log/
    :param device: device name
    :param air: test script name
    :param suites_path: test script path
    :return: log folder path
    """
    log_dir = os.path.join(
        suites_path, air, "log", device.replace(".", "_").replace(":", "_")
    )
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir
