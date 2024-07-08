
import os

PROFILE_ENABLED = os.getenv('LINE_PROFILE', '0') == '1'

if PROFILE_ENABLED:
    # from line_profiler import profile

    from line_profiler import LineProfiler
    profile = LineProfiler()
else:
    def profile(func): return func

_ = profile



