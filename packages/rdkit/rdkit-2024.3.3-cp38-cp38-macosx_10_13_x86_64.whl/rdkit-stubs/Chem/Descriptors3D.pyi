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
descList: list  # value = [('PMI1', <function <lambda> at 0x7fbccd0cf550>), ('PMI2', <function <lambda> at 0x7fbccd78ca60>), ('PMI3', <function <lambda> at 0x7fbccd78caf0>), ('NPR1', <function <lambda> at 0x7fbccd78cb80>), ('NPR2', <function <lambda> at 0x7fbccd78cc10>), ('RadiusOfGyration', <function <lambda> at 0x7fbccd78cca0>), ('InertialShapeFactor', <function <lambda> at 0x7fbccd78cd30>), ('Eccentricity', <function <lambda> at 0x7fbccd78cdc0>), ('Asphericity', <function <lambda> at 0x7fbccd78ce50>), ('SpherocityIndex', <function <lambda> at 0x7fbccd78cee0>), ('PBF', <function <lambda> at 0x7fbccd78cf70>)]
