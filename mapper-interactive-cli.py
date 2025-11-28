import pandas as pd
import argparse
import os
import linecache
import re
import networkx as nx
import app.views as MI  # MapperInteractive
from app import kmapper as km
from app import cover as km_cover
from sklearn.cluster import DBSCAN, MeanShift, AgglomerativeClustering
import json
import numpy as np
from os.path import join
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler, normalize
import l2
from anchored_vis import anchor

def mkdir(f):
    if not os.path.exists(f):
        os.mkdir(f)
    assert os.path.isdir(f), 'Not an output directory!'


def extract_range(s):
    s = s.strip().split(':')
    assert len(
        s) == 3, 'Invalid input format to either overlaps or intervals argument'
    try:
        params = [int(x) for x in s]
    except:
        print(
            'ERROR: Unable to parse input format to either overlaps or intervals argument')
        exit()
    for x in params:
        assert x > 0, 'Can not have non-positive values for overlaps or intervals argument'
    choices = [params[0] + params[-1] *
               i for i in range((params[1]-params[0]) // params[-1])]
    choices.append(params[1])
    return choices


def get_filter_fn(X, filter, filter_params=None):
    mapper = km.KeplerMapper()
    if type(filter) is not list:
        filter_fn = MI.compute_lens(filter, X, mapper, filter_params)
    else:
        lens = []
        for f in filter:
            lens_f = MI.compute_lens(filter, X, mapper, filter_params)
            lens.append(lens_f)
        filter_fn = np.concatenate((lens[0], lens[1]), axis=1)
    return filter_fn


def mapper_wrapper(X, overlap, intervals, filter_fn, clusterer, **mapper_args):
    mapper = km.KeplerMapper()
    #print(filter_fn[2])
    graph = mapper.map_parallel(filter_fn, X, clusterer=clusterer, cover=km_cover.Cover(
        n_cubes=intervals, perc_overlap=overlap / 100), **mapper_args)
    return graph


def graph_to_dict(g, **kwargs):
    d = {}
    d['nodes'] = {}
    d['edges'] = {}
    for k in g['nodes']:
        d['nodes'][k] = g['nodes'][k]
    for k in g['links']:
        d['edges'][k] = g['links'][k]
    for k in kwargs.keys():
        d[k] = kwargs[k]
    return d



def wrangle_csv(df):
    '''
    Check for:
    1. Missing value
    2. Non-numerical elements in numerical cols
    3. If cols are non-numerical, check if cols are categorical
    '''
    cols = list(df.columns.values)
    cols = [col for col in cols if col!=""] # not include the col is there is no colname
    #mat = [n.split(',') for n in ] # csv: if an element is empty, it will be "".
    newdf1 = df.to_numpy()[0:]
    rows2delete = np.array([])
    cols2delete = []

    # ### Delete missing values ###
    for i in range(len(cols)):
        col = newdf1[:, i]
        # if more than 20% elements in this column are empty, delete the whole column
        if np.sum(col == "") >= 0.2*len(newdf1):
            cols2delete.append(i)
        else:
            rows2delete = np.concatenate((rows2delete, np.where(col == "")[0]))
    rows2delete = np.unique(rows2delete).astype("int")
    newdf2 = np.delete(np.delete(newdf1, cols2delete,
                                 axis=1), rows2delete, axis=0)
    cols = [cols[i] for i in range(len(cols)) if i not in cols2delete]

    ### check if numerical cols ###
    cols_numerical_idx = []
    cols_categorical_idx = []
    cols_others_idx = []
    rows2delete = np.array([]) 
    

    #vmatch = np.vectorize(lambda x:bool(r1.match(x) or r2.match(x)))
    r1 = re.compile(r'^-?\d+(?:\.\d+)?$')
    r2 = re.compile(r'[+\-]?[^A-Za-z]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)') # scientific notation
    vmatch = np.vectorize(lambda x:bool(r1.match(x) or r2.match(x)))
    for i in range(len(cols)):
        col = newdf2[:, i]
        col = [str(i) for i in col]
        col_match = vmatch(col)
        # if more than 90% elements can be converted to float, keep the col, and delete rows that cannot be convert to float:
        if np.sum(col_match) >= 0.8*len(newdf1):
            cols_numerical_idx.append(i)
            rows2delete = np.concatenate(
                (rows2delete, np.where(col_match == False)[0]))
        else:
            ### check if categorical cols###
            if len(np.unique(col)) <= 40:  # if less than 10 different values: categorical
                cols_categorical_idx.append(i)
            else:
                cols_others_idx.append(i)
    newdf3 = newdf2[:, cols_numerical_idx+cols_categorical_idx+cols_others_idx]
    rows2delete = rows2delete.astype(int)
    newdf3 = np.delete(newdf3, rows2delete, axis=0)
    newdf3_cols = [cols[idx] for idx in cols_numerical_idx +
                   cols_categorical_idx+cols_others_idx]
    newdf3 = pd.DataFrame(newdf3)
    newdf3.columns = newdf3_cols
    # write the data frame
    newdf3.to_csv(output_dir+"/processed_data.csv", index=False)
    # For only the numerical cols
    newdf4 = np.array(newdf3)
    newdf4_cols = [cols[idx] for idx in cols_numerical_idx]
    newdf4 = np.delete(newdf4, cols_categorical_idx+cols_others_idx, axis=1)

    newdf4 = pd.DataFrame(newdf4)
    newdf4.columns = newdf4_cols
    newdf4.to_csv(join(output_dir, 'wrangled_data.csv'),index=False)

    return newdf4

# Only for the chemical mapper
def for_label_scaffold(filename,array,scaffold_col,label_col):
    categorical = {"label":{},"scaffold":{}}
    for i in array:
        line = linecache.getline(output_dir+'/processed_data.csv', i+2)
        label = line.split(',')[label_col]
        scaffold = line.split(',')[scaffold_col]
        if label not in categorical["label"]:
            categorical["label"][label] = 1
        else:
            categorical["label"][label] = categorical["label"][label] + 1
        
        if scaffold not in categorical["scaffold"]:
            categorical["scaffold"][scaffold] = 1
        else:
            categorical["scaffold"][scaffold] = categorical["scaffold"][scaffold] + 1   
    return categorical

def mean_property(array, property_col,output_dir):
    sum = 0
    for i in array:
        line = linecache.getline(output_dir+'/processed_data.csv', i+2)
        property = line.split(',')[property_col]
        property = property.replace('l','')
        property = property.replace('\n','')
        property = float(property)
        sum = sum + property
        

    return sum/len(array)

def compute_cc(graph): 
    '''
    Compute connected components for the mapper graph
    '''
    G = nx.Graph()
    for node in graph['nodes']:
        nodeId = int(node['id'])-1
        G.add_node(nodeId)
    for edge in graph['links']:
        sourceId = int(edge['source'])-1
        targetId = int(edge['target'])-1
        G.add_edge(sourceId, targetId)
    cc = nx.connected_components(G)
    cc_list = []
    for c in cc:
        cc_list.append(list(c))
    return cc_list

def normalize_data(X, norm_type):
    if norm_type == "none" or norm_type is None:
        X_prime = X
        pass
    elif norm_type == "0-1":  # axis=0, min-max norm for each column
        scaler = MinMaxScaler()
        X_prime = scaler.fit_transform(X)
    else:
        X_prime = normalize(X, norm=norm_type, axis=0,
                            copy=False, return_norm=False)
    return X_prime


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Mapper Interactive Command Line Tool. \nSee CLI_README.md for details.')
    parser.add_argument('input', type=str,
                        help='Specific input (must be CSV file)')
    parser.add_argument('-i', '--intervals', type=int, required=True,
                        help='Expects number of intervals')
    parser.add_argument('-o', '--overlap', type=int, required=True,
                        help='Expects a %')
    parser.add_argument('-f', '--filter', type=str,
                        help='Which filter function to use. See docs for choices.')
    parser.add_argument('-output', type=str,
                        help='Output Directory. Defaults to "./CLI_examples/"', default='./CLI_examples/')
    parser.add_argument('--no-preprocess', action='store_true')
    parser.add_argument('--threads', type=int, default=16,
                        help='Number of threads to allocate')

    parser.add_argument('--clusterer', type=str, required=False,
                        choices=['dbscan', 'agglomerative', 'meanshift', None], default='dbscan')

    # DBSCAN args
    parser.add_argument('--eps', type=float,
                        help='DBSCAN Epsilon', required=False, default=-1)
    parser.add_argument('--min_samples', type=int,
                        help='DBSCAN Min points', required=False, default=-1)

    # Agglomerative args
    # parser.add_argument('--linkage', help='Type of agglomerative clustering',
    #                     choices=[-1, 'ward', 'complete', 'average', 'single'], default=-1, required=False)
    # parser.add_argument('--distance_threshold', help='Distance threshold for agglomerative clustering',
    #                     type=float, default=-1, required=False)

    # Mean Shift args
    parser.add_argument(
        '--bandwidth', type=str, help='bandwidth for mean shift. If "None" is supplied, scikit-learn estimator is used', default='NA', required=False)

    parser.add_argument('--norm', help='Normalization of points', default=None)
    parser.add_argument('--gpu', action='store_true',
                         help='id(s) for CUDA_VISIBLE_DEVICES')
    parser.add_argument('--metric', default='euclidean',
                         help='Metric for DBSCAN')
    parser.add_argument('--preprocess_only', action='store_true')
    args = parser.parse_args()

    fname = args.input
    interval = args.intervals
    overlap = args.overlap
    filter_str = args.filter
    output_dir = args.output
    no_preprocess = args.no_preprocess
    threads = args.threads
    gpu = args.gpu
    clustering_method = args.clusterer
    metric = args.metric
    norm = args.norm
    preprocess_only = args.preprocess_only

    # Setup
    mkdir(output_dir)
    df = pd.read_csv(fname)
    if preprocess_only:
        df = wrangle_csv(df)
        #df.to_csv(join(output_dir, 'wrangled_data.csv'),index = False)
        exit()
    elif not no_preprocess:
        df = wrangle_csv(df)

    # Regardless, we want normalize_datato save the data for bookkeeping
    df_np = df.to_numpy()
    df_np = np.float32(df_np)#Very important line
    df_np = normalize_data(df_np, norm_type=norm)
    # overlaps = extract_range(overlaps_str)
    # intervals = extract_range(intervals_str)
    filter_fn = get_filter_fn(df_np, filter_str, filter_params=None)

    meta = {'data': fname, 'interval': interval,
            'overlap': overlap, 'filter': filter_str, 'normalization': norm}

    assert clustering_method is not None, 'Cant run mapper without specifying a clustering method!'
    meta['Clustering_method'] = clustering_method
    if clustering_method == 'dbscan':
        assert args.eps != -1, 'Must specify eps for DBSCAN'
        assert args.min_samples != -1, 'Must specify min_samples for DBSCAN'
        meta['DBSCAN_eps'] = args.eps
        meta['DBSCAN_min_samples'] = args.min_samples
        clusterer = DBSCAN(eps=args.eps, min_samples=args.min_samples)
    # elif clustering_method == 'agglomerative':
    #     assert args.linkage is not None, 'Linkage must be provided for Agglomerative Clustering'
    #     assert args.distance_threshold != - \
    #         1, 'Distance threshold must be specified for Agglomerative Clustering'
    #     meta['Agglomerative_linkage'] = args.linkage
    #     meta['Agglomerative_distance_threshold'] = args.distance_threshold
    #     clusterer = AgglomerativeClustering(
    #         linkage=args.linkage, distance_threshold=args.distance_threshold)
    elif clustering_method == 'meanshift':
        assert args.bandwidth != 'NA', 'Must specify bandwidth for Mean Shift (Did you mean to use None?)'
        if args.bandwidth == 'none' or args.bandwidth == 'None':
            bandwidth = None
        else:
            try:
                bandwidth = float(args.bandwidth)
            except:
                assert False, 'No float value passed to bandwidth for Mean Shift'
        meta['MeanShift_bandwidth'] = 'None' if bandwidth is None else bandwidth
        clusterer = MeanShift(bandwidth=args.bandwidth)
    
    # Picking the right scaffold column
    col_names = linecache.getline(output_dir+'/processed_data.csv', 1)
    col_names = col_names.split(',')

    scaffold_col = col_names.index('Scaffold')
    struct_col = col_names.index('Structure\n')
    label_col = col_names.index('Label')
    
    #for overlap, interval in tqdm(itertools.product(overlaps, intervals)):

    g = graph_to_dict(mapper_wrapper(
        df_np, overlap, interval, filter_fn, clusterer, n_threads=threads, metric=metric, use_gpu=True))

    g["links"] = g["edges"]
    del g["edges"]
    data = {"nodes": [], "links": []}
    node_keys = g['nodes'].keys()
    i =1
    name2id = {}
    for key in node_keys:
        cluster = g['nodes'][key]
        name2id[key] = i
        data['nodes'].append({
        "id": str(i),
        "id_orignal": key,
        "size": len(g['nodes'][key]),
        "vertices": cluster,
        "avgs":{},
        "categorical_cols_summary":for_label_scaffold(output_dir+'/processed_data.csv',cluster,scaffold_col,label_col)
                    })
        i = i+1
        
    # links
    links = set()
    for link_from in g['links'].keys():
        for link_to in g['links'][link_from]:
            from_id = name2id[link_from]
            to_id = name2id[link_to]
            left_id = min(from_id, to_id)
            right_id = max(from_id, to_id)
            links.add((left_id, right_id))
    for link in links:
        data['links'].append({"source": link[0], "target": link[1]})
        
    connected_components = compute_cc(data)
    to_dump = {'mapper':data,'col_keys':['l2_norm'],'connected_components':connected_components,'categorical_cols':['label','scaffold']}

    if clustering_method == 'dbscan':
        with open(output_dir+'/final_'+str(interval)+'_'+str(overlap)+'_'+str(args.eps)+'_'+str(args.min_samples)+'.json', 'w') as fp:
                json.dump(to_dump, fp)
        l2.l2(output_dir+'/final_'+str(interval)+'_'+str(overlap)+'_'+str(args.eps)+'_'+str(args.min_samples)+'.json')
        anchor.anchor(output_dir+'/final_'+str(interval)+'_'+str(overlap)+'_'+str(args.eps)+'_'+str(args.min_samples)+'.json')
        print("COMPLETE")

    if clustering_method == 'meanshift':
        with open(output_dir+'/final_'+str(interval)+'_'+str(overlap)+'_'+str(bandwidth)+'.json', 'w') as fp:
                json.dump(to_dump, fp)
        l2.l2(output_dir+'/final_'+str(interval)+'_'+str(overlap)+'_'+str(bandwidth)+'.json')
        anchor.anchor(output_dir+'/final_'+str(interval)+'_'+str(overlap)+'_'+str(bandwidth)+'.json')
        print("COMPLETE")
