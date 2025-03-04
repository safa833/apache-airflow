FROM apache/airflow:2.10.5

USER root

# Install wget and other dependencies
RUN apt-get update && apt-get install -y wget bzip2

# Download Miniconda installation script
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /tmp/miniconda.sh

# Install Miniconda with bash explicitly
RUN bash /tmp/miniconda.sh -b -p /opt/miniconda

# Install GDAL using conda
RUN /opt/miniconda/bin/conda install -y -c conda-forge gdal=3.6.2

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Add Miniconda to PATH
ENV PATH="/opt/miniconda/bin:${PATH}"

# Switch back to the airflow user
USER airflow

# Add and install Python requirements
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt \
    && pip install GDAL==$(gdal-config --version)