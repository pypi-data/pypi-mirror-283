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
descList: list  # value = [('PMI1', <function <lambda> at 0x10be7eb90>), ('PMI2', <function <lambda> at 0x1163a1e10>), ('PMI3', <function <lambda> at 0x1163a1ea0>), ('NPR1', <function <lambda> at 0x1163a1f30>), ('NPR2', <function <lambda> at 0x1163a1fc0>), ('RadiusOfGyration', <function <lambda> at 0x1163a2050>), ('InertialShapeFactor', <function <lambda> at 0x1163a20e0>), ('Eccentricity', <function <lambda> at 0x1163a2170>), ('Asphericity', <function <lambda> at 0x1163a2200>), ('SpherocityIndex', <function <lambda> at 0x1163a2290>), ('PBF', <function <lambda> at 0x1163a2320>)]
