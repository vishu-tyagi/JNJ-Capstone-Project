# JNJ-Capstone-Project

### Build the test container and run tests
```
make test
```

### Build the container
```
make build
```

### Fetch data
```
make fetch
```

## Setup to run jupyter notebooks

### Move into top-level directory
```
cd JNJ-Capstone-Project
```

### Install environment
```
conda env create -f environment.yml
```

### Activate environment
```
conda activate capstone
```

### Install package
```
pip install -e src/capstone
```
Including the optional -e flag will install the package in "editable" mode, meaning that instead of copying the files into your virtual environment, a symlink will be created to the files where they are.

You can now use the jupyter kernel to run notebooks.

## Develop locally

### Activate environment
```
conda activate capstone
```

### Fetch data
```
python -m capstone fetch
```
