from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/clip', methods=['POST'])
def clip():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        # Create a temporary output directory
        with tempfile.TemporaryDirectory() as output_dir:
            # Build the AutoCut CLI command
            command = [
                "python", "-m", "autocut",
                "-i", url,
                "-o", output_dir
            ]

            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode != 0:
                return jsonify({'status': 'error', 'message': result.stderr}), 500

            return jsonify({'status': 'success', 'output': result.stdout})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
