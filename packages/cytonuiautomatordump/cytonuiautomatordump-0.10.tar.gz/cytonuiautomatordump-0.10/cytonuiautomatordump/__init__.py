try:
    from .cyuiautomatordump import *

except Exception as e:
    import Cython, setuptools, numpy, pandas, platform, subprocess, os, sys, time, xmlhtml2pandas, cythonscreencap2ppm, cythondfprint, exceptdrucker

    iswindows = "win" in platform.platform().lower()
    if iswindows:
        addtolist = []
    else:
        addtolist = ["&"]

    olddict = os.getcwd()
    dirname = os.path.dirname(__file__)
    os.chdir(dirname)
    compile_file = os.path.join(dirname, "cyuiautomatordump_compile.py")
    subprocess.run(
        " ".join([sys.executable, compile_file, "build_ext", "--inplace"] + addtolist),
        shell=True,
        env=os.environ,
        preexec_fn=None if iswindows else os.setpgrp,
    )
    if not iswindows:
        time.sleep(30)
    from .cyuiautomatordump import *

    os.chdir(olddict)
