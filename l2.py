import json
import linecache
import numpy as np

def l2(filename):
    # This is for computing the l2 norm as a post-processing step.
    file = open(filename)
    mapper = json.load(file)
    for i in mapper['mapper']['nodes']:
        count = 0
        for j in i['vertices']:
            line = linecache.getline("./CLI_examples/processed_data.csv", j+2)
            vec = line.split(',')[:-3]
            vec = [float(i) for i in vec]
            count = count + np.linalg.norm(vec)
            
        count = count/len(i['vertices'])
        i['avgs']['l2_norm'] = count

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(mapper, f, ensure_ascii=False, indent=4)