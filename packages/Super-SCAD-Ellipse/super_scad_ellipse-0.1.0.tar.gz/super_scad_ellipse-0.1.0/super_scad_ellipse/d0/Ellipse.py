from super_scad.d2.Circle import Circle
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Resize2D import Resize2D
from super_scad.type.Size2 import Size2


class Ellipse(ScadWidget):
    """
    Widget for creating ellipses.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius_x: float | None = None,
                 radius_y: float | None = None,
                 diameter_x: float | None = None,
                 diameter_y: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        param radius_x: The radius of the ellipsis along the x-axis.
        param radius_y: The radius of the ellipsis along the y-axis.
        :param diameter_x: The diameter of the ellipsis along the x-axis.
        :param diameter_x: The diameter of the ellipsis along the y-axis.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create an ellipse with a multiple of 4 vertices.
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
        admission.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})
        admission.validate_required({'radius_x', 'diameter_x'}, {'radius_y', 'diameter_y'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_x(self) -> float:
        """
        Returns the radius of the ellipsis in x-direction.
        """
        return self.uc(self._args.get('radius_x', 0.5 * self._args.get('diameter_x', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_y(self) -> float:
        """
        Returns the radius of the ellipsis in y-direction.
        """
        return self.uc(self._args.get('radius_y', 0.5 * self._args.get('diameter_y', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_x(self) -> float:
        """
        Returns the length of the ellipsis in x-direction.
        """
        return self.uc(self._args.get('diameter_x', 2.0 * self._args.get('radius_x', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_y(self) -> float:
        """
        Returns the length of the ellipsis in y-direction.
        """
        return self.uc(self._args.get('diameter_y', 2.0 * self._args.get('radius_y', 0.0)))

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
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        diameter: float = max(self.diameter_x, self.diameter_y)

        return Resize2D(new_size=Size2(self.diameter_x, self.diameter_y),
                        child=Circle(diameter=diameter, fa=self.fa, fs=self.fs, fn=self.fn, fn4n=self.fn4n))

# ----------------------------------------------------------------------------------------------------------------------
