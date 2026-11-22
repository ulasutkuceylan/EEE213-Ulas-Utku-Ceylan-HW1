"""Run all three EEE213 scripts with the same Python interpreter.

From repository root: python code/run_all.py
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ['lab/w09.py','lab/knn_project.py','code/numerical.py','code/verify_outputs.py']


def main():
    print('PROJECT ROOT:', ROOT,flush=True)
    print('PYTHON EXECUTABLE:', sys.executable,flush=True)
    for path in SCRIPTS:
        print('\n'+'='*70,flush=True)
        print('RUN:',sys.executable,path,flush=True)
        subprocess.run([sys.executable,path],cwd=ROOT,check=True)
    print('\nALL SCRIPTS RAN SUCCESSFULLY',flush=True)

if __name__=='__main__':
    main()
