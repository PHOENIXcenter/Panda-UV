import sys
sys.path.insert(0, r'.')
import averagine
from pyteomics import mass

result1 = averagine.formula_to_iso('H749C470O136N131S1', 5)
print(result1)
result2 = averagine.mass_to_iso(mass.calculate_mass('H749C470O136N131S1'), 5)
print(result2)
# 返回 shape=(N, 2) 的 numpy array
# 每行 [mass, relative_abundance]