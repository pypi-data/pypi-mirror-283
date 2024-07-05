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
descList: list  # value = [('PMI1', <function <lambda> at 0x0000022918C66CA0>), ('PMI2', <function <lambda> at 0x000002291F9091F0>), ('PMI3', <function <lambda> at 0x000002291F909280>), ('NPR1', <function <lambda> at 0x000002291F909310>), ('NPR2', <function <lambda> at 0x000002291F9093A0>), ('RadiusOfGyration', <function <lambda> at 0x000002291F909430>), ('InertialShapeFactor', <function <lambda> at 0x000002291F9094C0>), ('Eccentricity', <function <lambda> at 0x000002291F909550>), ('Asphericity', <function <lambda> at 0x000002291F9095E0>), ('SpherocityIndex', <function <lambda> at 0x000002291F909670>), ('PBF', <function <lambda> at 0x000002291F909700>)]
