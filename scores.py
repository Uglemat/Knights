import os
import yaml

highscores_file = ".highscores.yaml"

def submit_score(score):
    if os.path.exists(highscores_file):
        f = open(highscores_file,"r")
        highscores = f.read()
        highscores = yaml.load(highscores)
        f.close()
    else:
        highscores = {'highscores':[]}
    with open(highscores_file,"w") as hs:
        highscores['highscores'].append(score)
        hs.write(yaml.dump(highscores))

def get_highscores(n):
    if not os.path.exists(highscores_file):
        return []
    with open(highscores_file,"r") as hs:
        highscores = yaml.load(hs.read())['highscores']
        highscores.sort(reverse=True)

        return highscores[0:n]
