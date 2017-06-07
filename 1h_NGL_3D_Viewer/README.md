##NGL Examples
NGL 3D Viewer is used for interactive visualization of molecular structures (Peptide/DNA/RNA). It is based on WebGL technology and offers cross-browser compatibility. If your browser does not support WebGL, it might be a good time to upgrade your browser! NGL repo can be found [here](https://github.com/arose/ngl).

This repo is designed to provide detailed examples and documentation on the use of NGL's APIs.

---

#### 3D Structure to Sequence Mapping Utility
**pdbmapper** - extracts PDB sequence, separates into chains, aligns with a given sequences, and provides positional mapping between the PDB sequence numbering (Chain + Amino Acid) and any other sequence.

Usage:

```bash
python mapper.py -s 'AMINOACIDSTRING' -pdb 4hj0.pdb
```
