**Quantum File Integrity Checker**

The Quantum **File Integrity Checker** is a **quantum-inspired simulator** designed to detect unauthorized modifications in files. It combines **quantum amplitude encoding** and **classical SHA-256 hashing** to generate a unique “fingerprint” for each file and verify its integrity over time. Even a single-byte change can trigger a tampering alert.

This project features an **elegant web-based GUI** built with **Flask and Bootstrap**, allowing users to **register** files and **verify** them later. Graphs visualize the quantum signatures and amplitude distributions, making it easy to understand how the file has changed.

---

## ⚙️ Features

* **Quantum-Inspired Signature Calculation:** Detects subtle changes in files.
* **Classical SHA-256 Hash Verification:** Ensures additional integrity check.
* **Elegant GUI:** Modern Bootstrap-based interface.
* **Graphical Visualization:**

  * Bar chart of Original vs Current quantum signature
  * Line graph of amplitude distributions
* **Local Fingerprint Database:** Stores file fingerprints in `fingerprints.json`.
* **Single-File Workflow:** Register a file once, verify anytime.

---

## 💻 How to Run

1. **Install Python 3.8+**
2. **Install dependencies**:

```bash
pip install flask numpy matplotlib
```

3. **Run the script**:

```bash
python quantum_file_integrity_checker.py
```

4. **Your default browser will open** at `http://127.0.0.1:5000`.
5. **Upload a file**:

   * Click **Register File** → stores the quantum signature and SHA-256 hash.
   * Click **Verify File** → compares the current file with the stored fingerprint.
6. **Interpret Results**:

   * **Intact ✅** → file matches the original fingerprint.
   * **Tampered ⚠️** → file content has been modified.
   * **Graphs** show differences in quantum signatures and amplitude distribution.


## 🔬 How Integrity is Checked

1. **Quantum Signature:**

   * File bytes are normalized into a “quantum amplitude vector.”
   * Deterministic transformation produces a signature.
   * Any change in the file changes the signature significantly.

2. **SHA-256 Hash:**

   * Classical hashing ensures additional verification.

3. **Visualization:**

   * **Bar Chart:** Compares original vs current quantum signature.
   * **Line Graph:** Shows amplitude distribution changes across the file.

---

## ✅ Advantages

* Detects tampering even at the **byte level**.
* Works for **any file type**: text, images, binaries, PDFs.
* Offline, lightweight, and **easy to use**.
* Perfect for **digital forensics and cybersecurity demos**.

---

## 📷 Demo

**1. Registering a File:**

* Upload your file and click **Register File**.
* File fingerprint stored in `fingerprints.json`.

**2. Verifying a File:**

* Upload the same file again → shows **Intact ✅**.
* Modify the file slightly → shows **Tampered ⚠️** with signature difference and graphs.
