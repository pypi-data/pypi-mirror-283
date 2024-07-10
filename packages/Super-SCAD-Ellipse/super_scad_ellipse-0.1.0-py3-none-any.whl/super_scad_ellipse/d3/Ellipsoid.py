from super_scad.d3.Sphere import Sphere
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Resize3D import Resize3D
from super_scad.type.Size3 import Size3
from super_scad.util.Radius2Sides4n import Radius2Sides4n


class Ellipsoid(ScadWidget):
    """
    Widget for creating ellipsoids.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius_x: float | None = None,
                 radius_y: float | None = None,
                 radius_z: float | None = None,
                 diameter_x: float | None = None,
                 diameter_y: float | None = None,
                 diameter_z: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param radius_x: The radius of the ellipsoid in x-direction.
        :param radius_y: The radius of the ellipsoid in y-direction.
        :param radius_z: The radius of the ellipsoid in z-direction.
        :param diameter_x: The diameter of the ellipsoid in x-direction.
        :param diameter_y: The diameter of the ellipsoid in y-direction.
        :param diameter_z: The diameter of the ellipsoid in z-direction.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a circle with a ellipsoid of 4 vertices.
        """
        ScadWidget.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'radius_x'}, {'diameter_x'})
        admission.validate_exclusive({'radius_y'}, {'diameter_y'})
        admission.validate_exclusive({'radius_z'}, {'diameter_z'})
        admission.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})
        admission.validate_required({'radius_x', 'diameter_x'},
                                    {'radius_y', 'diameter_y'},
                                    {'radius_z', 'diameter_z'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_x(self) -> float:
        """
        Returns the radius of the ellipsoid in x-direction.
        """
        return self.uc(self._args.get('radius_x', 0.5 * self._args.get('diameter_x', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_y(self) -> float:
        """
        Returns the radius of the ellipsoid in y-direction.
        """
        return self.uc(self._args.get('radius_y', 0.5 * self._args.get('diameter_y', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_z(self) -> float:
        """
        Returns the radius of the ellipsoid in z-direction.
        """
        return self.uc(self._args.get('radius_z', 0.5 * self._args.get('diameter_z', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_x(self) -> float:
        """
        Returns the length of the ellipsoid in x-direction.
        """
        return self.uc(self._args.get('diameter_x', 2.0 * self._args.get('radius_x', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_y(self) -> float:
        """
        Returns the length of the ellipsoid in y-direction.
        """
        return self.uc(self._args.get('diameter_y', 2.0 * self._args.get('radius_y', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_z(self) -> float:
        """
        Returns the length of the ellipsoid in z-direction.
        """
        return self.uc(self._args.get('diameter_z', 2.0 * self._args.get('radius_z', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.uc(self._args.get('fs'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._args.get('fn4n')

    # ------------------------------------------------------------------------------------------------------------------
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self.fn4n:
            return Radius2Sides4n.r2sides4n(max(self.radius_x, self.radius_y, self.radius_z), context)

        return self.fn

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        diameter: float = max(self.diameter_x, self.diameter_y, self.diameter_z)

        return Resize3D(new_size=Size3(self.diameter_x, self.diameter_y, self.diameter_z),
                        child=Sphere(diameter=diameter, fa=self.fa, fs=self.fs, fn=self.real_fn(context)))

# ----------------------------------------------------------------------------------------------------------------------
