# Panda-UV Update Log

## v2.0 Update (2026-04-16)

### Requirements

Panda-UV runs on **Python 3.7+** with the following dependencies:

| Package | Version | Description |
|--------|---------|-------------|
| pyteomics | ≥4.5.6 | Mass spectrometry data processing |
| pandas | ≥1.3.5 | Data manipulation |
| numpy | ≥1.21.0 | Numerical computing |
| plotly | ≥5.14.1 | Visualization |
| PyQt5 | ≥5.15.9 | GUI framework |
| tqdm | ≥4.60.0 | Progress bar (for prsm_parser.py) |
| rpy2 | ≥3.5.0 | R integration (for enviPat calculations) |

**R Environment:**
- R with enviPat package is required for theoretical isotope envelope calculations

**Installation:**
```bash
# Using conda environment file
conda env create -f requirements.yml
conda activate main

# Or using pip
pip install pyteomics pandas numpy plotly PyQt5 tqdm rpy2
```

**Note:** R and the enviPat package must be installed separately for isotope peak calculations.

---

### 1. Parameter Structure Refactoring

#### 1.1 Unified Parameter File Format

| Item | v1.0 (Old) | v2.0 (New) |
|------|------------|------------|
| File Format | YAML | JSON |
| Modification Config | Separate file paths | Embedded data structure |
| Scan Processing | Single scan_id | Multiple scans list |
| PRSM Mapping | None | prsm_id dictionary |

#### 1.2 Parameter Changes

**New Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| scans | list | [] | List of scan IDs to process |
| prsm_id | dict | {} | Mapping from scan to prsm_id |
| thread | int | 1 | Number of threads for parallel processing |
| msalign_file_dir | str | "" | Path to msalign file (replaces deconv_mass_file_dir) |

**Renamed/Modified Parameters:**

| Old Name | New Name | Change |
|----------|----------|--------|
| deconv_mass_file_dir | msalign_file_dir | Renamed |
| fixed_mod_file_dir | fixed_mod | File path → Embedded data structure |
| unlocalized_mod_file_dir | unloc_mod | File path → Embedded data structure |
| scan_id | scans | Single value → List |
| None | sequence | New, dict type |

**Deprecated Parameters:**
- `fixed_mod_file_dir`
- `unlocalized_mod_file_dir`
- `deconv_mass_file_dir`

#### 1.3 Modification Data Structure Changes

**Old v1.0 fixed_mod (file path):**
```
fixed_mod_file_dir: "path/to/fixed_mod.csv"
# CSV format: name, formula, loc
```

**New v2.0 fixed_mod (embedded data):**
```json
"fixed_mod": {
  "header": ["name", "formula", "loc"],
  "1920": [["Acetyl", "C2H2O", 1]],
  "4139": [["Acetyl", "C2H2O", 1], ["Carbamidomethyl", "C2H3NO", 2]]
}
```

**New v2.0 unloc_mod:**
```json
"unloc_mod": {
  "header": ["name", "formula", "start_loc", "end_loc", "ion type"],
  "3876": [["heme", "C34H31O4Fe", "any", "any", "any"]]
}
```

**New v2.0 prsm_id:**
```json
"prsm_id": {
  "1563": 0,
  "1570": 1,
  "1920": 100
}
```

---

### 2. GUI Interface Refactoring

#### 2.1 Layout System Upgrade

| Issue | Solution |
|-------|----------|
| Components crowded/overlapping | Qt Layout Manager (QGridLayout, QVBoxLayout, QHBoxLayout) |
| Layout broken on window resize | Set minimum window size (1300x950) |
| Fixed coordinate positioning | Responsive layout |

#### 2.2 New Table Components

| Table | Columns | Function |
|-------|---------|----------|
| Scan-Sequence | Scan, Sequence | Configure protein sequence for each scan |
| Fixed mod | Scan, name, formula, loc | Configure fixed modifications per scan |
| Unlocalized mod | Scan, name, formula, start_loc, end_loc, ion type | Configure variable modifications |
| PRSM ID | Scan, prsm_id | Configure scan to prsm_id mapping |

#### 2.3 Input Validation System

**Validation Rules:**

| Field | Validation | Error Message |
|-------|------------|---------------|
| Scan | Non-empty, integer | "Scan must be an integer, got 'xxx'" |
| Sequence | Non-empty | "Sequence cannot be empty" |
| loc | Integer | "'loc' must be an integer, got 'xxx'" |
| start_loc/end_loc | Integer or "any" | "'start_loc' must be an integer or 'any', got 'xxx'" |
| PRSM ID | Integer | "PRSM ID must be an integer, got 'xxx'" |

**Error Display Features:**
- Error cells highlighted (light red background #FFC8C8)
- Summary error message dialog
- Pre-save completeness check

---

### 3. Core Functionality Enhancements

#### 3.1 Multi-threaded Parallel Processing

**Parameter:** `thread` - Number of threads

**Behavior:**
- `thread = 1`: Single-threaded sequential processing
- `thread > 1`: Parallel processing using ThreadPoolExecutor

**GUI Location:** Right settings panel → "Thread count" control

#### 3.2 Batch Scan Processing

**Old version:** Can only process one scan at a time (scan_id parameter)

**New version:** Can configure multiple scans simultaneously, each with its own:
- Protein sequence
- Fixed modifications
- Variable modifications
- PRSM ID

---

### 4. Code Architecture Optimization

#### 4.1 Module Integration

| Old Version | New Version |
|-------------|-------------|
| PandaUV_main.py | PandaUV_core.py (PandaUV class) |
| Standalone functions | Class methods |
| Scattered param classes | Unified Param class |

#### 4.2 Main Classes and Methods

```python
# Param class
class Param:
    def get_param_template()  # Get default parameter template
    def save_param()         # Save parameters to JSON
    def read_param()         # Load parameters from JSON

# PandaUV class
class PandaUV:
    def run()                 # Single-threaded run
    def run_parallel()        # Multi-threaded run
    def initialize()          # Initialize environment
    def match()               # Single scan matching
```

---

### 5. Usage Method Changes

#### 5.1 Parameter File Creation Workflow

**Old version:**
1. Prepare fixed_mod.csv file
2. Prepare unlocalized_mod.csv file
3. Enter file paths in GUI
4. Save parameters

**New version:**
1. Add scan and sequence in Scan-Sequence table in GUI
2. Add modifications in Fixed mod table (directly embedded)
3. Add variable modifications in Unlocalized mod table
4. Configure mapping in PRSM ID table
5. Save parameters (automatically generates JSON)

#### 5.2 Parameter File Examples

**v1.0 (YAML):**
```yaml
sequence: 'MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG'
deconv_mass_file_dir: 'path/to/deconv_mass.csv'
fixed_mod_file_dir: 'path/to/fixed_mod.csv'
unlocalized_mod_file_dir: 'path/to/unloc_mod.csv'
scan_id: 3871
mass_calibration: true
ms_calibration: true
mass_mode: 'M'
terminal_mass_error: 10
```

**v2.0 (JSON):**
```json
{
  "sequence": {
    "1563": "MQIFVKTLTGKTITLEVEPSDTIENV...",
    "1570": "SGRGKGGLETKGPSSSEL..."
  },
  "scans": [1563, 1570, 1612],
  "msalign_file_dir": "path/to/msalign.msalign",
  "fixed_mod": {
    "header": ["name", "formula", "loc"],
    "1563": [["Acetyl", "C2H2O", 1]],
    "1570": [["Carbamidomethyl", "C2H3NO", 2]]
  },
  "unloc_mod": {
    "header": ["name", "formula", "start_loc", "end_loc", "ion type"],
    "1563": [["heme", "C34H31O4Fe", "any", "any", "any"]]
  },
  "prsm_id": {
    "1563": 0,
    "1570": 1,
    "1612": 10
  },
  "thread": 4,
  "mass_calibration": false,
  "ms_calibration": false,
  "mass_mode": "M",
  "terminal_mass_error": 10
}
```

### 6.3 Example Datasets

#### example_param_Ub_monomer.json
- **Dataset Location**: examples/20200110_ubiquitin_193nm_1_2mj_monomer_Z6_1428_1
- **Description**: Single protein (Ubiquitin) example demonstrating basic Panda-UV usage
- **Data Source**: UVPD mass spectrometry data of Ubiquitin monomer
- **Use Case**: Demonstrates single protein analysis with fixed and variable modifications

#### example_param_OT_rep1_toppic1.5.4.json
- **Dataset Location**: examples/CPTAC_Intact_rep1_15Jan15_Bane_C2-14-08-02RZ
- **Description**: Complex dataset from CPTAC intact proteomics study
- **Data Source**: Park, J., et al. "Informed-Proteomics: open-source software package for top-down proteomics." Nat. Methods 14.9 (2017): 909-914.
- **Search Method**: TopPIC v1.5.4 (Top-down proteomics identification and characterization)
- **Parameter Generation**: Generated using prsm_parse.py based on TopPIC search results
- **Reference**: Basharat, A.R., Ning, X., & Liu, X. "EnvCNN: a convolutional neural network model for evaluating isotopic envelopes in top-down mass-spectral deconvolution." Anal. Chem. 92.11 (2020): 7778-7785.

**Related References**:
- Park, J., et al. "Informed-Proteomics: open-source software package for top-down proteomics." Nat. Methods 14.9 (2017): 909-914.
- Basharat, A.R., Ning, X., & Liu, X. "EnvCNN: a convolutional neural network model for evaluating isotopic envelopes in top-down mass-spectral deconvolution." Anal. Chem. 92.11 (2020): 7778-7785.

---

### 7. Citation

If you use Panda-UV in your research, please cite:

**Panda-UV**: Zhu, Y., et al. "Panda-UV Unlocks Deeper Protein Characterization with Internal Fragments in Ultraviolet Photodissociation Mass Spectrometry." Anal. Chem. 96.21 (2024): 8474-8483.

---

## Original Version (v1.0 - 2023-08-18)

- Basic GUI and CLI implementation
- Single scan processing mode
- Separate file storage for modification data
- Core fragment matching algorithm
- PCC scoring system
- Mass calibration functionality
