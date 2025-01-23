# Participatory Multiverse

This repository holds the code for the simulation of the *multiverse analysis* conducted in the paper **Preventing Harmful Data Practices by using Participatory Input to Navigate the Machine Learning Multiverse** by Jan Simson, Fiona Draxler, Samuel Mehr and Christoph Kern.

The repository also contains the code for the interactive analysis of country-level data from the paper. The interactive analysis can be viewed at: [https://reliable-ai.github.io/participatory-multiverse/](https://reliable-ai.github.io/participatory-multiverse/). Its code is locateted in the directory [`interactive-analysis/`](./interactive-analysis).

This branch holds an updated version of the codebase, using newer versions of Python and respective packages. The original code used for the paper can be found on the `original` branch. The original Docker image used to run analyses can be found at [`ghcr.io/reliable-ai/participatory-multiverse:original-image`](https://github.com/reliable-ai/participatory-multiverse/pkgs/container/participatory-multiverse/341904979?tag=original-image).

The code, as well as parts of this `README` are based on and adapted from [https://github.com/reliable-ai/fairml-multiverse/](https://github.com/reliable-ai/fairml-multiverse/).

## Running the Code

### Setup

This project uses [uv](https://github.com/astral-sh/uv/) to control the Python environment to run the multiverse analysis. You will therefore first need to install `uv` by following the guidelines in the `uv` repository or running the following command:

```bash
pip install uv
```

### Running the Multiverse Analysis

The multiverse analysis itself is orchestrated via the [multiversum](https://github.com/jansim/multiversum/) package. You can run the complete multiverse analysis by running `uv run -m multiversum`. When running the command, `uv` will automatically create a virtual environment and install all necessary dependencies. The analysis will then be executed in this virtual environment.

To explore the individual analyses conducted in each *universe* of the *multiverse*, we recommend examining `universe.ipynb`. This notebook will be executed many times with different settings for each universe.

## Examining the Generated Data

The generated data from the different analyses is located in the `output` directory. Raw data from the different *universes* can be found under `output/runs/`.

## Important Concepts

In a multiverse analysis, we analyse the complete *multiverse* of plausible ML models. This *multiverse* is constructed by combining the plausible settings / options of multiple decisions one encounters during the design of an ML system. Each *universe* in this *multiverse*, corresponds to a unique combination of different decisions.

In our analysis we differentiate between "full" *universes*, which require refitting of the machine learnung model and *sub-universes* which can be evaluated without re-fitting the model. This distinction exists only for the sake of optimization, to save time when running the analysis. It is therefore completely optional to make use of sub-universes.

When specifying the dimensions of the *multiverse*, *sub-universes* are specified by passing in a list of lists (`[["a", "b"]]`) instead of a list (`["a", "b"]`). Each universe will receive a list of options / settings then instead of just a single option.

# Container Image 📦️

To make it easier to run the code and for the sake of long term reproducibility, we provide a container image that contains all the necessary dependencies. The container image is built using [Docker](https://www.docker.com/), using it with [Podman](https://podman.io/) is most likely also possible, but not yet tested.

### Running the Analysis

To run the multiverse analysis within our prebuilt container, you can run the following command:

```bash
# This will run the analysis with 16 cores and save the output to the output directory. The docker container will be deleted after the analysis is finished.
docker run --rm --cpus=16 -v $(pwd)/output:/app/output ghcr.io/reliable-ai/participatory-multiverse:latest
```

### Building

To build the container image, run the following command in the root directory of the project:

```bash
docker build -t participatory-multiverse .
```

To run the multiverse analysis within the container you built yourself, you can run the following command:

```bash
docker run --rm --cpus=10 -v $(pwd)/output:/app/output participatory-multiverse
```

## License

This work is licensed under the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/). Please note that the ACS PUMS data used in this work is not owned by the authors and may fall under a different license.
