#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .surface_tension import surface_tension as surface_tension_cls

class forces(Group):
    """
    Specify interfacial forces.
    """

    fluent_name = "forces"

    child_names = \
        ['surface_tension']

    _child_classes = dict(
        surface_tension=surface_tension_cls,
    )

