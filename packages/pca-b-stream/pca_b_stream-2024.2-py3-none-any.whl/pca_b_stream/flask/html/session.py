"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2021
SEE COPYRIGHT NOTICE BELOW
"""

import dominate.tags as html
from pca_b_stream.flask.session.session import session_t
from si_fi_o.path.html import URLOfPath

_LEGEND = {
    "m": "Max. value in array (= number of sub-streams)",
    "c": "Compressed",
    "e": "Endianness (or byte order)",
    "t": "dtype code",
    "T": "dtype name",
    "o": "Enumeration order",
    "v": "First value per sub-stream (0: 0 or False, 1: non-zero or True)",
    "d": "Array dimension",
    "l": "Lengths per dimension",
}


def SessionInputsAsHTML(_: session_t | None, __: str, /) -> html.html_tag:
    """"""
    return html.div(_class="container")


def SessionOutputsAsHTML(session: session_t, /) -> html.html_tag | None:
    """
    Needs to be kept in sync with processing.py since it assigns the outputs
    """
    if (outputs := session.outputs) is None:
        return None

    (
        stream,
        stream_size,
        details,
        high_contrast_name,
    ) = outputs  # This is where syncing matters
    if stream is None:
        stream = session["stream"]
        path = session.outputs_path
        name = "Decoded Stream"
    else:
        path = session["array"].server_path
        name = session["array"].client_name
    if high_contrast_name is None:
        high_contrast_path = path
    else:
        high_contrast_path = session.additional_paths[high_contrast_name]

    if path is None:
        figure = html.p("Decoding Error: Invalid Byte-Stream Representation")
        array_size = ""
    else:
        figure = html.figure(
            html.img(src=URLOfPath(high_contrast_path)),
            html.figcaption(
                html.i(f"{name} (do not download; contrast-enhanced version)")
            ),
        )
        array_size = path.stat().st_size

    output = html.div()
    with output:
        with html.table(style="margin-bottom:1em"):
            with html.tr():
                html.td(
                    html.div(
                        html.pre(stream),
                        style="margin-right:2em; width:50em; height:10em; overflow:auto",
                    )
                )
                html.td(figure)
            with html.tr():
                html.td(f"Stream length: {stream_size}")
                html.td(f"Filesize: {array_size}")
        with html.table(border="1px", style="margin-bottom:1em"):
            with html.tr():
                for key in details.keys():
                    html.th(_LEGEND[key])
            with html.tr():
                for key, value in details.items():
                    if key in ("c", "v"):
                        html.td(html.div(value, style="width:10em; overflow:auto"))
                    elif key == "l":
                        html.td(
                            str(value)[1:-1].replace(",", " x"), _class="align_center"
                        )
                    else:
                        html.td(value, _class="align_center")

    return output


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
