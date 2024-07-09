"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import secrets as scrt
from pathlib import Path as path_t
import typing as h

import flask as flsk

from si_fi_o.html.home_page import HomePage
from si_fi_o.path.server import (
    NAME_FIELD_SEPARATOR,
    TIME_STAMP_SEPARATOR,
)
from si_fi_o.session.form import InputFileContents
from si_fi_o.session.session import session_t, file_output_t


@d.dataclass(repr=False, eq=False)
class routes_t:

    home_page_details: dict[str, h.Any]
    form_type: type
    session_type: type
    ProcessSession: h.Callable[
        [session_t],
        tuple[
            tuple[h.Any, ...], tuple[file_output_t, ...] | None, str | tuple[str] | None
        ],
    ]
    ini_section: str
    runtime_folder: path_t = d.field(init=False, default=None)

    def Configure(self, app: flsk.app, /) -> path_t:
        """"""
        _ = app.route("/")(self.LaunchNewSession)
        _ = app.route("/<session_id>", methods=("GET", "POST"))(self.UpdateHomePage)
        _ = app.route("/load/<session_id>", methods=("POST",))(LoadSession)
        _ = app.route("/save/<session_id>")(SaveSession)
        _ = app.route("/delete/<session_id>")(DeleteSession)

        # app.static_folder is an absolute path
        relative_static_folder = path_t(path_t(app.static_folder).name)
        self.runtime_folder = relative_static_folder / "runtime"

        flask_session_folder = self.runtime_folder / "session"
        flask_session_folder.mkdir(parents=True, exist_ok=True)

        return flask_session_folder

    def LaunchNewSession(self) -> flsk.Response:
        """"""
        session_id = scrt.token_urlsafe().replace(
            NAME_FIELD_SEPARATOR, TIME_STAMP_SEPARATOR
        )
        flsk.session[session_id] = self.session_type(
            self.runtime_folder, session_id, self.ini_section
        )

        return flsk.redirect(f"/{session_id}")

    def UpdateHomePage(self, *, session_id: str = None) -> str:
        """"""
        session = flsk.session[session_id]
        form = self.form_type()  # Do not pass flask.request.form

        session.DeleteObsoleteFiles()

        if flsk.request.method == "GET":
            form.Update(session.AsDictionary())
        elif form.validate_on_submit():
            form_data = form.Data()
            session.UpdateInputs(form_data, form.file_fields)

            if session.IsComplete(form=form):
                outputs = self.ProcessSession(session)
                session.UpdateOutputs(*outputs)

        return HomePage(
            session_id, session=session, form=form, **self.home_page_details
        )


def LoadSession(*, session_id: str = None) -> flsk.Response:
    """"""
    session = flsk.session[session_id]

    contents = InputFileContents().decode("ascii")
    session.UpdateFromINIContents(contents)

    return flsk.redirect(f"/{session_id}")


def SaveSession(*, session_id: str = None) -> flsk.Response:
    """"""
    session = flsk.session[session_id]

    name, path = session.SaveForDownload()

    return flsk.send_file(
        path,
        mimetype="text/plain",
        as_attachment=True,
        download_name=name,
    )


def DeleteSession(*, session_id: str = None) -> flsk.Response:
    """"""
    session = flsk.session[session_id]

    session.DeleteInputFiles()
    session.DeleteOutputFiles()
    session.DeleteFileForDownload()

    flsk.session.pop(session_id, None)

    return flsk.redirect("/")

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
