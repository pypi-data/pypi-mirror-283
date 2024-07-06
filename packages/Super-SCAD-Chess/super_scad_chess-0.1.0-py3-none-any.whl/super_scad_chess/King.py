from super_scad.boolean.Union import Union
from super_scad.Context import Context
from super_scad.d2.Import2D import Import2D
from super_scad.d3.LinearExtrude import LinearExtrude
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Rotate3D import Rotate3D
from super_scad.transformation.Scale2D import Scale2D
from super_scad.transformation.Scale3D import Scale3D
from super_scad.transformation.Translate3D import Translate3D


class King(ScadObject):
    """
    Generates OpenSCAD code for a king.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        path1 = context.resolve_path('include/king_profile.svg')
        path2 = context.resolve_path('include/cross_profile.svg')

        body = Scale3D(factor=0.25,
                       child=RotateExtrude(convexity=10,
                                           fn=64,
                                           child=Import2D(path=path1)))

        crown = Translate3D(x=-21.0,
                            y=8.0,
                            z=270.0,
                            child=Rotate3D(angle_x=90.0,
                                           child=LinearExtrude(height=16.0,
                                                               child=Scale2D(factor=0.22,
                                                                             child=Import2D(path=path2)))))

        return Scale3D(factor=0.2, child=Union(children=[crown, body]))

# ----------------------------------------------------------------------------------------------------------------------
