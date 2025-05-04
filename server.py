from flask import Flask, request, send_file, send_from_directory
import os
import subprocess
import tempfile

app = Flask(__name__)

@app.route('/build', methods=['POST'])
def build():
    with tempfile.TemporaryDirectory() as build_dir:
        for file in request.files.getlist('files'):
            path = os.path.join(build_dir, file.filename)
            file.save(path)

        files = os.listdir(build_dir)
        source_files = [f for f in files if f.endswith(('.c', '.s', '.S', '.cpp', '.h'))]
        ld_files = [f for f in files if f.endswith('.ld')]

        print('src:', source_files)
        print('ld:', ld_files)

        if not ld_files:
            return 'Linker script missing (.ld)', 400
        ld_script = ld_files[0]

        obj_path = os.path.join(build_dir, 'out.elf')
        hex_path = os.path.join(build_dir, 'out.hex')

        cmd = [
            'arm-none-eabi-g++',
            '-O0', '-mcpu=cortex-m4', '-mthumb', '-mfpu=fpv4-sp-d16', '-mfloat-abi=hard', '-nostdlib',
            f'-T{ld_script}',
            *source_files,
            '-o', obj_path
        ]
        result = subprocess.run(cmd, cwd=build_dir, capture_output=True)

        if result.returncode != 0:
            return f'Compile error:\n{result.stderr.decode()}', 400

        subprocess.run([
            'arm-none-eabi-objcopy', '-O', 'ihex', obj_path, hex_path
        ], cwd=build_dir)

        return send_file(hex_path, as_attachment=True, download_name='program.hex')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
