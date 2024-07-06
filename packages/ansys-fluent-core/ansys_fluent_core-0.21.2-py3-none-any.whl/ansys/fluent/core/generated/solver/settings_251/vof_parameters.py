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

from .vof_formulation import vof_formulation as vof_formulation_cls

class vof_parameters(Group):
    """
    VOF Parameters.
    """

    fluent_name = "vof-parameters"

    child_names = \
        ['vof_formulation']

    _child_classes = dict(
        vof_formulation=vof_formulation_cls,
    )

