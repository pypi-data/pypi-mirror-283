"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2021
SEE COPYRIGHT NOTICE BELOW
"""

"""
Functions for the command line interface of PCA-B-Stream.
Run doctests below with: python cli.py

>>> import pathlib
>>> import sys
>>> from unittest.mock import patch
>>> path = pathlib.Path(".") / "resource" / "pca-0.png"
>>> with patch("sys.argv", new=["fake_cmd_name", path]):
...     PCA2BStream()
FnmHo0tyN+0}BCI
>>> import imageio
>>> import numpy
>>> import pathlib
>>> import sys
>>> import tempfile
>>> from unittest.mock import patch
>>> folder = tempfile.mkdtemp()
>>> path = pathlib.Path(folder) / "a.png"
>>> with patch("sys.argv", new=["fake_cmd_name", "FnmHo0tyN+0}BCI", path]):
...     BStream2PCA()
>>> original_path = pathlib.Path(".") / "resource" / "pca-0.png"
>>> original = imageio.v3.imread(original_path)
>>> image = imageio.v3.imread(path)
>>> print(numpy.array_equal(image, original))
True
"""

import sys as sstm
from pathlib import Path as path_t

import pca_b_stream.main as pcas

import imageio as mgio


def PCA2BStream() -> None:
    """"""
    error_code = -1

    if sstm.argv.__len__() != 2:
        print(
            f"{PCA2BStream.__name__.lower()}: No image specified or too many arguments"
        )
        sstm.exit(error_code)
    error_code -= 1

    path = path_t(sstm.argv[1])
    if not path.is_file():
        print(f"{path}: Specified path is not a(n existing) file")
        sstm.exit(error_code)
    error_code -= 1

    try:
        image = mgio.v3.imread(path)
    except Exception as exception:
        print(exception)
        sstm.exit(error_code)
    error_code -= 1

    issues = pcas.PCArrayIssues(image)
    if issues.__len__() > 0:
        issues = "\n    ".join(issues)
        print(f"{path}: Not a valid Piecewise-Constant Array:\n    {issues}")
        sstm.exit(error_code)
    error_code -= 1

    print(pcas.PCA2BStream(image).decode("ascii"))


def BStream2PCA() -> None:
    """"""
    error_code = -1

    if sstm.argv.__len__() != 3:
        print(
            f"{BStream2PCA.__name__.lower()}: No stream and output file specified, or too many arguments"
        )
        sstm.exit(error_code)
    error_code -= 1

    stream = sstm.argv[1]
    if ("'" in stream) or ('"' in stream):
        print(
            f"{stream}: Stream contains ' or \"; "
            f'Note that the stream must not be passed with the "b" string type prefix'
        )
        sstm.exit(error_code)
    error_code -= 1

    stream = bytes(stream, "ascii")

    path = path_t(sstm.argv[2])
    if path.exists():
        print(
            f"{path}: Specified file already exists; Please delete first, or use another filename"
        )
        sstm.exit(error_code)
    error_code -= 1

    try:
        decoded = pcas.BStream2PCA(stream)
    except Exception as exception:
        print(exception)
        sstm.exit(error_code)
    error_code -= 1

    mgio.imwrite(path, decoded)


if __name__ == "__main__":
    #
    import doctest

    doctest.testmod()

"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
