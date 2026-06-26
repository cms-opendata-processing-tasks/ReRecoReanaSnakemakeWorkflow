"""Patch runForest_pPb_DATA_53X_OD.py to read from a specific input file.

Usage: python patch_forest.py <forest_script.py> <input_reco_file>
Compatible with Python 2.7 and Python 3 (SLC6 container only has Python 2).
"""

import re
import sys

script_path = sys.argv[1]
input_file = sys.argv[2]

with open(script_path) as f:
    lines = f.readlines()

# Find and remove the existing process.source = cms.Source(...)) block
start = None
end = None
for i, line in enumerate(lines):
    if re.match(r'^process\.source\s*=\s*cms\.Source', line):
        start = i
    elif start is not None and re.match(r'^\s*\)\)', line):
        end = i
        break

if start is not None and end is not None:
    del lines[start:end + 1]

lines.append(
    '\nprocess.source = cms.Source("PoolSource",\n'
    '    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),\n'
    '    fileNames = cms.untracked.vstring("' + input_file + '")\n'
    ')\n'
)

with open(script_path, 'w') as f:
    f.writelines(lines)
