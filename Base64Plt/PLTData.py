import re
import base64
import zlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d

# 🔹 Paste your FULL raw message exactly (including FLOATLE lines)
raw_message = """
4M|2|HISTOGRAM|PLT|PLTALONGRES|FLOATLE-stream/deflate:base64^Y2AAAQ4nMMXQA6IdgMghPS3IYdVHE8cFs1ihcg32IDkA|FLOATLE-stream/deflate:base64^zdQPTJR1HMfxR7gZ1Khj0hg5mjhFs0bEkkyK5/d5bsYYNHA0hg4bJkvGOidTJGPgiaYEJAapGBSXEKJBnXnKn4A4QwkMCiIkqIMg/hjUGFC
5RpKndXn8LaMkSvHWrd77273/Pl97/XcPZJkezgpUy9SFl91gm/YAkiSnl3CjW22z3ZotOYlgVa3Q4Gmld2BGsPdsrfGV3bqXC2Pxm2Rh1My5KigfLlJXSYHdNfIZUUtsqfWLGf7W2Tb8VWxTiKhSS2W+XiIgRwvkX/1AfFMtJ9wMa0UZxdrRGpGiHjMEiEsEdGitDJWrPfUCo+0RNE+lMLtu8TCqL3cJ1N012Rzv1yR65XHfDB
6QtE6B499y8WqtFSHlMuasNO8LhTYpuxisfWCh+PMyIj5JwYTmkWGkOrKOxvF1a3CyIqqEcYt/cK17IBoTUPiyb1mPDWXBJpiVeE+eg1EdBt5bklvFTogNJKFTrb5kI16gQ/1V1Y7+mCbP97UBvmitG4efBIuxdB+e7YZvRAcct8tA95wmZ4ed5CDC5ZhK4Ab5wPW4q6DctgSHoIRZk+OFjoi/STfkhufBSbevwRY1mBCMcAP32
7OX+JB5/UAafuD9CA9eNq+CYHISJfcG4eCQEPaefRmtzGEzm1TCOR6BkbiQO3xeFLJ+1SFWikRD5LGLjYxCZ+hyCc2LxRMnzeLg6Dl6t8XDrfwF3TGzCpHMCxjy3oPeRRLStSkLDmu2o0Cbj+M4UFBzYgcYOHc+/E9UjaVxjF8qtu7nOHujVe7lWOnIWvcL1MvDyikyumYUXQ1/luvsQH5PNtfdj3dbXuH4OwtNzOcPrUAoOcDB
0I6DWG44xFnysLThMOd5A/O78jlTAVzG3uRcb0395iad36bbEc5XRLtizvgO/Uo451EalnLWY3Q8znnfpWUZZy6n53uc+32aGpB97ARdP0Ba7UnaGrG17RR9T2PjYAWNK7F2sorOHyLUpYbWtZC96uj9EfyW19PchMXBZ+j+MdzXNdD+LO5MOEf/Rlzf/QmvQRMsec28DufRX/Ypr0ULvqxv5fX4jGaf06yNZu00+4JmHTTrpED
1NkFmnXR7CuaddOsh2Zf0+wbmplp1kuzPpp9S7N+mg3Q7DuaDdJsiGbDNBuh2UWafU+zUZqN0ewHmv049R+ddP6JZuM0u0yzKzT7mWYTNLtKs2s0m6TZLzT7lWZWml2n2W80+53bJaWxQ1Ia1sxRTOY5St0GB6V6xEGp0DoqxnFHxZCkUsqtKvs9YjYfOvmvSeLPhD3b/Uhvr5712ZP4vdX2bPcqX3vCXjiLsbf5pnQ3lT5D+DE
22+jmc5zu+mmtXmGYv6m8BkS0/Kd1oJpqW+RNIv1iX9W/S3Sz2K6/yDxL5L+J92Y5w8=
"""

def extract_and_plot_plt(raw_text):

    clean_text = re.sub(r'[\x00-\x1F]+', '', raw_text)

    base64_blocks = re.findall(r'base64\^([A-Za-z0-9+/=]+)', clean_text)

    if not base64_blocks:
        print("No Base64 found")
        return

    # ✅ Combine ALL decoded binary first
    combined_binary = b''

    for block in base64_blocks:
        block = block.strip()
        if len(block) % 4:
            block += '=' * (4 - len(block) % 4)

        combined_binary += base64.b64decode(block)

    # ✅ Decompress ONCE (very important)
    try:
        decompressed = zlib.decompress(combined_binary, -zlib.MAX_WBITS)
    except Exception as e:
        print("Decompression failed:", e)
        return
    
    print("Length of combined binary:", len(combined_binary))
    print("Length after decompression:", len(decompressed))
    print("Length % 4:", len(decompressed) % 4)

    histogram_data = np.frombuffer(decompressed, dtype='<f4')

    print("Total bins:", len(histogram_data))



    min_volume = 2
    max_volume = 30

    x_original = np.geomspace(2, 30, len(histogram_data))

    # Smooth X axis
    x_smooth = np.linspace(min_volume, max_volume, 400)

    # 🔥 Shape-preserving interpolation (NO overshoot)
    interp = PchipInterpolator(x_original, histogram_data)
    y_smooth = interp(x_smooth)

    # Light smoothing like firmware
    y_smooth = gaussian_filter1d(y_smooth, sigma=1.5)

    # Remove negative values
    y_smooth[y_smooth < 0] = 0

    # Normalize display
    y_smooth = y_smooth / np.max(y_smooth)

    # Plot like Horiba screen
    plt.figure()
    plt.plot(x_smooth, y_smooth, linewidth=2)

    plt.title("PLT Histogram")
    plt.xlabel("Platelet Volume (fL)")

    # 🔥 Horiba style: remove Y axis completely
    plt.yticks([])
    plt.ylabel("")

    # Remove grid
    plt.grid(False)

    # Show only main ticks
    plt.xticks([2, 10, 20, 30])

    plt.show()

    # plt.figure()
    # plt.plot(x_smooth, y_smooth)
    # plt.title("PLT Histogram")
    # plt.xlabel("Platelet Volume (fL)")
    # plt.ylabel("Frequency")
    # plt.xticks([2, 10, 20, 30])
    # plt.grid(True)
    # plt.show()


# Run
extract_and_plot_plt(raw_message)
