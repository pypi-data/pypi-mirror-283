import cython
cimport cython
import numpy as np
cimport numpy as np
np.import_array()
import subprocess
import re
import pandas as pd
from functools import cache
import os
from xmlhtml2pandas import parse_xmlhtml
from cythonscreencap2ppm import (
    Screencaptaker,
    mount_memory_disk,
    unmount_memory_disk,
)
from cythondfprint import add_printer 
import time
from exceptdrucker import errwrite
add_printer(1)
df_number_regex = re.compile(r"\d+", flags=re.I)
df_bounds_split_regex = re.compile(r"(?:(?:\]\[)|(?:,))", flags=re.I)
df_empty_regex = re.compile(r"^\s*$", flags=re.I)
numberre = re.compile(rb"^[0-9]+$", flags=re.I)


def cropimage(np.ndarray img, tuple coords):
    """
    Crops an image to the specified coordinates.

    Parameters:
    img (np.ndarray): The image to crop.
    coords (tuple): The coordinates (x1, y1, x2, y2) to crop the image.

    Returns:
    np.ndarray or pd.NA: The cropped image or pd.NA if an error occurs.
    """
    try:
        return img[coords[1] : coords[3], coords[0] : coords[2]]
    except Exception:
        return pd.NA


def create_memdisk_and_screenshot_instance(
    str memdiskpath="/media/ramdisk",
    int mb=256,
    str su="su",
    str sh="sh",
    cython.bint try_all_rw_remount_combinations=False,
    int screen_width=0,
    int screen_height=0,
):
    """
    Creates a memory disk and an instance of Screencaptaker.

    Parameters:
    memdiskpath (str): The path to the memory disk.
    mb (int): The size of the memory disk in MB.
    su (str): The superuser command.
    sh (str): The shell command.
    try_all_rw_remount_combinations (bool): Whether to try all read-write remount combinations.
    screen_width (int): The width of the screen.
    screen_height (int): The height of the screen.

    Returns:
    Screencaptaker: An instance of Screencaptaker.
    """
    if not os.path.exists(memdiskpath):
        mount_memory_disk(
            path=memdiskpath,
            mb=mb,
            su=su,
            sh=sh,
            try_all_combinations=try_all_rw_remount_combinations,
        )

    return Screencaptaker(
        path=memdiskpath,
        mb=mb,
        sh=sh,
        pure_shot="pure_shot.raw",
        converted_shot="converted_shot.ppm",
        width=screen_width,
        height=screen_height,
        max_color_value=255,
    )


def get_pid(str package, cython.bint shell=True):
    """
    Gets the process ID (PID) of a given package.

    Parameters:
    package (str): The package name.
    shell (bool): Whether to use the shell in the subprocess.

    Returns:
    int: The PID of the package.

    Raises:
    Exception: If the PID cannot be found.
    """
    p1 = subprocess.run(
        f'pgrep "{package}"', shell=shell, env=os.environ, capture_output=True
    )
    if not numberre.match(p1.stdout.strip()):
        raise Exception(f"Could not find pid of {package}")
    return int(p1.stdout.decode("utf-8").strip())


def limit_cpu_percentage_of_process(int pid, int percentage=10, cython.bint shell=True):
    """
    Limits the CPU usage of a process to a specified percentage.

    Parameters:
    pid (int): The process ID.
    percentage (int): The CPU usage limit percentage.
    shell (bool): Whether to use the shell in the subprocess.

    Returns:
    subprocess.Popen: The process limiting the CPU usage.
    """
    cpulimitcmd = f"cpulimit -l {percentage} -i -p {pid}"
    return subprocess.Popen(cpulimitcmd, shell=shell, env=os.environ)


def get_uiautomator_dump(
    str memdiskpath="/media/ramdisk",
    int uiautomator_nice=-20,
    float sleep_between_retries=0.3,
    cython.bint shell=True,
    int timeout=20,
):
    """
    Gets a UI Automator dump and saves it to the specified memory disk path.

    Parameters:
    memdiskpath (str): The path to the memory disk.
    uiautomator_nice (int): The nice value for UI Automator.
    sleep_between_retries (float): The sleep time between retries.
    shell (bool): Whether to use the shell in the subprocess.
    timeout (int): The timeout for the subprocess.

    Returns:
    bool: True if the dump was successful, False otherwise.
    """
    outputdump = f"{memdiskpath}/window_dump.xml"

    scr = rf"""
    rm -f {outputdump}
    while true; do
        nice -n {uiautomator_nice} uiautomator dump {outputdump}
        sleep {sleep_between_retries}
        if [ -f {outputdump} ]; then
                break
        fi
    done""".encode("utf-8")
    try:
        subprocess.run(
            "sh",
            input=scr,
            shell=shell,
            env=os.environ,
            timeout=timeout,
            capture_output=True,
        )
        return True
    except Exception as e:
        errwrite()
    return False


@cache
def bounds_split_to_int(x):
    """
    Splits a string of bounds into a tuple of integers.

    Parameters:
    x (str): The string containing bounds.

    Returns:
    tuple: A tuple of integers representing the bounds.
    """
    return tuple(map(int, df_bounds_split_regex.split(str(x).strip(r"[] "))))


@cache
def format_cols(col):
    """
    Formats a column name by converting it to lowercase and replacing hyphens with underscores.

    Parameters:
    col (str): The column name.

    Returns:
    str: The formatted column name.
    """
    col = str(col).lower().replace("-", "_")
    if not col.startswith("aa_"):
        return f"aa_{col}"
    return col


def get_cyuiautomator_dump(
    str package, # com.instagram.android
    str memdisk_path="/media/ramdisk",
    int memdisk_size=256,
    str memdisk_su="su",
    str memdisk_sh="sh",
    cython.bint memdisk_try_all_rw_remount_combinations=False,
    int max_cpu_percentage_for_process=10,
    float sleep_after_starting_cpu_limiter=0.1,
    cython.bint add_screenshot=True,
    int screen_width=0,
    int screen_height=0,
    cython.bint debug=False,
    int uiautomator_nice=-20,
    float uiautomator_sleep_between_retries=0.3,
    cython.bint uiautomator_shell=True,
    int uiautomator_timeout=20,
):
    """
    Gets a UI Automator dump, processes it, and returns the result as a DataFrame.

    Parameters:
    package (str): The package name.
    memdisk_path (str): The path to the memory disk.
    memdisk_size (int): The size of the memory disk in MB.
    memdisk_su (str): The superuser command.
    memdisk_sh (str): The shell command.
    memdisk_try_all_rw_remount_combinations (bool): Whether to try all read-write remount combinations.
    max_cpu_percentage_for_process (int): The maximum CPU usage percentage for the process.
    sleep_after_starting_cpu_limiter (float): The sleep time after starting the CPU limiter.
    add_screenshot (bool): Whether to add a screenshot to the DataFrame.
    screen_width (int): The width of the screen.
    screen_height (int): The height of the screen.
    debug (bool): Whether to enable debug mode.
    uiautomator_nice (int): The nice value for UI Automator.
    uiautomator_sleep_between_retries (float): The sleep time between retries for UI Automator.
    uiautomator_shell (bool): Whether to use the shell in the subprocess.
    uiautomator_timeout (int): The timeout for UI Automator.

    Yields:
    pd.DataFrame: The processed UI Automator dump as a DataFrame.
    """
    cdef:
        str outputdump
        np.ndarray badcols, allcols, grcolsarra, attrsarray, badindis
        dict[Py_ssize_t, str] rename_cols1
        list allresus, allresus2
        np.ndarray dummyarray, parsed_image
        int limit_cpu_of_process, pid
        cython.bint dumpok
        float total_screenarea = float(screen_width) * float(screen_height)

    outputdump = f"{memdisk_path}/window_dump.xml"
    badcols = np.array([
        "aa_attrib_keys",
        "aa_attrib_values",
        "aa_elem",
        "aa_previous",
        "aa_sourceline",
        "aa_text",
        "aa_all_text",
        "aa_all_text_len",
        'aa_all_html','aa_tag'
    ])
    rename_cols1 = {
        0: "start_x",
        1: "start_y",
        2: "end_x",
        3: "end_y",
    }
    allresus = []
    allresus2 = []
    screencapper = create_memdisk_and_screenshot_instance(
        memdiskpath=memdisk_path,
        mb=memdisk_size,
        su=memdisk_su,
        sh=memdisk_sh,
        try_all_rw_remount_combinations=memdisk_try_all_rw_remount_combinations,
        screen_width=screen_width,
        screen_height=screen_height,
    )
    screen_width, screen_height = screencapper.width, screencapper.height
    total_screenarea = float(screen_width) * float(screen_height)
    dummyarray = np.array([], dtype=np.uint8)
    limit_cpu_of_process = max_cpu_percentage_for_process >= 100
    allcols = np.array(["index", 
    "NAF",
    "text",
    "resource-id",
    "class",
    "package",
    "content-desc",
    "checkable",
    "checked",
    "clickable",
    "enabled",
    "focusable",
    "focused",
    "scrollable",
    "long-clickable",
    "password",
    "selected",
    "bounds","rotation"])
    while True:
        try:
            if package:
                pid = get_pid(package=package, shell=True)
            else:
                pid = 0
            if limit_cpu_of_process and pid > 0:
                limitproc = limit_cpu_percentage_of_process(
                    pid, percentage=max_cpu_percentage_for_process, shell=True
                )
            else:
                limitproc = None
            if add_screenshot:
                parsed_image = screencapper.get_screenshot_as_np()
            else:
                parsed_image = dummyarray
            time.sleep(sleep_after_starting_cpu_limiter)
            dumpok = False
            try:
                dumpok = get_uiautomator_dump(
                    memdiskpath=memdisk_path,
                    uiautomator_nice=uiautomator_nice,
                    sleep_between_retries=uiautomator_sleep_between_retries,
                    shell=uiautomator_shell,
                    timeout=uiautomator_timeout,
                )
            except Exception:
                if debug:
                    errwrite()
                yield pd.DataFrame()
            finally:
                if limit_cpu_of_process and pid > 0:
                    try:
                        limitproc.kill()
                    except Exception:
                        if debug:
                            errwrite()

            if not dumpok:
                continue

            if dumpok and os.path.exists(outputdump):
                with open(
                    outputdump,
                    "rb",
                ) as fxx:
                    allresus.clear()
                    allresus2.clear()
                    for name, group in parse_xmlhtml(fxx, "xml", ()).groupby("aa_elem"):
                        if debug:
                            print(name)
                            print(group)
                        attrsarray = group["aa_attrib_keys"].__array__()
                        allresus.append( (
                            group[["aa_attrib_keys", "aa_attrib_values"]]
                            .set_index("aa_attrib_keys")
                            .T.reset_index(drop=True)
                            .replace({"true": True, "false": False})
                        ).assign(**{kk1: "" for kk1 in np.setdiff1d(allcols, attrsarray) },)
                        )
                        grcolsarra = group.columns.__array__()
                        allresus2.append(group.iloc[:1][np.setdiff1d(grcolsarra, badcols)])

                    dffix = pd.concat([pd.concat(allresus, ignore_index=True), pd.concat(allresus2, ignore_index=True)], axis=1)
                    if debug:
                        dffix.ds_color_print_all()
                    try:
                        if "rotation" in dffix.columns:
                            dffix.loc[:, "rotation"] = int(max((str(xx) for xx in (dffix.rotation.unique())), key=len))
                    except Exception:
                        if debug:
                            errwrite()
                    badindis = dffix.loc[
                        ~dffix["bounds"].str.contains(
                            '[', regex=False, na=False
                        )
                    ].index.__array__()
                    if len(badindis) > 0:
                        dffix.drop(badindis, inplace=True)
                    dffix.reset_index(drop=True, inplace=True)
                    dffi = pd.concat(
                        [
                            dffix,
                            dffix.bounds.apply(bounds_split_to_int)
                            .apply(pd.Series)
                            .rename(columns=rename_cols1),
                        ],
                        axis=1,
                    )
                    dffi.columns = [format_cols(col) for col in dffi.columns]
                    dffi.loc[:, "aa_width"] = dffi.aa_end_x - dffi.aa_start_x
                    dffi.loc[:, "aa_height"] = dffi.aa_end_y - dffi.aa_start_y
                    dffi.loc[:, "aa_center_x"] = dffi["aa_start_x"] + (dffi["aa_width"] // 2)
                    dffi.loc[:, "aa_center_y"] = dffi["aa_start_y"] + (dffi["aa_height"] // 2)
                    dffi.loc[:, "aa_area"] = dffi["aa_width"] * dffi["aa_height"]
                    dffi.loc[:,"aa_area_percent"] = (dffi["aa_area"] / total_screenarea) * 100.0
                    if add_screenshot:
                        dffi["aa_screenshot"] = dffi.apply(
                            lambda x: cropimage(
                                parsed_image,
                                (
                                    x["aa_start_y"],
                                    x["aa_start_x"],
                                    x["aa_end_y"],
                                    x["aa_end_x"],
                                ),
                            ),
                            axis=1,
                        )
                    if debug:
                        dffi.ds_color_print_all()
                    dffi.drop(columns='aa_bounds', inplace=True)
                    yield dffi.sort_values(by=["aa_myid", "aa_parent", 'aa_index']).reset_index(drop=True)

                try:
                    os.remove(outputdump)
                except Exception:
                    if debug:
                        errwrite()
                allresus.clear()
                allresus2.clear()
        except Exception:
            if debug:
                errwrite()
