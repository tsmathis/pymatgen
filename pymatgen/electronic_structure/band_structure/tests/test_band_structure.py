#!/usr/bin/python

import unittest
import os
import json

from pymatgen.electronic_structure.band_structure.band_structure import Kpoint
from pymatgen.core.structure import Lattice
from pymatgen.electronic_structure.core import Spin
from pymatgen.electronic_structure.band_structure.band_structure import BandStructureSymmLine

module_dir = os.path.dirname(os.path.abspath(__file__))

class KpointTest(unittest.TestCase):

    def setUp(self):
        self.lattice = Lattice.cubic(10.0)
        self.kpoint = Kpoint([0.1, 0.4, -0.5], self.lattice, label = "X")

    def test_properties(self):
        self.assertEquals(self.kpoint.frac_coords[0], 0.1)
        self.assertEquals(self.kpoint.frac_coords[1], 0.4)
        self.assertEquals(self.kpoint.frac_coords[2], -0.5)
        self.assertEquals(self.kpoint.a, 0.1)
        self.assertEquals(self.kpoint.b, 0.4)
        self.assertEquals(self.kpoint.c, -0.5)
        self.assertEquals(self.lattice, Lattice.cubic(10.0))
        self.assertEquals(self.kpoint.cart_coords[0], 1.0)
        self.assertEquals(self.kpoint.cart_coords[1], 4.0)
        self.assertEquals(self.kpoint.cart_coords[2], -5.0)
        self.assertEqual(self.kpoint.label, "X")

class BandStructureSymmLine_test(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(module_dir, "CaO_2605.json"), "rb") as f:
            d = json.loads(f.read())
            #print d.keys()
            self.bs = BandStructureSymmLine.from_dict(d)
            #print self.bs.to_dict.keys()
            #this doesn't really test to_dict -> from_dict very well
            #self.assertEqual(self.bs.to_dict.keys(), d.keys())
            self.one_kpoint = self.bs.kpoints[31]
            self.assertEqual(self.bs._nb_bands, 16)
            self.assertAlmostEqual(self.bs._bands[Spin.up][5][10], 0.5608)
            self.assertAlmostEqual(self.bs._bands[Spin.up][5][10], 0.5608)
            self.assertEqual(self.bs._branches[5]['name'], "L-U")
            self.assertEqual(self.bs._branches[5]['start_index'], 80)
            self.assertEqual(self.bs._branches[5]['end_index'], 95)
            self.assertAlmostEqual(self.bs._distance[70], 4.2335127528765737)
        with open(os.path.join(module_dir, "NiO_19009.json"), "rb") as f:
            d = json.loads(f.read())
            self.bs_spin = BandStructureSymmLine.from_dict(d)
            #this doesn't really test to_dict -> from_dict very well
            #self.assertEqual(self.bs_spin.to_dict.keys(), d.keys())
            self.assertEqual(self.bs_spin._nb_bands, 27)
            self.assertAlmostEqual(self.bs_spin._bands[Spin.up][5][10], 0.262)
            self.assertAlmostEqual(self.bs_spin._bands[Spin.down][5][10], 1.6156)

    def test_properties(self):
        self.assertEqual(self.one_kpoint.frac_coords[0], 0.5)
        self.assertEqual(self.one_kpoint.frac_coords[1], 0.25)
        self.assertEqual(self.one_kpoint.frac_coords[2], 0.75)
        self.assertAlmostEqual(self.one_kpoint.cart_coords[0], 0.79508914)
        self.assertAlmostEqual(self.one_kpoint.cart_coords[1], 0.45904494)
        self.assertAlmostEqual(self.one_kpoint.cart_coords[2], 1.12442586)
        self.assertEqual(self.one_kpoint.label, "W")

        self.assertAlmostEqual(self.bs.efermi, 2.6211967, "wrong fermi energy")

    def test_get_branch_name(self):
        self.assertAlmostEqual(self.bs.get_branch_name(110)[0], "U-W")

    def test_is_metal(self):
        self.assertFalse(self.bs.is_metal(), "wrong metal assignment")
        self.assertFalse(self.bs_spin.is_metal(), "wrong metal assignment")

    def test_get_cbm(self):
        cbm = self.bs.get_cbm()
        self.assertAlmostEqual(cbm['energy'], 5.8709, "wrong CBM energy")
        self.assertEqual(cbm['band_index'][Spin.up][0], 8, "wrong CBM band index")
        self.assertEqual(cbm['kpoint_index'][0], 15, "wrong CBM kpoint index")
        self.assertEqual(cbm['kpoint'].frac_coords[0], 0.5, "wrong CBM kpoint frac coords")
        self.assertEqual(cbm['kpoint'].frac_coords[1], 0.0, "wrong CBM kpoint frac coords")
        self.assertEqual(cbm['kpoint'].frac_coords[2], 0.5, "wrong CBM kpoint frac coords")
        self.assertEqual(cbm['kpoint'].label, "X", "wrong CBM kpoint label")
        cbm_spin = self.bs_spin.get_cbm()
        self.assertAlmostEqual(cbm_spin['energy'], 8.0458, "wrong CBM energy")
        self.assertEqual(cbm_spin['band_index'][Spin.up][0], 12, "wrong CBM band index")
        self.assertEqual(len(cbm_spin['band_index'][Spin.down]), 0, "wrong CBM band index")
        self.assertEqual(cbm_spin['kpoint_index'][0], 0, "wrong CBM kpoint index")
        self.assertEqual(cbm_spin['kpoint'].frac_coords[0], 0.0, "wrong CBM kpoint frac coords")
        self.assertEqual(cbm_spin['kpoint'].frac_coords[1], 0.0, "wrong CBM kpoint frac coords")
        self.assertEqual(cbm_spin['kpoint'].frac_coords[2], 0.0, "wrong CBM kpoint frac coords")
        self.assertEqual(cbm_spin['kpoint'].label, "\Gamma", "wrong CBM kpoint label")

    def test_get_vbm(self):
        vbm = self.bs.get_vbm()
        self.assertAlmostEqual(vbm['energy'], 2.2361, "wrong VBM energy")
        self.assertEqual(len(vbm['band_index'][Spin.up]), 3, "wrong VBM number of bands")
        self.assertEqual(vbm['band_index'][Spin.up][0], 5, "wrong VBM band index")
        self.assertEqual(vbm['kpoint_index'][0], 0, "wrong VBM kpoint index")
        self.assertEqual(vbm['kpoint'].frac_coords[0], 0.0, "wrong VBM kpoint frac coords")
        self.assertEqual(vbm['kpoint'].frac_coords[1], 0.0, "wrong VBM kpoint frac coords")
        self.assertEqual(vbm['kpoint'].frac_coords[2], 0.0, "wrong VBM kpoint frac coords")
        self.assertEqual(vbm['kpoint'].label, "\Gamma", "wrong VBM kpoint label")
        vbm_spin = self.bs_spin.get_vbm()
        self.assertAlmostEqual(vbm_spin['energy'], 5.731, "wrong VBM energy")
        self.assertEqual(len(vbm_spin['band_index'][Spin.up]), 2, "wrong VBM number of bands")
        self.assertEqual(len(vbm_spin['band_index'][Spin.down]), 0, "wrong VBM number of bands")
        self.assertEqual(vbm_spin['band_index'][Spin.up][0], 10, "wrong VBM band index")
        self.assertEqual(vbm_spin['kpoint_index'][0], 79, "wrong VBM kpoint index")
        self.assertEqual(vbm_spin['kpoint'].frac_coords[0], 0.5, "wrong VBM kpoint frac coords")
        self.assertEqual(vbm_spin['kpoint'].frac_coords[1], 0.5, "wrong VBM kpoint frac coords")
        self.assertEqual(vbm_spin['kpoint'].frac_coords[2], 0.5, "wrong VBM kpoint frac coords")
        self.assertEqual(vbm_spin['kpoint'].label, "L", "wrong VBM kpoint label")

    def test_get_band_gap(self):
        bg = self.bs.get_band_gap()
        self.assertAlmostEqual(bg['energy'], 3.6348, "wrong gap energy")
        self.assertEqual(bg['transition'], "\\Gamma-X", "wrong kpoint transition")
        self.assertFalse(bg['direct'], "wrong nature of the gap")
        bg_spin = self.bs_spin.get_band_gap()
        self.assertAlmostEqual(bg_spin['energy'], 2.3148, "wrong gap energy")
        self.assertEqual(bg_spin['transition'], "L-\\Gamma", "wrong kpoint transition")
        self.assertFalse(bg_spin['direct'], "wrong nature of the gap")

if __name__ == '__main__':
    unittest.main()
