from super_scad.Context import Context
from super_scad.d2.Import2D import Import2D
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Scale2D import Scale2D
from super_scad.transformation.Scale3D import Scale3D
from super_scad.transformation.Translate3D import Translate3D


class Pawn(ScadObject):
    """
    Generates OpenSCAD code for a pawn.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        path = context.resolve_path('include/pawn_profile.svg')

        extrude = RotateExtrude(convexity=10,
                                fn=64,
                                child=Scale2D(factor=0.25,
                                              child=Import2D(path=path)))

        return Translate3D(z=-28.0,
                           child=Scale3D(factor=0.2,
                                         child=Translate3D(z=140.0,
                                                           child=extrude)))

# ----------------------------------------------------------------------------------------------------------------------
