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
descList: list  # value = [('PMI1', <function <lambda> at 0x000001B4AB318CC0>), ('PMI2', <function <lambda> at 0x000001B4AB319300>), ('PMI3', <function <lambda> at 0x000001B4AB319440>), ('NPR1', <function <lambda> at 0x000001B4AB3194E0>), ('NPR2', <function <lambda> at 0x000001B4AB319580>), ('RadiusOfGyration', <function <lambda> at 0x000001B4AB319620>), ('InertialShapeFactor', <function <lambda> at 0x000001B4AB3196C0>), ('Eccentricity', <function <lambda> at 0x000001B4AB319760>), ('Asphericity', <function <lambda> at 0x000001B4AB319800>), ('SpherocityIndex', <function <lambda> at 0x000001B4AB3198A0>), ('PBF', <function <lambda> at 0x000001B4AB319940>)]
