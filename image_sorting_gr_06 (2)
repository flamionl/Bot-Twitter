import os
import os.path
import deep_learning
def dico_creation(path) :
    dico = {}
    dirs = os.listdir(path)
    for files in dirs :
        new_dirs = os.listdir(path+'/'+files)
        updated_path = path+'/'+files
        for files in new_dirs :
            new_updated_path = updated_path+'/'+files
            print(new_updated_path)
            dico[files] = deep_learning.transform_image(new_updated_path, deep_learning.load_network('MobileNet'))
    return dico
dico = dico_creation('/home/louis/Documents/Mini_Projet 3/Environnement test')
print(dico)
