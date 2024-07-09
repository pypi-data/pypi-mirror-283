"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d

from logger_36.handler import AddGenericHandler
from logger_36.instance.loggers import LOGGERS
from pyvispr.extension.qt.imports import qtwg
from pyvispr.flow.visual.whiteboard import whiteboard_t


@d.dataclass(slots=True, repr=False, eq=False)
class _text_wgt_t(qtwg.QTextEdit):
    def __post_init__(self) -> None:
        """"""
        qtwg.QTextEdit.__init__(self)
        self.setReadOnly(True)
        self.setLineWrapMode(qtwg.QTextEdit.LineWrapMode.NoWrap)
        AddGenericHandler(self.insertHtml, logger=LOGGERS.active, supports_html=True)

    def insertHtml(self, text: str, /) -> None:
        """
        Overridden to avoid extra vertical space between every message. This is done by
        adding an empty paragraph. Why does this work? ...
        """
        qtwg.QTextEdit.insertHtml(self, text + "<p></p>")


@d.dataclass(slots=True, repr=False, eq=False)
class log_wgt_t(qtwg.QStackedWidget):
    whiteboard: d.InitVar[whiteboard_t]
    text_areas: dict[whiteboard_t, qtwg.QTextEdit] = d.field(
        init=False, default_factory=dict
    )

    def __post_init__(self, whiteboard: whiteboard_t) -> None:
        """"""
        qtwg.QStackedWidget.__init__(self)
        self.AddAreaForWhiteboard(whiteboard)

    def AddAreaForWhiteboard(self, whiteboard: whiteboard_t, /) -> None:
        """"""
        LOGGERS.AddNew(whiteboard)
        text = _text_wgt_t()
        self.addWidget(text)
        self.text_areas[whiteboard] = text

    def RemoveAreaOfWhiteboard(self, whiteboard: whiteboard_t, /) -> None:
        """"""
        text = self.text_areas[whiteboard]
        del self.text_areas[whiteboard]
        self.removeWidget(text)

    def SwitchAreaForWhiteboard(self, whiteboard: whiteboard_t, /) -> None:
        """"""
        if whiteboard not in self.text_areas:
            self.AddAreaForWhiteboard(whiteboard)
        text = self.text_areas[whiteboard]
        self.setCurrentWidget(text)


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
