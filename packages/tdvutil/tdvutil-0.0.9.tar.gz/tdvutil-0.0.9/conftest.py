# flake8: noqa
import os

print("load conftest")
# deprecated hook, but it works
# def pytest_cmdline_preparse(config, args):
#     print("preparse")
#     for i, arg in enumerate(args):
#         if "@rootdir@" in arg:
#             newpath = arg.replace("@rootdir@", str(config.rootdir))
#             args[i] = os.path.normpath(newpath)

def pytest_html_report_title(report):
    report.title = "TDVUtil Test Report"
