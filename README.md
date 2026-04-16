# Panda-UV Update Log

## v2.0 Update (2026-04-16)

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

---

### 6. Migration Guide

#### 6.1 From v1.0 to v2.0

1. **Parameter File Conversion**
   - Old version uses separate CSV files for modifications
   - New version requires embedding modification data into JSON structure

2. **scan_id to scans**
   - Old: `scan_id: 3871`
   - New: `scans: [3871]`, add corresponding sequence in `sequence`

3. **File Path Updates**
   - `deconv_mass_file_dir` → `msalign_file_dir`
   - Format changed from CSV to msalign

#### 6.2 Compatibility Notes

- v2.0 uses JSON format, v1.0 uses YAML format
- The two versions have completely different parameter structures and require manual conversion

---

## Original Version (v1.0 - 2023-08-18)

- Basic GUI and CLI implementation
- Single scan processing mode
- Separate file storage for modification data
- Core fragment matching algorithm
- PCC scoring system
- Mass calibration functionality
