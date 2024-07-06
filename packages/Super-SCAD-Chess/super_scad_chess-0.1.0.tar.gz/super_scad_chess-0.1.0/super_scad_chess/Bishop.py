from super_scad.boolean.Difference import Difference
from super_scad.Context import Context
from super_scad.d2.Import2D import Import2D
from super_scad.d3.Cuboid import Cuboid
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Rotate3D import Rotate3D
from super_scad.transformation.Scale3D import Scale3D
from super_scad.transformation.Translate3D import Translate3D


class Bishop(ScadObject):
    """
    Generates OpenSCAD code for a bishop.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        path = context.resolve_path('include/bishop_profile.dxf')

        body = Difference(children=[RotateExtrude(convexity=10,
                                                  fn=64,
                                                  child=Import2D(path=path)),
                                    Rotate3D(angle_y=-45.0,
                                             child=Translate3D(x=-30.0,
                                                               child=Cuboid(width=10,
                                                                            depth=80,
                                                                            height=80,
                                                                            center=True)))])

        return Translate3D(x=34.0,
                           child=Scale3D(factor_x=0.18,
                                         factor_y=0.18,
                                         factor_z=0.2,
                                         child=body))

# ----------------------------------------------------------------------------------------------------------------------
