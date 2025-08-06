# This file is set up to profile the performance of various functions in the application.

import cProfile
import pstats
import io
import os
from datetime import datetime
from functools import wraps

# Central folder for all profile outputs
PROFILES = os.path.abspath(os.path.join(os.getcwd(), "profiles"))
os.makedirs(PROFILES, exist_ok=True)

def profile(func):
    """
    Decorator to profile a function with cProfile.
    Stores a .prof file and a top-20 stats .txt under profiles/.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"{func.__name__}_{timestamp}"
        prof_path = os.path.join(PROFILES, f"{base}.prof")
        txt_path  = os.path.join(PROFILES, f"{base}.txt")

        # Dump raw profile data
        pr.dump_stats(prof_path)

        # Write top-20 cumulative time stats
        s = io.StringIO()
        stats = pstats.Stats(pr, stream=s).sort_stats("cumtime")
        stats.print_stats(20)
        with open(txt_path, "w") as f:
            f.write(s.getvalue())

        return result

    return wrapper
