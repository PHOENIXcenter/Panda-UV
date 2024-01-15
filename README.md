![Icon](https://github.com/PHOENIXcenter/Panda-UV/assets/55739492/4cf58a21-0bc8-46d4-81fa-eeb18367939c)

Panda-UV is an efficient tool for highly confident fragment assignment in UVPD (Ultraviolet Photodissociation) data. Panda-UV is also compatible with common dissociation methods. Compared to traditional software, Panda-UV implements two strategies as auxiliary quality control for matched fragments: spectral calibration and Pearson correlation scoring. With its high accuracy and confidence, Panda-UV brings the internal fragments that are prevalent in UVPD data into real-world applications, removing the hurdle of random matching of internal fragments caused by the larger search space compared to terminal fragments.

Panda-UV only requires a parameter file (.yaml) as input. With both a GUI (Graphical User Interface) and a CLI (Command Line Interface), Panda-UV is easy to use for a variety of users. The GUI are constructed by PyQt5 v5.15.9 and all the dependencies are packaged in an executable file. GUI can be obtained by clicking the “releases” on the right side of your window. 

The required python libraries:
python 3.7.3+
pandas > 1.3.5
numpy > 1.2.16
argparse > 1.2.1
pyteomics > 4.5.6
PyQt5 > 5.15.9
plotly > 5.14.1

A template parameter file is provided in the source code list above, and users can generate a template by clicking “save param” button in the GUI. The parameter file contains the following parameters:
1.	Sequence: The protein sequence corresponding to the mass spectrua (MS).
2.	Deconv mass: The file directory of the deconvoluted masses, which includes four columns: monoisotopic mass, intensity, m/z, and charge. Both masses and charges are required for fragment matching and theoretical envelope calculation. If intensity and m/z are unknown, they must be set to zero.
3.	Fixed mod: The file directory of the fixed modifications of the analyzed protein, which includes three columns: name, formula, and loc. If the fixed modifications are added to the location of the protein sequence, the theoretical fragments containing the modification will be generated with the mass shift of the modifications. The formulas of the theoretical fragments are also updated by the formulas of the added modifications for the calculation of theoretical envelopes. For example, in the analysis of holo carbonic anhydrase II with an acetylated modification at the N-terminal, a fixed mod file (.csv) containing name, formula, and loc as columns, and acetylation, H2C2O, and 1 as values, is required for correct fragment matching. All fragments containing the first amino acid are generated with the addition of the mass and formula of the acetylation.
4.	Unlocalized mod: The file directory of the unlocalized modifications of the analyzed protein, which includes five columns: name, formula, start_loc, end_loc, and ion_type. Unlocalized modifications are used to match ligands whose binding sites are unknown in the protein sequence. For example, Zn2+ binds to holo carbonic anhydrase II as a non-covalent ligand, but the binding is fragile and can easily be lost from the protein. Theoretical fragments containing the amino acid between start_loc and end_loc should be generated with or without unlocalized modifications to match these modifications.
5.	R env dir: The user should specify the directory of the R environment that has the enviPat package installed for Panda-UV to calculate the theoretical envelopes according to the formulas and charges of the matched fragments. 
6.	mzML dir: The file directory of the centralized raw spectra of the analyzed protein. This is essential for the extraction of the experimental envelopes to calculate the PCC scores of the matched fragments.
7.	Workplace dir: All result files are saved in this directory.
8.	Mass Calibration: The deconvoluted masses can be calibrated if this box is checked for accurate fragment matching.
9.	MS Calibration: The mass spectra can be calibrated if this box is checked for accurate extraction of the experimental envelopes.
10.	Mass Mode: This refers to the mode of deconvoluted masses. If MH+ is selected, the deconvoluted masses, minus the mass of a hydrogen atom, are matched with theoretical fragments.
11.	Terminal mass error (ppm): Allowed mass error tolerance of terminal fragments during fragment matching.
12.	Internal mass error (ppm): Allowed mass error tolerance of internal fragments during fragment matching.
13.	Scan id: This refers to the index of centralized spectra used for extracting the experimental envelope.
14.	Peak match error (ppm): This is the error tolerance allowed during the extraction of the experimental envelopes.
15.	Frag Type: This refers to the possible types of fragments based on the dissociation method used.

Once all parameters are correctly entered into the parameter file, the user can start Panda-UV using either the Command Line Interface (CLI) or the Graphical User Interface (GUI). The Panda-UV GUI allows for the uploading and editing of existing parameters. After all modifications are added to the protein sequence at the user-defined location, all possible theoretical fragments are generated. These fragments are then matched with deconvoluted masses within the specified mass error tolerance. calculated to measure the confidence level between the theoretical envelopes of matched fragments and the experimental envelopes extracted from the analyzed spectrum. Duplicate matches are eliminated by considering both the error and the PCC score. Initially, Panda-UV retains the terminal fragments that have a lower error and a higher PCC score. The workspace directory stores the fragment matching file, fragment cleavage maps, and bar plots of the residual fragment yield of matched fragments for manual review.
