<div align=center>
<img src=https://github.com/PHOENIXcenter/Panda-UV/assets/55739492/42bc2fc6-1e61-4df7-b84d-b32d1dafabeb>
</div>

Panda-UV is an efficient tool for highly confident fragment assignment in UVPD (Ultraviolet Photodissociation) data. Panda-UV is also compatible with common dissociation methods. Compared to traditional software, Panda-UV implements two strategies as quality control for matched fragments: spectral calibration and Pearson correlation scoring. With its high accuracy and confidence, Panda-UV brings the internal fragments that are prevalent in UVPD data into real-world applications, removing the hurdle of random matching of internal fragments caused by the larger search space compared to terminal fragments.

Panda-UV only requires a parameter file (.yaml) as input. With both a GUI (Graphical User Interface) and a CLI (Command Line Interface), Panda-UV is easy to use for a variety of users. The GUI is built using PyQt5 v5.15.9, and all dependencies are packaged into an executable file Panda-UV_GUI.exe. It can be downloaded by clicking the “releases” on the right side of your window. The program can be run by double-clicking on it, and it does not require any third-party libraries. 

The required python libraries:
python 3.7.3+
pandas > 1.3.5
numpy > 1.2.16
argparse > 1.2.1
pyteomics > 4.5.6
PyQt5 > 5.15.9
plotly > 5.14.1

A template parameter file is provided in the source code list above, and users can generate a template by clicking “save param” button in the GUI. The parameter file contains the following parameters:
①	Sequence: The protein sequence corresponding to the mass spectra.
②	Deconv mass: The file directory of the deconvoluted masses, which includes four columns: monoisotopic mass, intensity, m/z, and charge. Both masses and charges are required for fragment matching and theoretical envelope calculation. If intensity and m/z are unknown, they should be set to zero.
③	Fixed mod: The file directory of the fixed modifications of the analyzed protein, which includes three columns: name, formula, and location. If a fixed modification is added to a certain location of the protein sequence, the theoretical fragments containing the modification will be generated with the mass shift of the modification. The formulas of the theoretical fragments are also updated by the formulas of the added modifications to calculate theoretical envelopes. For example, in the analysis of holo carbonic anhydrase II with an acetylated modification at the N-terminal, a fixed mod file (.csv) containing name, formula, and location as columns, and acetylation, H2C2O, and 1 as values, is required for correct fragment matching. All fragments containing the first amino acid are generated with the addition of the mass and formula of the acetylation.
④	Unlocalized mod: The file directory of the unlocalized modifications of the analyzed protein, which includes five columns: name, formula, start_loc, end_loc, and ion_type. Unlocalized modifications are used to match ligands whose binding sites are unknown in the protein sequence. For example, Zn2+ binds to holo carbonic anhydrase II as a non-covalent ligand, but the binding is fragile and can easily be lost from the protein. Theoretical fragments containing the amino acid between start_loc and end_loc should be generated with or without unlocalized modifications to match these modifications.
⑤	R env dir: The user should specify the directory of the R environment where the enviPat package is installed. The enviPat package is used to calculate the theoretical envelopes according to the formulas and charges of the matched fragments.
⑥	mzML dir: The file directory of the centralized raw spectra of the analyzed protein. This is essential for the extraction of the experimental envelopes to calculate the PCC scores of the matched fragments.
⑦	Workplace dir: All result files are saved in this directory.
⑧	Mass calibration: The deconvoluted masses can be calibrated if this box is checked for accurate fragment matching.
⑨	Mass spectrum calibration: The mass spectra can be calibrated if this box is checked for accurate extraction of the experimental envelopes.
⑩	Mass mode: This refers to the mode of deconvoluted masses. If MH+ is selected, the deconvoluted masses, minus the mass of a hydrogen atom, are matched with theoretical fragments.
⑪	Terminal mass error (ppm): Allowed mass error tolerance of terminal fragments during fragment matching.
⑫	Internal mass error (ppm): Allowed mass error tolerance of internal fragments during fragment matching.
⑬	Scan id: This refers to the index of centralized spectra used for extracting the experimental envelope.
⑭	Peak match error (ppm): This is the error tolerance allowed during the extraction of the experimental envelopes.
⑮	Frag Type: This refers to the possible types of fragments based on the dissociation method used.

Once all parameters are correctly entered into the parameter file, the user can start Panda-UV using either the CLI or GUI interfaces. The Panda-UV GUI allows users to upload and edit existing parameter files. After all modifications are added to the protein sequence at the user-defined location, all possible theoretical fragments are generated. These fragments are then matched with deconvoluted masses within the specified mass error tolerance. The Pearson Correlation Coefficient (PCC) scores are calculated to measure the confidence level between the theoretical envelopes of matched fragments and the experimental envelopes extracted from the analyzed spectrum. Duplicate matches are eliminated by considering both the error and the PCC score. Initially, Panda-UV retains the terminal fragments that have a lower mass error and a higher PCC score. The workspace directory stores the fragment matching file, fragment cleavage maps, and bar plots of the residual fragment yield of matched fragments for manual review.
