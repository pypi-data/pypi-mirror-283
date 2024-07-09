"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import datetime as dttm
import re as regx
from pathlib import Path as path_t
import typing as h

from werkzeug.utils import secure_filename as SecureFilenameVersion

from si_fi_o.session.constants import SESSION_DURATION as MAXIMUM_SERVER_FILE_AGE


NAME_FIELD_SEPARATOR = "-"
TIME_STAMP_SEPARATOR = "_"

_SERVER_FILENAME_FORMAT = (
    "{session_id}"
    + NAME_FIELD_SEPARATOR
    + "{time_stamp}"
    + NAME_FIELD_SEPARATOR
    + "{name}"
)
_NOT_FIELD_SEPARATOR = f"[^{NAME_FIELD_SEPARATOR}]+"
_SERVER_FILENAME_PATTERN = _SERVER_FILENAME_FORMAT.format(
    session_id=_NOT_FIELD_SEPARATOR, time_stamp=f"({_NOT_FIELD_SEPARATOR})", name=".+"
)
_SERVER_FILENAME_PATTERN = regx.compile(_SERVER_FILENAME_PATTERN)

_MAXIMUM_SERVER_FILE_AGE = dttm.timedelta(seconds=MAXIMUM_SERVER_FILE_AGE)
_DATE_TIME_REPLACEMENTS = str.maketrans(
    f"{NAME_FIELD_SEPARATOR}:.", 3 * TIME_STAMP_SEPARATOR
)
# See: https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
#     YYYY-MM-DDTHH:MM:SS.ffffff
_DATE_TIME_ISO_FORMAT = "{}-{}-{}T{}:{}:{}.{}"
_DATE_TIME_PATTERN = regx.compile(
    "([0-9]{4})_([0-9]{2})_([0-9]{2})T([0-9]{2})_([0-9]{2})_([0-9]{2})_([0-9]{6})"
)


class file_t(h.NamedTuple):
    client_name: str
    server_path: path_t


def ServerVersionOfFilename(name: str, session_id: str, /) -> str:
    """"""
    time_stamp = (
        dttm.datetime.now()
        .isoformat(timespec="microseconds")
        .translate(_DATE_TIME_REPLACEMENTS)
    )

    return _TimeStampedFilename(name, session_id, time_stamp)


def ServerFilesIterator(
    folder: path_t, session_id: str, /, *, name: str | None = None
) -> h.Iterator[path_t]:
    """
    The default value of "name" could be "*". However, to "simplify" the test in "_TimeStampedFilename", None is used
    instead.
    """
    return folder.glob(_TimeStampedFilename(name, session_id, "*"))


def OutdatedServerFilesIterator(folder: path_t, /) -> h.Iterator[path_t]:
    """"""
    now = dttm.datetime.now()

    for name in folder.glob("*"):
        # Does voluntarily not test matching success since not matching must raise an error
        match = _SERVER_FILENAME_PATTERN.fullmatch(str(name))
        time_stamp = match.group(1)

        # Does voluntarily not test matching success since not matching must raise an error
        match = _DATE_TIME_PATTERN.fullmatch(time_stamp)
        as_tuple = tuple(match.group(_idx) for _idx in range(1, 8))
        iso_date_time = _DATE_TIME_ISO_FORMAT.format(*as_tuple)
        date_time = dttm.datetime.fromisoformat(iso_date_time)

        if date_time + _MAXIMUM_SERVER_FILE_AGE < now:
            yield folder / name


def _TimeStampedFilename(name: str | None, session_id: str, time_stamp: str, /) -> str:
    """"""
    if name is None:
        name = "*"
    else:
        name = SecureFilenameVersion(name)

    return _SERVER_FILENAME_FORMAT.format(
        session_id=session_id, time_stamp=time_stamp, name=name
    )


if TIME_STAMP_SEPARATOR == NAME_FIELD_SEPARATOR:
    raise ValueError("This error should not have happened; Please, contact developer")

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
