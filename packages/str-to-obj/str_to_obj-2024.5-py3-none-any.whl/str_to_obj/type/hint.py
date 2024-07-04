# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2023)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import types as t
import typing as h

# --- Unannotated hints
# Atoms
generic_hint_h = h.Any
simple_hint_h = type[h.Any]
complex_hint_h = t.GenericAlias | t.UnionType

# Grouping
non_complex_hint_h = generic_hint_h | simple_hint_h
raw_hint_h = non_complex_hint_h | complex_hint_h


# --- Annotated hints
annotated_hint_t = type(h.Annotated[object, None])


# --- [Un]Annotated hints
any_hint_h = raw_hint_h | annotated_hint_t


# --- Complex hints additional components:
#     - EllipsisType for GenericAlias, as in: tuple[int, ...]
#     - None for UnionType, as in: int | None
complex_hint_additions_h = t.EllipsisType | None
