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
descList: list  # value = [('PMI1', <function <lambda> at 0x1087919e0>), ('PMI2', <function <lambda> at 0x10e376fc0>), ('PMI3', <function <lambda> at 0x10e377100>), ('NPR1', <function <lambda> at 0x10e3771a0>), ('NPR2', <function <lambda> at 0x10e377240>), ('RadiusOfGyration', <function <lambda> at 0x10e3772e0>), ('InertialShapeFactor', <function <lambda> at 0x10e377380>), ('Eccentricity', <function <lambda> at 0x10e377420>), ('Asphericity', <function <lambda> at 0x10e3774c0>), ('SpherocityIndex', <function <lambda> at 0x10e377560>), ('PBF', <function <lambda> at 0x10e377600>)]
