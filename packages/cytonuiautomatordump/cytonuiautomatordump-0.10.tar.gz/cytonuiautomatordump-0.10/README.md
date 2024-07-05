# uiautomator parser for Android

### Tested against Bluestacks 5 / Python 3.11, directly in the terminal

### pip install cyuiautomatordump

### Cython and a C compiler must be installed!
### You also need to compile https://github.com/opsengine/cpulimit

```PY

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

from cytonuiautomatordump import get_cyuiautomator_dump



geni = get_cyuiautomator_dump(
    package= "com.instagram.android",
    memdisk_path="/media/ramdisk",
    memdisk_size=256,
    memdisk_su="su",
    memdisk_sh="sh",
    memdisk_try_all_rw_remount_combinations=False,
    max_cpu_percentage_for_process=10,
    sleep_after_starting_cpu_limiter=0.5,
    add_screenshot=False,
    screen_width=720,
    screen_height=1280,
    debug=False,
    uiautomator_nice=-19,
    uiautomator_sleep_between_retries=0.3,
    uiautomator_shell=True,
    uiautomator_timeout=20,
)
counter = 0
while True:
    df = next(geni)
    print(df)
    counter = counter + 1
    print(counter)

```