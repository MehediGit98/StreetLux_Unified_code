"""Independent regression checks; standard library unittest, no pytest required."""
from pathlib import Path
import json, sys, unittest
ROOT=Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
sys.path.insert(0, str(SOURCE / 'streetlux'))

class SharedChecks(unittest.TestCase):
    def test_spectral_reference(self):
        from streetlux.reference_data import load_publication_references
        from streetlux import photometry,self_check,spectra
        load_publication_references(SOURCE/'reference_data')
        self.assertEqual(photometry.K_MEL_V_D65_OFFICIAL,.0013262)
        self.assertTrue(spectra.provenance()['official_action_spectra'])
        self.assertLess(abs(self_check()['der_d65']-1),.001)

    def test_strict_json(self):
        from streetlux.jsonio import dumps
        self.assertEqual(json.loads(dumps({'undefined':float('nan'),'infinite':float('inf')})),{'undefined':None,'infinite':None})

class StreetChecks(unittest.TestCase):
    def route(self):
        from streetlux.route import load_route
        return load_route(SOURCE/'streetlux/examples/dhaka_mirpur_motijheel.json')

    def test_design_invariants(self):
        from streetlux.scenarios import STANDARD_SCENARIOS
        route=self.route(); scenarios={s.key:s for s in STANDARD_SCENARIOS}
        for old,new in zip(route.sections,scenarios['widen_18'].apply(route).sections):
            self.assertGreaterEqual(new.width_m,old.width_m); new.validate()
            self.assertEqual(new.eye_offset_m,old.eye_offset_m)
        under=route.sections[3]
        for key in ['canopy_40','canopy_70']:
            new=scenarios[key].apply(route).sections[3]
            self.assertEqual(new.canopy,under.canopy)
        new=scenarios['pale_paving'].apply(route)
        self.assertEqual(new.sections[0].ground_material,'brick_pavement')
        self.assertEqual(new.sections[1].ground_material,'concrete_pavement')

    def test_invalid_eye_location(self):
        r=self.route(); r.sections[0].eye_offset_m=100
        with self.assertRaises(ValueError):r.sections[0].validate()

    def test_pareto_indices(self):
        from streetlux.scenarios import pareto_front
        rows=[{'objectives':{'x':1,'y':2}},{'objectives':{'x':4,'y':4}},{'objectives':{'x':2,'y':1}}]
        self.assertEqual(pareto_front(rows,('x','y')),[1])


class SolarChecks(unittest.TestCase):
    """Solar position against an independent implementation (astral 3.2).

    Tuples: name, latitude, longitude, UTC offset (h), (y, m, d), clock hour,
    azimuth (deg clockwise from north), altitude (deg).  These cases cover both
    hemispheres, both halves of the day and a winter date.
    """
    REFERENCE = [
        ('Dhaka 15 Mar 08:00', 23.8103, 90.4125, 6, (2026, 3, 15), 8.0, 104.34, 24.62),
        ('Dhaka 15 Mar 09:00', 23.8103, 90.4125, 6, (2026, 3, 15), 9.0, 113.08, 37.62),
        ('Dhaka 15 Mar 12:07', 23.8103, 90.4125, 6, (2026, 3, 15), 12 + 7 / 60, 179.83, 64.08),
        ('Dhaka 15 Mar 14:00', 23.8103, 90.4125, 6, (2026, 3, 15), 14.0, 230.51, 52.31),
        ('Dhaka 15 Mar 16:00', 23.8103, 90.4125, 6, (2026, 3, 15), 16.0, 253.88, 27.90),
        ('Dhaka 21 Dec 10:00', 23.8103, 90.4125, 6, (2026, 12, 21), 10.0, 147.05, 34.99),
        ('London 21 Jun 08:00', 51.5074, -0.1278, 0, (2026, 6, 21), 8.0, 97.50, 36.31),
        ('London 21 Jun 17:00', 51.5074, -0.1278, 0, (2026, 6, 21), 17.0, 273.53, 27.73),
        ('Sydney 21 Jun 10:00', -33.8688, 151.2093, 10, (2026, 6, 21), 10.0, 29.98, 26.34),
        ('Sydney 21 Jun 14:00', -33.8688, 151.2093, 10, (2026, 6, 21), 14.0, 328.62, 25.68),
    ]

    def test_azimuth_and_altitude_match_reference(self):
        from streetlux.sun import solar_position
        for name, lat, lon, tz, ymd, hour, az, alt in self.REFERENCE:
            with self.subTest(case=name):
                s = solar_position(lat, lon, tz, *ymd, hour)
                d_az = (s.azimuth_deg - az + 180.0) % 360.0 - 180.0
                self.assertLess(abs(d_az), 0.25)
                self.assertLess(abs(s.altitude_deg - alt), 0.2)

    def test_sun_is_east_of_south_in_the_morning(self):
        from streetlux.sun import solar_position
        am = solar_position(23.8103, 90.4125, 6.0, 2026, 3, 15, 9.0).azimuth_deg
        pm = solar_position(23.8103, 90.4125, 6.0, 2026, 3, 15, 15.0).azimuth_deg
        self.assertTrue(90.0 < am < 180.0)
        self.assertTrue(180.0 < pm < 270.0)


class CanyonChecks(unittest.TestCase):
    """Canyon geometry: sun side, open-sky limit, occlusion and mirror symmetry."""

    def field(self, sec, hour=8.0):
        import numpy as np
        from streetlux.route import load_route
        from streetlux.sun import solar_position, spectral_sky
        from streetlux.sky import SkyDome, fibonacci_sphere
        from streetlux.canyon import EyeField
        route = load_route(SOURCE / 'streetlux/examples/dhaka_mirpur_motijheel.json')
        sun = solar_position(route.site.latitude, route.site.longitude,
                             route.site.timezone_hours, route.year, route.month,
                             route.day, hour)
        sky = spectral_sky(sun, route.atmosphere)
        dirs = fibonacci_sphere(768)
        return EyeField(sec, SkyDome(sky, dirs), sky, dirs, 4.0 * np.pi / 768), dirs

    def test_beam_reaches_the_eye_only_from_the_low_side(self):
        from streetlux.canyon import CanyonSection
        # East-west street travelled eastward: the right of travel is south.
        # At 08:00 on 15 March in Dhaka the sun is south-east (about 104 deg,
        # 25 deg high), i.e. on the right.
        low_right = CanyonSection('ew-low-south', 100, 90.0, width_m=12,
                                  left_height_m=40, right_height_m=6)
        low_left = CanyonSection('ew-low-north', 100, 90.0, width_m=12,
                                 left_height_m=6, right_height_m=40)
        self.assertTrue(self.field(low_right)[0].beam.any())
        self.assertFalse(self.field(low_left)[0].beam.any())

    def test_open_sky_limit(self):
        import numpy as np
        from streetlux.canyon import CanyonSection, WALL_L, WALL_R
        for hour in (8.0, 16.0):
            with self.subTest(hour=hour):
                sec = CanyonSection('open', 100, 90.0, width_m=2000,
                                    left_height_m=0.1, right_height_m=0.1)
                fld, dirs = self.field(sec, hour)
                self.assertFalse(np.isin(fld.code, (WALL_L, WALL_R)).any())
                self.assertAlmostEqual(fld.sky_view_fraction,
                                       float(np.mean(dirs[:, 2] > 0.0)), places=9)
                self.assertTrue(fld.beam.any())

    def test_occlusion_is_monotonic(self):
        from streetlux.canyon import CanyonSection
        svf = [self.field(CanyonSection('c', 100, 90.0, width_m=12,
                                        left_height_m=h, right_height_m=h))[0].sky_view_fraction
               for h in (0.1, 10.0, 40.0)]
        self.assertGreater(svf[0], svf[1])
        self.assertGreater(svf[1], svf[2])
        self.assertGreater(svf[2], 0.0)

    def test_mirrored_street_gives_the_same_irradiance(self):
        import numpy as np
        from streetlux.canyon import CanyonSection
        # The same physical street described from the opposite travel direction.
        a = CanyonSection('a', 100, 30.0, width_m=14, left_height_m=10, right_height_m=35,
                          left_material='whitewash', right_material='grey_concrete',
                          eye_offset_m=2.0)
        b = CanyonSection('b', 100, 210.0, width_m=14, left_height_m=35, right_height_m=10,
                          left_material='grey_concrete', right_material='whitewash',
                          eye_offset_m=-2.0)
        headings = np.arange(0.0, 360.0, 30.0)
        ea = self.field(a, 9.0)[0].vertical_irradiance(headings)
        eb = self.field(b, 9.0)[0].vertical_irradiance(headings)
        np.testing.assert_allclose(ea, eb, rtol=1e-6, atol=1e-12)


if __name__ == '__main__':
    unittest.main(verbosity=2)
