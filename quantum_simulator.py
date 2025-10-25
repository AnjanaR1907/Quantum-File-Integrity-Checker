from flask import Flask, render_template_string, request
import numpy as np
import hashlib
import matplotlib.pyplot as plt
import io, base64, json, os

app = Flask(__name__)
DB_FILE = "fingerprints.json"

# Ensure DB exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

# Quantum-inspired encoding (deterministic for consistency)
def quantum_encode(data_bytes):
    arr = np.array([b / 255.0 for b in data_bytes])
    norm = np.linalg.norm(arr)
    return arr / norm if norm != 0 else arr

def quantum_hash(state):
    n = len(state)
    hadamard = np.ones(n) / np.sqrt(n)
    phase = np.exp(1j * 2 * np.pi * np.arange(n)/n)  # deterministic phase
    transformed = state * hadamard * phase
    return np.abs(np.sum(transformed)) % 1

def classical_hash(data_bytes):
    return hashlib.sha256(data_bytes).hexdigest()

# Plot graphs
def plot_signatures(qsig_old, qsig_new, state_old, state_new):
    fig, axs = plt.subplots(1, 2, figsize=(10, 3))

    # Bar chart
    axs[0].bar(['Original', 'Current'], [qsig_old, qsig_new], color=['#00cc99', '#ff9933'])
    axs[0].set_title('Quantum Signature Comparison')
    axs[0].set_ylabel('Signature Value')
    axs[0].grid(alpha=0.3)

    # Line chart
    axs[1].plot(state_old, color='#00cc99', label='Original')
    axs[1].plot(state_new, color='#ff9933', label='Current')
    axs[1].set_title('Quantum Amplitude Distribution')
    axs[1].set_xlabel('Byte Index')
    axs[1].set_ylabel('Amplitude Value')
    axs[1].legend()
    axs[1].grid(alpha=0.3)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    img_data = None
    db = load_db()
    if request.method == 'POST':
        file = request.files['file']
        action = request.form['action']
        if file:
            filename = file.filename
            data = file.read()
            qsig_new = quantum_hash(quantum_encode(list(data)))
            chash_new = classical_hash(data)
            state_new = quantum_encode(list(data))

            if action == "register":
                db[filename] = {'quantum': qsig_new, 'sha256': chash_new}
                save_db(db)
                result = f"File '{filename}' registered successfully ✅"
            elif action == "verify":
                if filename not in db:
                    result = f"File '{filename}' not found in database ⚠️"
                else:
                    old_qsig = db[filename]['quantum']
                    old_sha = db[filename]['sha256']
                    qdiff = abs(old_qsig - qsig_new)
                    integrity = 'Intact ✅' if qdiff < 0.0001 else 'Tampered ⚠️'
                    sha_match = (old_sha == chash_new)
                    result = {
                        'integrity': integrity,
                        'quantum_diff': round(qdiff,6),
                        'sha_match': sha_match
                    }
                    # Use the original file hash to reconstruct approximate state for visualization
                    old_state = quantum_encode([int(c,16) for c in old_sha[:len(state_new)]])
                    img_data = plot_signatures(old_qsig, qsig_new, old_state, state_new)
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Quantum File Integrity Checker</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#f0f2f5;}
.container{max-width:700px;margin-top:50px;padding:30px;background:white;border-radius:10px;box-shadow:0 0 20px rgba(0,0,0,0.1);}
h1{color:#0077cc;margin-bottom:30px;}
img{margin-top:20px;border-radius:5px;box-shadow:0 0 10px rgba(0,0,0,0.2);}
</style>
</head>
<body>
<div class="container text-center">
<h1>Quantum File Integrity Checker</h1>
<form method="post" enctype="multipart/form-data">
<div class="mb-3">
<input type="file" class="form-control" name="file" required>
</div>
<button class="btn btn-primary me-2" name="action" value="register">Register File</button>
<button class="btn btn-success" name="action" value="verify">Verify File</button>
</form>
<hr>
{% if result %}
    {% if result is string %}
        <h4 class="text-success">{{result}}</h4>
    {% else %}
        <h4>Integrity: <span class="{{ 'text-success' if result['integrity']=='Intact ✅' else 'text-danger' }}">{{result['integrity']}}</span></h4>
        <p>Quantum Signature Difference: {{result['quantum_diff']}}</p>
        <p>SHA-256 Match: {{'Yes' if result['sha_match'] else 'No'}}</p>
        {% if img_data %}<img src="data:image/png;base64,{{img_data}}" width="600">{% endif %}
    {% endif %}
{% endif %}
</div>
</body>
</html>
''', result=result, img_data=img_data)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)
