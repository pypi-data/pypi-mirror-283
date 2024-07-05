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
descList: list  # value = [('PMI1', <function <lambda> at 0x000002724006E560>), ('PMI2', <function <lambda> at 0x0000027248B500D0>), ('PMI3', <function <lambda> at 0x0000027248B50160>), ('NPR1', <function <lambda> at 0x0000027248B501F0>), ('NPR2', <function <lambda> at 0x0000027248B50280>), ('RadiusOfGyration', <function <lambda> at 0x0000027248B50310>), ('InertialShapeFactor', <function <lambda> at 0x0000027248B503A0>), ('Eccentricity', <function <lambda> at 0x0000027248B50430>), ('Asphericity', <function <lambda> at 0x0000027248B504C0>), ('SpherocityIndex', <function <lambda> at 0x0000027248B50550>), ('PBF', <function <lambda> at 0x0000027248B505E0>)]
