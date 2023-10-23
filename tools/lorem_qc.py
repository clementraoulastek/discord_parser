from typing import List
import random


JURON_LIST: List[List] = [
    ["tabarnak", "tabarnouche", "tabarouette", "taboire", "tabarslaque", "tabarnane"],
    ["câlisse", "câlique", "câline", "câline de bine", "câliboire", "caltor"],
    ["crisse", "christie", "crime", "bout d'crisse"],
    ["ostie", "astie", "estique", "ostifie", "esprit"],
    ["ciboire", "saint-ciboire"],
    ["torrieux", "torvisse"],
    ["cimonaque", "saint-cimonaque"],
    ["baptême", "batince", "batèche"],
    ["bâtard"],
    ["calvaire", "calvince", "calvinouche"],
    ["mosus"],
    ["maudit", "mautadit", "maudine"],
    ["sacrament", "sacréfice", "saint-sacrament"],
    ["viarge", "sainte-viarge", "bout d'viarge"],
    ["ciarge", "saint-ciarge", "bout d'ciarge"],
    ["cibouleau"],
    ["cibole", "cibolac"],
    ["enfant d'chienne"],
    ["verrat"],
    ["marde", "maudite marde", "mangeux d'marde", "gros tas d'marde"],
    ["boswell"],
    ["sacristi", "sapristi"],
    ["Jésus de plâtre", "Jésus Marie Joseph", "p'tit Jésus"],
    ["crucifix"],
    ["patente à gosse", "cochonnerie", "cossin"],
    ["viande à chien"],
    ["cul", "trou d'cul"],
    ["purée"],
    ["étole"],
    ["charogne", "charrue"],
    ["gériboire", "géritole"],
    ["colon"],
]

def lorem_qc(nb_of_world: int) -> str:
    return_sentence = ""
    random_row = -1
    for _ in range(nb_of_world):
        random_row = random.choice([i for i in range(len(JURON_LIST)) if i != random_row])
        random_world = random.randint(0, len(JURON_LIST[random_row]) - 1)
        return_sentence += " " 
        return_sentence += JURON_LIST[random_row][random_world]
        
    return return_sentence
