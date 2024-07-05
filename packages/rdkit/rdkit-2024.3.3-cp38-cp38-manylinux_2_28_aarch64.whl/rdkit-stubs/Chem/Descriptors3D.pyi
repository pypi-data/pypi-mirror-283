"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0xffffbad83e50>), ('PMI2', <function <lambda> at 0xffffae1a8dc0>), ('PMI3', <function <lambda> at 0xffffae1a8e50>), ('NPR1', <function <lambda> at 0xffffae1a8ee0>), ('NPR2', <function <lambda> at 0xffffae1a8f70>), ('RadiusOfGyration', <function <lambda> at 0xffffade5e040>), ('InertialShapeFactor', <function <lambda> at 0xffffade5e0d0>), ('Eccentricity', <function <lambda> at 0xffffade5e160>), ('Asphericity', <function <lambda> at 0xffffade5e1f0>), ('SpherocityIndex', <function <lambda> at 0xffffade5e280>), ('PBF', <function <lambda> at 0xffffade5e310>)]
