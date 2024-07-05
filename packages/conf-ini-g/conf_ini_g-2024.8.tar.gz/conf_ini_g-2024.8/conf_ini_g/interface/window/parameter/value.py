# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2021)
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

import dataclasses as d
import typing as h
from abc import ABC as abstract_class_t
from abc import abstractmethod

from babelwidget.main import backend_t
from str_to_obj.api.type import annotation_t, type_t


class _do_not_set_value:
    pass


DO_NOT_SET_VALUE = _do_not_set_value()


@d.dataclass(repr=False, eq=False)
class value_wgt_a(abstract_class_t):
    messenger: d.InitVar[h.Any | None]
    message: d.InitVar[str | h.Sequence[str] | None]
    backend: d.InitVar[backend_t | None]
    _AcknowledgeNewValue: h.Callable[[], None] | None = d.field(
        init=False, default=None
    )

    def __post_init__(
        self,
        messenger: h.Any | None,
        message: str | h.Sequence[str] | None,
        backend: backend_t,
    ) -> None:
        """"""
        if messenger is None:
            return

        if isinstance(messenger, h.Sequence):
            if isinstance(message, str):
                message = messenger.__len__() * (message,)
            for who, what in zip(messenger, message):
                backend.AddMessageCanal(who, what, self.AcknowledgeNewValue)
        else:
            backend.AddMessageCanal(messenger, message, self.AcknowledgeNewValue)

    def SetNewValueAcknowledgementFunction(
        self, Function: h.Callable[[], None], /
    ) -> None:
        """"""
        self._AcknowledgeNewValue = Function

    def AcknowledgeNewValue(self) -> None:
        """"""
        if self._AcknowledgeNewValue is not None:
            self._AcknowledgeNewValue()

    @classmethod
    @abstractmethod
    def NewForSpecification(
        cls, stripe: type_t | annotation_t | None, backend: backend_t
    ) -> h.Self: ...

    @abstractmethod
    def Assign(self, value: h.Any, stripe: type_t | annotation_t | None, /) -> None: ...

    @abstractmethod
    def Text(self) -> str: ...
