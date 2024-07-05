"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2024
SEE COPYRIGHT NOTICE BELOW
"""

import collections.abc as i
import dataclasses as d
import typing as h
from enum import Enum as enum_t

from sio_messenger.exception import (
    ActionNotFoundError,
    CanalNotFoundError,
    ExistingActionError,
    ExistingCanalError,
    MissingSourceError,
)

canal_name_h = str | enum_t
source_h = h.Any
educated_source_h = i.Hashable  # May be an str built from a non-hashable source.
receiver_action_h = h.Callable[[...], None] | h.Callable[[source_h, ...], None]


class canal_t(h.NamedTuple):
    name: canal_name_h
    source: educated_source_h | None = None

    @classmethod
    def UIDfor(cls, name: canal_name_h, /, *, source: source_h | None = None) -> h.Self:
        """"""
        if source is None:
            return cls(name=name)

        if not isinstance(source, i.Hashable):
            # This should serve as a unique id (actually, id(source) alone should work).
            source = f"{type(source).__name__}.{id(source)}"

        return cls(name=name, source=source)

    def __str__(self) -> str:
        """"""
        if (self.source is None) or isinstance(self.source, str):
            source = self.source
        else:
            source = self.source.__name__

        return f"=[{self.name}+{source}]=>"


@d.dataclass(slots=True, repr=False, eq=False)
class messenger_t(dict[canal_t, list[receiver_action_h]]):
    """
    Canal: From (known or unknown) source, and specialized by a message type (its name),
    to message acknowledgement function.
    Limitation: the name "source" cannot be a kwarg of receiver actions.
    """

    _actions_needing_source: set[receiver_action_h] = d.field(
        init=False, default_factory=set
    )

    @property
    def all_actions(self) -> set[receiver_action_h]:
        """"""
        output = set()

        for actions in self.values():
            output.update(actions)

        return output

    def NewCanal(
        self,
        name: canal_name_h,
        /,
        *,
        source: source_h | None = None,
        should_allow_existing_canal: bool = False,
    ) -> canal_t:
        """"""
        output = canal_t.UIDfor(name, source=source)

        if output in self:
            if not should_allow_existing_canal:
                raise ExistingCanalError(f"Canal {output} already exists.")
        else:
            self[output] = []

        return output

    def RemoveCanal(
        self, canal: canal_name_h | canal_t, /, *, source: source_h | None = None
    ) -> None:
        """"""
        if isinstance(canal, canal_name_h):
            canal = canal_t.UIDfor(canal, source=source)
        if canal in self:
            actions_w_src = self._actions_needing_source.intersection(self[canal])

            del self[canal]

            all_actions = self.all_actions
            for action in actions_w_src:
                if action not in all_actions:
                    self._actions_needing_source.discard(action)
        else:
            raise CanalNotFoundError(f"Canal {canal} not found.")

    def AddAction(
        self,
        MessageReceiverAction: receiver_action_h,
        canal: canal_t | canal_name_h,
        /,
        *,
        source: source_h | None = None,
        action_needs_source: bool = False,
    ) -> None:
        """"""
        if action_needs_source and (source is None):
            raise MissingSourceError(
                f"No source passed for canal {canal} and "
                f"receiver action {MessageReceiverAction.__name__}."
            )

        if isinstance(canal, canal_name_h):
            canal = canal_t.UIDfor(canal, source=source)
        if MessageReceiverAction in self[canal]:
            raise ExistingActionError(
                f"Message receiver action {MessageReceiverAction.__name__} "
                f"already exists for canal {canal}."
            )

        self[canal].append(MessageReceiverAction)
        if action_needs_source:
            self._actions_needing_source.add(MessageReceiverAction)

    def RemoveAction(
        self,
        MessageReceiverAction: receiver_action_h,
        /,
        *,
        canal: canal_t | canal_name_h | None = None,
        source: source_h | None = None,
    ) -> None:
        """"""
        if canal is None:
            for actions in self.values():
                if MessageReceiverAction in actions:
                    actions.remove(MessageReceiverAction)

            if MessageReceiverAction in self._actions_needing_source:
                self._actions_needing_source.remove(MessageReceiverAction)
            return

        if isinstance(canal, canal_name_h):
            canal = canal_t.UIDfor(canal, source=source)

        if (canal in self) and (MessageReceiverAction in self[canal]):
            self[canal].remove(MessageReceiverAction)
            if self[canal].__len__() == 0:
                del self[canal]

            if MessageReceiverAction in self._actions_needing_source:
                self._actions_needing_source.remove(MessageReceiverAction)
        elif canal not in self:
            raise CanalNotFoundError(f"Canal {canal} not found.")
        else:
            raise ActionNotFoundError(
                f"Message receiver action {MessageReceiverAction.__name__} "
                f"not found in canal {canal}."
            )

    def AddCanalWithAction(
        self,
        name: canal_name_h,
        MessageReceiverAction: receiver_action_h,
        /,
        *,
        source: source_h | None = None,
        action_needs_source: bool = False,
        should_allow_existing_canal: bool = True,
        should_return_canal: bool = False,
    ) -> canal_t | None:
        """"""
        canal = self.NewCanal(
            name, source=source, should_allow_existing_canal=should_allow_existing_canal
        )
        self.AddAction(
            MessageReceiverAction,
            canal,
            source=source,
            action_needs_source=action_needs_source,
        )

        if should_return_canal:
            return canal

    def Transmit(
        self,
        canal: canal_t | canal_name_h,
        /,
        *args,
        source: source_h | None = None,
        **kwargs,
    ) -> None:
        """"""
        if isinstance(canal, canal_name_h):
            canal = canal_t.UIDfor(canal, source=source)

        if canal in self:
            for MessageReceiverAction in self[canal]:
                if MessageReceiverAction in self._actions_needing_source:
                    MessageReceiverAction(source, *args, **kwargs)
                else:
                    MessageReceiverAction(*args, **kwargs)
        else:
            raise CanalNotFoundError(f"Canal {canal} not found.")

    def __str__(self) -> str:
        """"""
        output = []

        for canal, actions in self.items():
            output.append(f"Canal {canal}")
            for action in actions:
                if action in self._actions_needing_source:
                    with_source = " (w/ source)"
                else:
                    with_source = ""
                owner = getattr(action, "__self__", None)
                if owner is None:
                    owner = ""
                else:
                    owner = f" (owned by {id(owner)})"
                output.append(
                    f"    {action.__module__}.{action.__name__}{with_source}{owner}"
                )

        return "\n".join(output)


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
