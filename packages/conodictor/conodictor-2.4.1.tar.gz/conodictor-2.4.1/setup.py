# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conodictor']

package_data = \
{'': ['*']}

install_requires = \
['bio>=1.3.3,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyfastx>=0.8.4,<0.9.0',
 'pyhmmer>=0.10.13,<0.11.0',
 'xphyle>=4.4.4,<5.0.0']

entry_points = \
{'console_scripts': ['conodictor = conodictor.conodictor:main']}

setup_kwargs = {
    'name': 'conodictor',
    'version': '2.4.1',
    'description': 'Prediction and classification of conopeptides',
    'long_description': '# ConoDictor\n\n*A fast and accurate prediction and classification tool for conopeptides*\n\n[![PyPI](https://img.shields.io/pypi/v/conodictor.svg)](https://pypi.org/project/conodictor)\n[![Wheel](https://img.shields.io/pypi/wheel/conodictor.svg)](https://pypi.org/project/conodictor)\n[![Language](https://img.shields.io/pypi/implementation/conodictor)](https://pypi.org/project/conodictor)\n[![Pyver](https://img.shields.io/pypi/pyversions/conodictor.svg)](https://pypi.org/project/conodictor)\n[![Downloads](https://img.shields.io/pypi/dm/conodictor)](https://pypi.org/project/conodictor)\n[![Docker](https://img.shields.io/docker/pulls/ebedthan/conodictor.svg)]()\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n\n## 🗺️ Overview\n### Unlocking the Potential of Cone Snail Venom\nCone snails are a treasure trove of natural peptides with immense pharmacological and therapeutic potential. The advent of affordable RNA sequencing (RNAseq) has revolutionized the mining of novel bioactive conopeptides from venom gland transcriptomes. However, the complexity of bioinformatic analyses often impedes the discovery process.\n\n### Introducing ConoDictor 2\nConoDictor 2 is a standalone, user-friendly command-line tool designed to streamline the discovery of conopeptides. Building on a decade-old web server, we have significantly upgraded ConoDictor with modern tools and algorithms, and enhanced our classification models using new, high-quality sequences. The result is a program that is more accurate, faster, and compatible across multiple platforms.\n\n### Key Features\n* **Enhanced Accuracy and Speed**: ConoDictor 2 processes entire venom gland transcriptomes, whether from raw reads or assembled contigs, in record time.\n* **Ease of Use**: The program requires only the assembled transcriptome or raw reads file, in either DNA or amino acid format. ConoDictor 2 automatically recognizes the alphabet used.\n* **Advanced Prediction Capabilities**: It runs predictions directly on the submitted or dynamically generated proteins file, aiming to identify the longest conopeptide precursor-like sequences.\n\n### Simplified Bioinformatics for Breakthrough Discoveries\nWith ConoDictor 2, researchers can bypass the intricate bioinformatic challenges and focus on uncovering the next generation of bioactive peptides from cone snail venom. Its robust performance and user-centric design make it an indispensable tool in venom research and drug discovery.\n\n## Installing\n\n### Install from Pip\n\nYou will first have to install ~~[HMMER 3](https://hmmer.org) and~~ [Pftools](https://github.com/sib-swiss/pftools3) to be able to run conodictor (**as of version 2.4, conodictor does not need hmmer anymore as it use the wonderful [pyhmmer](https://github.com/althonos/pyhmmer) library**).\n\n```bash\npip install conodictor\n```\n\n### Using containers\n\n### Docker\n\nAccessible at https://hub.docker.com/u/ebedthan or on [BioContainers](https://github.com/BioContainers/containers/tree/master/conodictor/2.2.2).\n\n\n```bash\ndocker pull ebedthan/conodictor:latest\ndocker run ebedthan/conodictor:latest conodictor -h\n```\n\nExample of a run\n\n```bash\ndocker run --rm=True -v $PWD:/data -u $(id -u):$(id -g) ebedthan/conodictor:latest conodictor --out /data/outdir /data/input.fa.gz\n```\n\nSee https://staph-b.github.io/docker-builds/run_containers/ for more informations on how to properly run a docker container.\n\n\n### Singularity\n\nThe singularity container does not need admin privileges making it\nsuitable for university clusters and HPC.\n\n```bash\nsingularity build conodictor.sif docker://ebedthan/conodictor:latest\nsingularity exec conodictor.sif conodictor -h\n```\n\n\n### Install from source\n\n```bash\n# Download ConoDictor development version\ngit clone https://github.com/koualab/conodictor.git conodictor\n\n# Navigate to directory\ncd conodictor\n\n# Install with poetry: see https://python-poetry.org\npoetry install --no-dev\n\n# Enter the Python virtual environment with\npoetry shell\n\n# Test conodictor is correctly installed\nconodictor -h\n```\n\nIf you do not want to go into the virtual environment just do:\n\n```bash\npoetry run conodictor -h\n```\n\n\n## 💡 Example\n\n```bash\nconodictor file.fa.gz\nconodictor --out outfolder --cpus 4 --mlen 51 file.fa\n```\n\n\n## Output files\n\nThe comma separeted-values file summary.csv can be easily viewed with any office suite,\nor text editor.\n\n```csv\nsequence,hmm_pred,pssm_pred definitive_pred\nSEQ_ID_1,A,A,A\nSEQ_ID_2,B,D,CONFLICT B and D\nSEQ_ID_3,O1,O1,O1\n...\n\n```\n\n## 💭 Feedback\n\n### Issue tracker\n\nFound a bug ? Have an enhancement request ? Head over to the [GitHub issue\ntracker](https://github.com/koualab/conodictor/issues) if you need to report\nor ask something. If you are filing in on a bug, please include as much\ninformation as you can about the issue, and try to recreate the same bug\nin a simple, easily reproducible situation.\n\n## ⚖️ License\n\n[GPL v3](https://github.com/koualab/conodictor/blob/main/LICENSE).\n\nFor commercial uses please contact Dominique Koua at dominique.koua@inphb.ci.\n\n## 🔖 Citation\n\nConoDictor is a scientifc software, with a [published paper](https://doi.org/10.1093/bioadv/vbab011) in the [Bioinformatics Advances](https://academic.oup.com/bioinformaticsadvances) journal. Please cite this article if you are using it in an academic work, for instance as: \nKoua, D., Ebou, A., & Dutertre, S. (2021). Improved prediction of conopeptide superfamilies with ConoDictor 2.0. Bioinformatics Advances, 1(1), vbab011. https://doi.org/10.1093/bioadv/vbab011\n\n\n## Dependencies\n\n* [**Pftools**](https://github.com/sib-swiss/pftools3)  \n  Used for PSSM prediction.    \n  *Schuepbach P et al. pfsearchV3: a code acceleration and heuristic to search PROSITE profiles. Bioinformatics 2013, 10.1093/bioinformatics/btt129*\n\n\n## 📚 References\n\n* [**HMMER 3**](https://hmmer.org)  \n  Used for HMM profile prediction.   \n  *Eddy SR, Accelerated Profile HMM Searches. PLOS Computational Biology 2011, 10.1371/journal.pcbi.1002195*\n\n* [**Pftools**](https://github.com/sib-swiss/pftools3)  \n  Used for PSSM prediction.    \n  *Schuepbach P et al. pfsearchV3: a code acceleration and heuristic to search PROSITE profiles. Bioinformatics 2013, 10.1093/bioinformatics/btt129*\n\n\n## Authors\n\n* [Anicet Ebou](https://orcid.org/0000-0003-4005-177X)\n* [Dominique Koua](https://www.researchgate.net/profile/Dominique_Koua)',
    'author': 'Anicet Ebou',
    'author_email': 'anicet.ebou@gmail.com',
    'maintainer': 'Anicet Ebou',
    'maintainer_email': 'anicet.ebou@gmail.com',
    'url': 'https://github.com/koualab/conodictor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
