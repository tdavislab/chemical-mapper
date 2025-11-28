import sys
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.sping import PIL
from rdkit.Chem import rdRGroupDecomposition
from PIL import Image
from PIL import ImageDraw
import linecache
import base64
from PIL import ImageFont
from rdkit.Chem import BRICS
from rdkit.Chem.Scaffolds import MurckoScaffold
import numpy as np
import pandas as pd

def draw_chem(vertices,struct_col,scaffold_col):
    images = {"success":1}
    count = 0
    for i in range(len(vertices)):
        vertices[i] = int(vertices[i])
        line = linecache.getline("./CLI_examples/processed_data.csv", vertices[i]+2)
        structure = line.split(',')[struct_col]
        #scaffold = line.split(',')[scaffold_col]
        mol = Chem.MolFromSmiles(structure)
        #scaffold = Chem.MolFromSmiles(scaffold)
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
        Draw.MolToFile(scaffold,"./temp_figs/sample_structure.png",size=(800, 800))
        lst = [mol]
        rgd,fails = rdRGroupDecomposition.RGroupDecompose([scaffold],[mol])
        for molecule in rgd[0].values():
           lst.append(molecule)
        for j in range(len(lst)):
            Draw.MolToFile(lst[j],"./temp_figs/sample.png")
            Draw.MolToFile(lst[j],"./temp_figs/sample" + str(j) + ".png",size=(800, 800))
            #myFont = ImageFont.truetype('FreeMono.ttf', 25)
            myFont = ImageFont.load_default()
            if j == 0:
                img = Image.open("./temp_figs/sample.png")
                I1 = ImageDraw.Draw(img)
                I1.text((125, 5), "Structure", fill=(0, 0, 0),font=myFont)
                img.save("./temp_figs/sample.png")
            elif j == 1:
                img = Image.open("./temp_figs/sample.png")
                I1 = ImageDraw.Draw(img)
                I1.text((125, 5), "Scaffold", fill=(0, 0, 0),font=myFont)
                img.save("./temp_figs/sample.png")
            else:
                img = Image.open("./temp_figs/sample.png")
                I1 = ImageDraw.Draw(img)
                I1.text((125, 5), "Group", fill=(0, 0, 0),font=myFont)
                img.save("./temp_figs/sample.png")
            with open("./temp_figs/sample.png", "rb") as img_file:
                images[count] = {'image':base64.b64encode(img_file.read()).decode("utf-8"),'group':j,'vertex':i}
            count = count + 1
    return images



