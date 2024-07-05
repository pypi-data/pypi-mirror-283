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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff8b0a59e0>), ('PMI2', <function <lambda> at 0xffff8b0a60c0>), ('PMI3', <function <lambda> at 0xffff8b0a6160>), ('NPR1', <function <lambda> at 0xffff8b0a6200>), ('NPR2', <function <lambda> at 0xffff8b0a62a0>), ('RadiusOfGyration', <function <lambda> at 0xffff8b0a6340>), ('InertialShapeFactor', <function <lambda> at 0xffff8b0a63e0>), ('Eccentricity', <function <lambda> at 0xffff8b0a6480>), ('Asphericity', <function <lambda> at 0xffff8b0a6520>), ('SpherocityIndex', <function <lambda> at 0xffff8b0a65c0>), ('PBF', <function <lambda> at 0xffff8b0a6660>)]
