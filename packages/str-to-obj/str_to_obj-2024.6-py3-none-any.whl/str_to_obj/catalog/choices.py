"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

from logger_36 import LOGGER
from str_to_obj.type.annotation import annotation_t
from str_to_obj.type.hint import annotated_hint_t


@d.dataclass(slots=True, repr=False, eq=False)
class choices_t(annotation_t):
    ACCEPTED_TYPES: h.ClassVar[tuple[type, ...]] = (str,)

    options: h.Sequence[str]

    def __post_init__(self) -> None:
        """"""
        with LOGGER.AddedContextLevel("Choices Annotation"):
            for option in self.options:
                if not isinstance(option, str):
                    LOGGER.StageIssue(
                        f'Invalid type of option "{option}"',
                        actual=type(option).__name__,
                        expected="str",
                    )

    @classmethod
    def NewAnnotatedType(cls, options: h.Sequence[str], /) -> annotated_hint_t:
        """"""
        return h.Annotated[str, cls(tuple(options))]

    def ValueIssues(self, value: str | h.Any, /) -> list[str]:
        """"""
        issues = annotation_t.ValueIssues(self, value)
        if issues.__len__() > 0:
            return issues

        if (self.options.__len__() == 0) or (value in self.options):
            # Options can be empty for a controlling parameter whose controlled section
            # has not been specified. In a GUI context, such controlled section should
            # have been populated programmatically.
            return []

        options = map(lambda _elm: f'"{_elm}"', self.options)
        options = " or ".join(options)

        return [f"Invalid choice: Actual={value}; Expected={options}."]


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
