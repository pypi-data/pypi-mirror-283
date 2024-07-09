"""
Wrappers for the entire interface replacing all quantities with astropy units.

"""

from astropy import units as u

from .. import core as _core
from .. import density as _density
from .. import mass as _mass

atomic_mass_units = u.u
number_density_units = 1/u.cm**3
density_units = u.g/u.cm**3
electron_charge_units = u.e


# Note: only need __getattr__ not __setattr__ since tables are read-only

class PeriodicTable(_core.PeriodicTable):
    __doc__ = _core.PeriodicTable.__doc__
    def __init__(self, table):
        # type: (str) -> None
        _core.PeriodicTable.__init__(self, table)
        self._element = {el.number: _wrap_element(el) for el in self}
        # set all the toplevel symbols to the wrapped elements.
        for el in self:
            setattr(self, el.symbol, el)
        # _wrap_element wraps the defined isotopes, so just need to update
        # the top level D and T symbols
        self.D = self.H[2]
        self.T = self.H[3]


class Element(object):
    def __init__(self, base_element):
        # type: (str, str, int, List[int], str) -> None
        _core.Element.__init__(self, name, symbol, Z, ions, table)
        self._isotopes = {k: _wrap_isotope(v) for k, v in self._isotopes.items()}

class Isotope(_core.Isotope):
    def __init__(self, element, isotope_number):
        # type: (Element, int) -> None
        _core.Isotope.__init__(self, element, isotope_number)

class Ion(_core.Ion):
    def __init__(self, element, charge):
        # type: (Element, int) -> None
        # Note: not doing proper superclass call because charge becomes property
        self.element = element
        self._charge = charge
    @property
    def charge(self):
        return self._base.charge * electron_charge_units

def _wrap_element(el):
    return Element(el.name, el.symbol, el.Z, el.ions, el.table)

def _wrap_isotope(iso):
    return Isotope(iso.element, iso.isotope)


# Mass and density are preloaded

def _mass_with_units(iso_el):
    return _mass.mass(iso_el) * atomic_mass_units

def _density_with_units(iso_el):
    return _density.density(iso_el) * density_units

def _number_density_with_units(iso_el):
    return _density.number_density(iso_el) * density_units

Element.mass = property(_mass_with_units, _core.Element.mass.__doc__)
Element.density = property(_density_with_units, _core.Element.density.__doc__)
Element.number_density = property(_number_density_with_units, _core.Element.number_density.__doc__)
Isotope.mass = property(_mass_with_units, _core.Isotope.mass.__doc__)
Isotope.density = property(_density_with_units, _core.Isotope.density.__doc__)
Isotope.number_density = property(_number_density_with_units, _core.Isotope.number_density.__doc__)

