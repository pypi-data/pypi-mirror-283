"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2021
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

import numpy as nmpy
import pca_b_stream.main as pcas
from pca_b_stream.flask.session.form import form_t
from pca_b_stream.flask.session.session import session_t
from si_fi_o.session.session import file_output_t

import imageio as mgio

output_types_h = tuple[
    tuple[h.Any, ...], tuple[file_output_t, ...] | None, str | tuple[str] | None
]


def ProcessSession(session: session_t, /) -> output_types_h:
    """"""
    if form_t.RequestedToByteStream():
        return _ToSTR(session)
    else:
        return _ToARY(session)


def _ToSTR(session: session_t, /) -> output_types_h:
    """"""
    image = mgio.v3.imread(session["array"].server_path)
    issues = pcas.PCArrayIssues(image)
    if issues.__len__() == 0:
        stream = pcas.PCA2BStream(image)
        length = stream.__len__()
        details = pcas.BStreamDetails(stream)
        stream = stream.decode("ascii")
    else:
        issues = "\n    ".join(issues)
        stream = f"Invalid Piecewise-constant Array:\n    {issues}"
        length = -1
        details = None

    high_contrast = nmpy.around(255.0 * (image / nmpy.amax(image))).astype(nmpy.uint8)
    high_contrast_name = "image-high-contrast.png"
    file_output = file_output_t(
        name=high_contrast_name,
        contents=high_contrast,
        Write=mgio.imwrite,
    )

    return (stream, length, details, high_contrast_name), (file_output,), None


def _ToARY(session: session_t, /) -> output_types_h:
    """"""
    stream = bytes(session["stream"], "ascii")
    length = stream.__len__()

    try:
        decoded = pcas.BStream2PCA(stream)
    except:
        decoded = None

    if decoded is None:
        return (None, length, None, None), None, None

    high_contrast = nmpy.around(255.0 * (decoded / nmpy.amax(decoded))).astype(
        nmpy.uint8
    )
    details = pcas.BStreamDetails(stream)

    file_output_1 = file_output_t(
        name="decoded.png", contents=decoded, Write=mgio.imwrite
    )
    high_contrast_name = "decoded-high-contrast.png"
    file_output_2 = file_output_t(
        name=high_contrast_name, contents=high_contrast, Write=mgio.imwrite
    )

    return (
        (None, length, details, high_contrast_name),
        (file_output_1, file_output_2),
        "decoded.png",
    )


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
