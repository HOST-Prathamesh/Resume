# =========================================
# ACCURATE GRAPHS FROM NUMERIC CBC DATA
# Source: cbc_report.html (Patient 3114)
# Using mathematically defined parameters only
# =========================================

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1️⃣ RBC Distribution Curve
# Using:
# MCV = 87.9 fL
# RDW-CV = 13.2 %
# Formula: RDW-CV = (SD / MCV) × 100
# Therefore SD = (RDW-CV × MCV) / 100
# -----------------------------

MCV = 87.9
RDW_CV = 13.2

rbc_sd = (RDW_CV * MCV) / 100

x_rbc = np.linspace(0, 200, 1000)
rbc_curve = (1 / (rbc_sd * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_rbc - MCV) / rbc_sd) ** 2)

plt.figure()
plt.plot(x_rbc, rbc_curve)
plt.title("RBC Volume Distribution Curve")
plt.xlabel("Cell Volume (fL)")
plt.ylabel("Relative Frequency")
plt.show()


# -----------------------------
# 2️⃣ PLT Distribution Curve
# Using:
# MPV = 7.8 fL (mean platelet volume)
# PDW = 9.2 fL (treated as SD since unit is fL)
# -----------------------------

MPV = 7.8
PDW = 9.2

plt_sd = PDW

x_plt = np.linspace(0, 30, 1000)
plt_curve = (1 / (plt_sd * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_plt - MPV) / plt_sd) ** 2)

plt.figure()
plt.plot(x_plt, plt_curve)
plt.title("Platelet Volume Distribution Curve")
plt.xlabel("Platelet Volume (fL)")
plt.ylabel("Relative Frequency")
plt.show()


# -----------------------------
# 3️⃣ WBC Differential Distribution (Pie Chart)
# Using exact percentage values
# -----------------------------

labels = ["Neutrophils", "Lymphocytes", "Monocytes", "Eosinophils", "Basophils"]
sizes = [64.1, 26.7, 6.9, 1.8, 0.5]

plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title("WBC Differential Distribution")
plt.show()

print("Accurate graphs generated from numeric CBC parameters.")
