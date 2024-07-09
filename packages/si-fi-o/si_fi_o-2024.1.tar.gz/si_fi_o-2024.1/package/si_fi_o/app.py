"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import datetime as dttm
import secrets as scrt
import typing as h

from flask import Flask as flask_app_t
from flask_bootstrap import Bootstrap as BootstrapFlask
from flask_session import Session as flask_session_t

from si_fi_o.routes import routes_t
from si_fi_o.session.constants import SESSION_DURATION
from si_fi_o.session.session import file_output_t, session_t


# def FlaskApp(html_folder: str, /) -> flask_app_t:
#     """
#     Just for reference. The app must be created within the specific project in order
#     to set the template folder.
#     """
#     return flask_app_t(__name__, template_folder=html_folder)


def ConfigureApp(
    app: flask_app_t,
    home_page_details: dict[str, h.Any],
    form_type: type,
    session_type: type,
    max_upload_size: int,
    ProcessSession: h.Callable[
        [session_t],
        tuple[
            tuple[h.Any, ...], tuple[file_output_t, ...] | None, str | tuple[str] | None
        ],
    ],
    ini_section: str,
    /,
) -> None:
    """
    max_upload_size: in megabytes
    """
    routes = routes_t(
        home_page_details=home_page_details,
        form_type=form_type,
        session_type=session_type,
        ProcessSession=ProcessSession,
        ini_section=ini_section,
    )
    flask_session_folder = routes.Configure(app)

    app.config.from_mapping(
        PREFERRED_URL_SCHEME="https",
        SESSION_TYPE="filesystem",
        PERMANENT_SESSION_LIFETIME=dttm.timedelta(seconds=SESSION_DURATION),
        SESSION_FILE_DIR=flask_session_folder,
        SECRET_KEY=scrt.token_bytes(),
        MAX_CONTENT_LENGTH=max_upload_size * 1024 * 1024,
    )
    flask_session_t(app)
    BootstrapFlask(app)

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
