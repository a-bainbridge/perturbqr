# perturbqr

How to use our project:

Install (via pip) the libraries `reedsolo` (to handle the Reed-Solomon codes and GF(256) arithmetic) and `qrcodegen` (used only for writing out the adversarial QR codes). Then follow this process:

- Generate/find the QR code you want to modify, noting the version, mask bits, and data. At this time, only the 'L' level of redundancy is supported.
- Consult ISO/IEC 18004:2015(E), Table 7 for the number of binary and error correction symbols for the given version.
- Come up with a strategy to generate adversarial URLs (random, sequential, etc.)
- Follow the example in `util.py` to rapidly encode, optimize, and compute the Hamming distance between your adversarial QR and the target QR.
- Repeat until satisfied!
