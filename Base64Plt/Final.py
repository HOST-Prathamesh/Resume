import re
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# =========================
# CONFIG
# =========================
INPUT_FILE = r"C:\Users\Prathamesh\Documents\Resume\Base64Plt\3106.txt"   # change for new file
OUTPUT_FOLDER = "cbc_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================
# CLEAN CONTROL CHARACTERS
# =========================
def clean_line(line):
    return re.sub(r'[^\x20-\x7E]', '', line)

# =========================
# PARSE NUMERIC RESULTS
# =========================
def parse_numeric_results(file_path):
    results = {}

    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()

    for line in lines:
        line = clean_line(line)

        if "R|" in line:
            parts = line.split("|")

            if len(parts) > 4:
                test_name = parts[2].replace("^^^", "").strip()

                try:
                    value = float(parts[3])
                    results[test_name] = value
                except:
                    continue

    return results


results = parse_numeric_results(INPUT_FILE)

print("\nExtracted Parameters:")
for k, v in results.items():
    print(k, "=", v)

# =========================
# RBC CURVE
# =========================
def generate_rbc_curve(results):
    if "MCV" not in results or "RDW-CV" not in results:
        return None

    MCV = results["MCV"]
    RDW = results["RDW-CV"]
    sd = (RDW * MCV) / 100

    x = np.linspace(0, 200, 1000)
    y = (1 / (sd * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - MCV) / sd) ** 2)

    path = os.path.join(OUTPUT_FOLDER, "rbc_curve.png")

    plt.figure()
    plt.plot(x, y)
    plt.title("RBC Volume Distribution")
    plt.xlabel("Cell Volume (fL)")
    plt.ylabel("Relative Frequency")
    plt.savefig(path)
    plt.close()

    return "rbc_curve.png"


# =========================
# PLT CURVE
# =========================
def generate_plt_curve(results):
    if "MPV" not in results or "PDW" not in results:
        return None

    MPV = results["MPV"]
    SD = results["PDW"]

    x = np.linspace(0, 30, 1000)
    y = (1 / (SD * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - MPV) / SD) ** 2)

    path = os.path.join(OUTPUT_FOLDER, "plt_curve.png")

    plt.figure()
    plt.plot(x, y)
    plt.title("Platelet Volume Distribution")
    plt.xlabel("Platelet Volume (fL)")
    plt.ylabel("Relative Frequency")
    plt.savefig(path)
    plt.close()

    return "plt_curve.png"


# =========================
# WBC PIE
# =========================
def generate_wbc_pie(results):
    keys = ["NEU%", "LYM%", "MON%", "EOS%", "BAS%"]

    labels = []
    values = []

    for k in keys:
        if k in results:
            labels.append(k.replace("%", ""))
            values.append(results[k])

    if not values:
        return None

    path = os.path.join(OUTPUT_FOLDER, "wbc_pie.png")

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("WBC Differential Distribution")
    plt.savefig(path)
    plt.close()

    return "wbc_pie.png"


rbc_img = generate_rbc_curve(results)
plt_img = generate_plt_curve(results)
wbc_img = generate_wbc_pie(results)

# =========================
# GENERATE HTML
# =========================
report_path = os.path.join(OUTPUT_FOLDER, "cbc_report.html")

with open(report_path, "w") as f:
    f.write(f"""
    <html>
    <head><title>CBC Report</title></head>
    <body>
    <h1>CBC Automated Report</h1>
    <p>Generated: {datetime.now()}</p>

    <h2>Numeric Results</h2>
    <table border="1" cellpadding="5">
    """)

    for k, v in results.items():
        f.write(f"<tr><td>{k}</td><td>{v}</td></tr>")

    f.write("</table>")

    if rbc_img:
        f.write(f"<h2>RBC Curve</h2><img src='{rbc_img}' width='600'>")

    if plt_img:
        f.write(f"<h2>Platelet Curve</h2><img src='{plt_img}' width='600'>")

    if wbc_img:
        f.write(f"<h2>WBC Distribution</h2><img src='{wbc_img}' width='600'>")

    f.write("</body></html>")

print("\nReport Generated Successfully.")
print("Open:", report_path)
