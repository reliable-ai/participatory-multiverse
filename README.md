# Participatory Multiverse Simulation

This is the original simulation code used to conduct analyses for the paper **Preventing Harmful Data Practices by using Participatory Input to Navigate the Machine Learning Multiverse** by Jan Simson, Fiona Draxler, Samuel Mehr and Christoph Kern.

Please refer to the updated README on the `main` branch for the latest information about the paper itself, as well as a more modern implementation of the simulation code.

The code, as well as parts of this `README` are based on and adapted from [https://github.com/reliable-ai/fairml-multiverse/](https://github.com/reliable-ai/fairml-multiverse/).

## Running the Code

### Setup

This project uses [Pipenv](https://pipenv.pypa.io/en/latest/) to control the Python environment. To install the dependencies, first install `pipenv` on your machine, then run `pipenv sync -d` in the root directory of the project. Once set up, you can enter the virtual environment in your command line by running `pipenv shell`.

### Running the Multiverse Analysis

You can run the complete multiverse analysis by running `python multiverse_analysis.py`. Make sure to activate the virtual environment beforehand, so that the installed dependencies are available. By default this will allow you to stop and restart the analysis between different universe runs.

To explore the individual analyses conducted in each *universe* of the *multiverse*, we recommend examining `universe_analysis.ipynb`. This notebook will be executed many times with different settings for each universe.

### Analysing the Results

The different Jupyter notebooks prefixed with `analysis` are analyzing the generated output from the multiverse analysis. To compute e.g. the different measures of variable importance, you can run the notebook [`analysis_var_imp_overall.ipynb`](./analysis_var_imp_overall.ipynb). The `analysis__setup.ipynb` is used for loading and preparing the multiverse analysis results and is called by the other notebooks internally. You may wish to change this notebook, though, to choose the correct `run` to analyze.

## Examining the Generated Data

The generated data from the different analyses is located in the `output` directory. Raw data from the different *universes* can be found under `output/runs/`, raw data from the analyses e.g. the FANOVAs can be found under `output/analyses/`.

# Adapting the Analysis

We purposefully created our analysis in a way that makes it easy to adapt for your own usecase(s). The steps do so are as follows:

1. Clone (or fork) this repository to have a copy of the codebase.
2. Follow the steps in the "Setup" section to install dependencies and create a virtual environment.
3. *Optional:* Delete files and results from the original analysis. You can safely delete the `data/`, `misc/`, `interactive-analysis/` and `output/` directories.
4. Modify the [`universe_analysis.ipynb`](./universe_analysis.ipynb) notebook to contain your analysis instead. All settings / options you may wish to modify as explicit decisions in the multiverse can be configured in the `universe` object.
   - We recommend verifying that your universe analysis script works correctly by trying out a few settings and running the script manually.
5. Once you are satisfied with your universe analysis, you can update the [`multiverse_analysis.py`](./multiverse_analysis.py) script to include all available options for the decisions you created in the `universe_analysis.ipynb`.
6. Execute the multiverse analysis script by running `python multiverse_analysis.py`. Make sure you are running your analysis inside the virtual environment created in step 2.

## Important Concepts

In a multiverse analysis, we analyse the complete *multiverse* of plausible ML models. This *multiverse* is constructed by combining the plausible settings / options of multiple decisions one encounters during the design of an ML system. Each *universe* in this *multiverse*, corresponds to a unique combination of different decisions.

In our analysis we differentiate between "full" *universes*, which require refitting of the machine learnung model and *sub-universes* which can be evaluated without re-fitting the model. This distinction exists only for the sake of optimization, to save time when running the analysis. It is therefore completely optional to make use of sub-universes.

When specifying the dimensions of the *multiverse*, *sub-universes* are specified by passing in a list of lists (`[["a", "b"]]`) instead of a list (`["a", "b"]`). Each universe will receive a list of options / settings then instead of just a single option.

# Container Image 📦️

To make it easier to run the code and for the sake of long term reproducibility, we provide a container image that contains all the necessary dependencies. The container image is built using [Docker](https://www.docker.com/), using it with [Podman](https://podman.io/) is most likely also possible, but not yet tested.

### Running the Analysis

To run the multiverse analysis within our prebuilt container, you can run the following command:

```bash
# Remove container after runnning
docker run --rm --cpus=5 -v $(pwd)/output:/app/output ghcr.io/reliable-ai/participatory-multiverse

# Restart up to 5 times if there are issues while running (happens sometimes when running in parallel)
docker run --restart on-failure:5 --cpus=15 --env MODE=continue -v $(pwd)/output:/app/output ghcr.io/reliable-ai/participatory-multiverse
```

Please note the cpus flag here, which may be necessary based on how powerful of a machine you use. When we first conducted the analysis on an 8 core machine we did not encounter any issues, but when running the analysis on a 32 core machine we encountered issues with a race condition leading to errors upon startup due to a [bug](https://github.com/nteract/papermill/issues/511) in the Jupyter client.

### Building

To build the container image, run the following command in the root directory of the project:

```bash
docker build -t participatory-multiverse .
```

To run the multiverse analysis within the container you built yourself, you can run the following command:

```bash
docker run --rm --cpus=5 -v $(pwd)/output:/app/output participatory-multiverse
```

## License

This work is licensed under the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). Please note that the ACS PUMS data used in this work is not owned by the authors and may fall under a different license.
