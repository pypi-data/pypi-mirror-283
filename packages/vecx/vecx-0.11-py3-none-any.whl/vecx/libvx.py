
import os
import platform
import ctypes

# TODO - put lru_cache here
def load_libvx():
    """Loads the correct C++ library based on the OS and architecture."""

    system = platform.system().lower()
    arch = platform.machine().lower()

    # Linux
    if system == "linux":
        if arch == "x86_64" or arch == "amd64":
            library_name = "libvx_x86_64.so"
        elif arch == "arm64" or arch == "aarch64":
            library_name = "libvx_arm64.so"
        else:
            raise Exception(f"Unsupported architecture for Linux: {arch}")
    # macOS (Darwin)
    elif system == "darwin":
        if arch == "x86_64":
            library_name = "libvx_x86_64.dylib"
        elif arch == "arm64":
            library_name = "libvx_arm64.dylib"
        else:
            raise Exception(f"Unsupported architecture for macOS: {arch}")
    # Windows
    # TODO - check for arm architecture in Windows
    # TODO - check for 32-bit architecture in Windows
    elif system == "windows":
        if arch == "amd64":  # 64-bit
            library_name = "libvx_x64.dll"
        elif arch == "x86":  # 32-bit
            library_name = "libvx_x86.dll"
        else:
            raise Exception(f"Unsupported architecture for Windows: {arch}")
    else:
        raise Exception(f"Unsupported operating system: {system}")

    # Ensure library file exists
    library_path = os.path.join(os.path.dirname(__file__), "libvx", library_name)
    if not os.path.exists(library_path):
        raise Exception(f"Library file not found: {library_path}")

    print(f"Loading library: {library_path}")

    # Load the library using ctypes
    vxlib = ctypes.cdll.LoadLibrary(library_path)
    return vxlib

# Define the argument and return types of the functions

# Define the function to encode a string
def encode(string, vector):
    libvx = load_libvx()
    libvx.encode.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
    libvx.encode.restype = None
    # Convert the string to a byte string
    string = string.encode('utf-8')
    # Convert the string to a c_char_p
    c_string = ctypes.c_char_p(string)
    vector_size = len(vector)
    c_vector = (ctypes.c_double * vector_size)(*vector)
    c_transformed_vector = (ctypes.c_double * vector_size)()
    # Call the function
    libvx.encode(c_string, c_vector, vector_size, c_transformed_vector)
    transformed_vector = list(c_transformed_vector)
    #print(transformed_vector)
    return transformed_vector

# Define the function to decode a string
def decode(string, vector):
    libvx = load_libvx()
    libvx.decode.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
    libvx.decode.restype = None
    # Convert the string to a byte string
    string = string.encode('utf-8')
    # Convert the string to a c_char_p
    c_string = ctypes.c_char_p(string)
    vector_size = len(vector)
    c_vector = (ctypes.c_double * vector_size)(*vector)
    c_transformed_vector = (ctypes.c_double * vector_size)()
    # Call the function
    libvx.decode(c_string, c_vector, vector_size, c_transformed_vector)
    transformed_vector = list(c_transformed_vector)
    return transformed_vector






