#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  8/17/2021 6:49 PM
@Desc    :  Command line.
"""
import argparse
import os
import random
import subprocess
import sys
from pprint import pprint

from loguru import logger

from utx import __description__
from utx import __version__
from utx.cli.func import deprecated
from utx.cli.scaffold import init_parser_install
from utx.cli.scaffold import init_parser_scaffold
from utx.cli.scaffold import init_parser_uninstall
from utx.cli.scaffold import main_install
from utx.cli.scaffold import main_scaffold
from utx.cli.scaffold import main_uninstall
from utx.cli.scaffold_web import init_parser_scaffold_web
from utx.cli.scaffold_web import main_scaffold_web
from utx.core.utils.tools import adb
from utx.core.utils.tools import check_port
from utx.core.utils.tools import decryption
from utx.core.utils.tools import get_host_ip
from utx.core.utils.tools import plat


def main():
    """Parse command line options and run commands."""
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_scaffold = init_parser_scaffold(subparsers)
    sub_parser_scaffold_web = init_parser_scaffold_web(subparsers)
    sub_parser_install = init_parser_install(subparsers)
    sub_parser_uninstall = init_parser_uninstall(subparsers)
    subparsers.add_parser(
        "test", help="debug iOS devices(UTX driver needs to be installed)."
    )

    subparsers.add_parser("adb", help="complete adb debugging capability.")
    subparsers.add_parser(
        "remote", help="open Android device remote debugging port(5555)."
    )
    subparsers.add_parser(
        "proxy", help=f"enable device global proxy({get_host_ip()}:8888)."
    )
    subparsers.add_parser("unproxy", help=f"disable device global proxy.")
    # show device info
    subparsers.add_parser("list", help="show connected iOS devices.")
    subparsers.add_parser("info", help="show current connected iOS device info.")
    subparsers.add_parser("applist", help="list packages on iOS devices.")

    if len(sys.argv) == 1:
        # utx
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-v", "--version"]:
            # utx -v
            print(f"{__version__}")
        elif sys.argv[1] == "test":
            # utx -test
            logger.info("UTX will connect your IOS device.")
            logger.warning(
                "Please make sure the IOS phone is connected to the computer and the UTX driver is installed!"
            )
            devices = "{} list".format(decryption(b"dGlkZXZpY2U="))
            d = os.popen(devices)
            if len(d.readlines()) == 0:
                logger.error("No device detected!")
                sys.exit()

            res = subprocess.run(
                "{} applist".format(decryption(b"dGlkZXZpY2U=")),
                shell=True,
                capture_output=True,
            )
            utx_driver = res.stdout.decode("utf-8", "ignore")

            if "WebDriverAgentRunner" not in utx_driver:
                logger.error("UTX driver(WDA.ipa) is not installed!")
                sys.exit()
            else:
                pass

            proxy = str(random.randint(50000, 60000) + 1)
            check_port(port=proxy)
            logger.info(f"Debug address:http://127.0.0.1:{proxy}")
            try:
                subprocess.call(
                    "{} wdaproxy --port {}".format(decryption(b"dGlkZXZpY2U="), proxy),
                    shell=True,
                )
            except KeyboardInterrupt:
                check_port(port=proxy)
                sys.exit()
            finally:
                if plat() != "Windows":
                    os.system("clear")
                else:
                    os.system("cls")
                logger.error("")
                logger.error("-------------------- utx end --------------------------")

                logger.error("Disconnect and end debugging!")

        elif sys.argv[1] == "remote":
            # utx remote
            os.system(f"{adb} tcpip 5555")

        elif sys.argv[1] == "proxy":
            # utx proxy
            os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5")} {get_host_ip()}:8888'
            )

        elif sys.argv[1] == "unproxy":
            # utx proxy
            os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5IDow")}'
            )

        elif sys.argv[1] == "adb":
            # utx adb
            os.system(f"{adb}")

        elif sys.argv[1] in ["-h", "--help"]:
            # utx -h
            parser.print_help()

        elif sys.argv[1] == "install":
            # utx install
            sub_parser_install.print_help()

        elif sys.argv[1] == "uninstall":
            # utx uninstall
            sub_parser_uninstall.print_help()

        elif sys.argv[1] == "list":
            # utx list
            os.system("{} list".format(decryption(b"dGlkZXZpY2U=")))

        elif sys.argv[1] == "info":
            # utx info
            os.system("{} info".format(decryption(b"dGlkZXZpY2U=")))

        elif sys.argv[1] == "applist":
            # utx applist
            os.system("{} applist".format(decryption(b"dGlkZXZpY2U=")))

        elif sys.argv[1] == "startproject":
            # utx startproject
            sub_parser_scaffold.print_help()

        elif sys.argv[1] == "startproject-web":
            # utx startproject-web
            sub_parser_scaffold_web.print_help()
        else:
            parser.print_help()
        sys.exit(0)

    elif sys.argv[1] == "adb":
        del sys.argv[0:2]
        args = " ".join([str(i) for i in sys.argv])
        os.system(f"{adb} {args}")
        sys.exit(0)

    args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)

    if sys.argv[1] == "startproject":
        main_scaffold(args)

    if sys.argv[1] == "startproject-web":
        main_scaffold_web(args)

    if sys.argv[1] == "install":
        main_install(args)

    if sys.argv[1] == "uninstall":
        main_uninstall(args)


@deprecated("cli_env_new()")
def cli_env():
    parser = argparse.ArgumentParser(description="manual to this script")
    parser.add_argument("--device", type=str)
    parser.add_argument("--platform", type=str)
    parser.add_argument("--wda", type=str)
    parser.add_argument("--init", type=str)

    args = parser.parse_args()
    cli_device = args.device
    cli_platform = args.platform
    cli_wda = args.wda
    cli_init = args.init

    return cli_device, cli_platform, cli_wda, cli_init


@deprecated("cli_env_new()")
def cli_env_v2():
    """
    cli param v2
    :return: param dict
    """
    parser = argparse.ArgumentParser(description="manual to this script cli_env v2")
    parser.add_argument("--device", type=str)
    parser.add_argument("--platform", type=str)
    parser.add_argument("--wda", type=str)
    parser.add_argument("--init", type=str)
    parser.add_argument("--package", type=str)
    parser.add_argument("--filename", type=str)
    parser.add_argument("--times", type=str)
    parser.add_argument("--name", type=str)
    parser.add_argument("--is_all", type=str)
    parser.add_argument("--record", type=str)
    parser.add_argument("--proxy", type=str)
    parser.add_argument("--cases", type=str)

    parser.add_argument("--duration", type=str)
    parser.add_argument("--whitelist", type=str)
    parser.add_argument("--throttle", type=str)
    parser.add_argument("--widget", type=str)

    args = parser.parse_args()
    device = args.device
    platform = args.platform
    wda = args.wda
    init = args.init
    package = args.package
    filename = args.filename
    times = args.times
    name = args.name
    is_all = args.is_all
    record = args.record
    proxy = args.proxy
    cases = args.cases

    duration = args.duration
    whitelist = args.whitelist
    throttle = args.throttle
    widget = args.widget

    cli_result = {
        "device": device,
        "platform": platform,
        "wda": wda,
        "init": init,
        "package": package,
        "filename": filename,
        "times": times,
        "name": name,
        "is_all": is_all,
        "record": record,
        "proxy": proxy,
        "cases": cases,
        "duration": duration,
        "whitelist": whitelist,
        "throttle": throttle,
        "widget": widget,
    }
    return cli_result


@deprecated("cli_env_new()")
def cli_web_env():
    parser = argparse.ArgumentParser(description="manual to this script")
    parser.add_argument("--headless", type=str)
    args = parser.parse_args()
    cli_headless = args.headless

    return cli_headless


def cli_env_new(*args, **kwargs):
    """
    the parameters currently used are as follows：

    device, platform, wda, init, duration, whitelist, widget, package, filename, times, name, is_all,
    record, proxy, cases, username, password, phone_numbers_api, save_mark_api, data, phone

    :param kwargs: additional parameters
    :return: param dict
    """
    parser = argparse.ArgumentParser(description="manual to this script.")
    args, unknown = parser.parse_known_args()
    # make sure that all the parameters are stored in a dictionary
    cli_result = vars(args)

    # handle undefined parameters
    for arg in unknown:
        arg_name, arg_value = arg.split("=")
        cli_result[arg_name.lstrip("-")] = arg_value

    # handle the undefined parameters passed in
    for key, value in kwargs.items():
        cli_result[key] = value

    pprint(cli_result)
    return cli_result
