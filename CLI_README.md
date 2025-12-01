# Mapper Interactive Command Line Interface

---

### Additional Requirements:

* [tqdm](https://github.com/tqdm/tqdm)
* [PyTorch](https://pytorch.org/) (If GPU acceleration is desired. CUDA device required.)

---

### Quickstart

To only perform data wrangling:

```bash
python data.csv --preprocess-only
```

Example mapper graph computation with parameters:

* Intervals 50
* Overlap 30%
* DBSCAN Epsilon = 0.5
* DBSCAN num_pts = 5
* Filter Function = L2norm
* Graphs stored in ./`CLI_examples/`

```bash
python data.csv --intervals 50 --overlap 30 --clusterer dbscan --eps 0.5 --min_samples 5 --filter l2norm --output ./CLI_examples
```

---

### Output format

Unless specified with the output flag, the default export directory is `./CLI_examples/`. Each mapper graph has the form "final\_{interval}\_{overlap}\_{epsilon}\_{min samples}.json" where overlap is the integer representing a percent (i.e. 35 for 35%). There are two additional files. `./CLI_examples/wrangled_data.csv` contains the processed data if preprocessing was requested. Note that these three files must be present in the `./CLI_examples` folder to interactively visualize the mapper graph (in particular with the same file names). 
---

### Full List of Parameters

Positional Arguments

* `input`: the data in csv format to run Mapper and / or to wrangle.

Flag Arguments

* `-i` or `--interval`: The intervals to use of the form START:END:STEP where start and end are inclusive.
* `-o` or `--overlap`: The overlaps to use of the form START:END:STEP where start and end are inclusive. These must be integers corresponding to percents, not floats.
* `-output`: Output directory. Defaults to `./graph/`
* `--no-preprocess`: Boolean flag to omit preprocessing. If used, no `wrangled_data.csv` will be produced.
* `--threads`: Number of threads to use when computing pairwise distances for clustering. -1 means uses all available processors.
* `--clusterer`: Required parameter to indicate which clustering method to use. Choices included dbscan, agglomerative, and meanshift.
* `--norm`: Normalization of points before computing the mapper graph. Possible choices include: None, 0-1, l1, l2, max. Defaults to None.
* `--gpu`: Boolean flag to indicate whether GPU acceleration should be used. Requires PyTorch and a CUDA compatible device. If the CUDA device runs out of memory, distance computation defaults to the CPU. **Note: Using a GPU might cause small numerical inaccuracies. Preliminary testing shows 5e-5 tolerance.** GPU Acceleration only available when using a euclidean metric.
* `--metric`: Metric to pass to DBSCAN. Any Scikit-learn metric. Defaults to euclidean.
* `--preprocess_only`: Boolean flag to only wrangle the data. No mapper graphs are computed.


Clustering Arguments as Flags


The same parameter naming convention is used from scikit learn (see documentation for [meanshift](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MeanShift.html), [dbscan] (https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html), and [agglomerative](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html)).

* `--eps`: epsilon for DBSCAN
* `--min_samples`: Min samples for DBSCAN
<!-- * `--linkage`: Linkage type for Agglomerative
* `--distance_threshold`: Distance threshold for stopping Agglomerative clustering -->
* `--bandwidth`: RBF kernel parameter for Mean Shift


----
### Original Datasets
The datasets used to generate the results presented in the paper are available at the following link:
https://drive.google.com/drive/folders/1grx1dcYGW--wzrxnrw0d6pwW3fbigWgg?usp=sharing 

----
### Bug Reporting

Please submit an issue with the exact command ran and full text of the error.
