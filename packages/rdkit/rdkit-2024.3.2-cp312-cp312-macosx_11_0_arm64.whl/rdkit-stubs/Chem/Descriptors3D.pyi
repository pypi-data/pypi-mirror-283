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
descList: list  # value = [('PMI1', <function <lambda> at 0x104ae96c0>), ('PMI2', <function <lambda> at 0x106647a60>), ('PMI3', <function <lambda> at 0x106647b00>), ('NPR1', <function <lambda> at 0x106647ba0>), ('NPR2', <function <lambda> at 0x106647c40>), ('RadiusOfGyration', <function <lambda> at 0x106647ce0>), ('InertialShapeFactor', <function <lambda> at 0x106647d80>), ('Eccentricity', <function <lambda> at 0x106647e20>), ('Asphericity', <function <lambda> at 0x106647ec0>), ('SpherocityIndex', <function <lambda> at 0x106647f60>), ('PBF', <function <lambda> at 0x107e4c040>)]
