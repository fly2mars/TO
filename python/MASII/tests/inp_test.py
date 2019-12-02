# -*- coding: utf-8 -*-
"""
"""
import copy
import unittest
import numpy as np
import sys, os
if __name__ == '__main__':    
    sys.path.append("..")
    import utils.beso_lib
    


class TestClass(unittest.TestCase):    
        
    def test_read_inp(self):
        domain_optimized = {}
        file_name = "../examples/MBB_L2_C2.inp"
        elset_name = "SolidMaterialElementGeometry2D"  # string with name of the element set in .inp file
        domain_optimized[elset_name] = True  # True - optimized domain, False - elements will not be removed
        domains_from_config = domain_optimized.keys()
        shells_as_composite = False  # True - use more integration points to catch bending stresses (ccx 2.12 WILL FAIL for other than S8R and S6 shell elements)
                                    # False - use ordinary shell section        
        
        [nodes, Elements, domains, opt_domains, en_all, plane_strain, plane_stress, axisymmetry] = utils.beso_lib.import_inp(
                                                  file_name, domains_from_config, domain_optimized, shells_as_composite)
        
        np_nodes = np.array(list(nodes.values()))
        print(np_nodes)
        print(np_nodes.shape)
        print(opt_domains)
        print(en_all)
        print(plane_strain)
        print(plane_stress)
        
      
if __name__ == '__main__':
    unittest.main()