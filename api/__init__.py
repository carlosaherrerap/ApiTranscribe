# Package initializer for api module
import os
if os.name == "nt":
    os.environ["WHISPER_NO_LIBC"] = "1"
