FROM quay.io/jupyter/base-notebook:2024-04-29
USER root

# Update package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    gcc \
    graphviz \
    graphviz-dev \
    build-essential \
    neovim \
    vim \
    tmux \
    fzf \
    && rm -rf /var/lib/apt/lists/*


ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"
ARG HOME="/home/${NB_USER}"
# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

RUN pip install --upgrade jupyterlab-vim

# Clone the repository and install requirements
# RUN git clone https://github.com/uds-se/fuzzingbook.git --depth 1 \
#     && cd fuzzingbook \
#     && pip install -r requirements.txt

WORKDIR "${HOME}"

