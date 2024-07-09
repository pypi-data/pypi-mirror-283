#!/bin/bash


export ENV_STATE=$1
export VERSION=$2

echo "ENV_STATE=$ENV_STATE"$'\n'"VERSION=$VERSION" > prismstudio/_common/.env

rm -rf dist
mkdir dist

source .env/bin/activate
python -m pip install -r requirements.txt

python setup.py sdist bdist_wheel --python-tag py310

deactivate


source .env9/bin/activate
python -m pip install -r requirements.txt

python setup.py sdist bdist_wheel --python-tag py39

deactivate


source .env8/bin/activate
python -m pip install -r requirements.txt

python setup.py sdist bdist_wheel --python-tag py38
deactivate


source .env11/bin/activate
python -m pip install -r requirements.txt

python setup.py sdist bdist_wheel --python-tag py311
deactivate


# token="pypi-AgEIcHlwaS5vcmcCJDZmZTQ4ZjQ3LWFkYjgtNGRiZS05MGY2LTFmZmYzNWYzYjRlZAACKlszLCI0MmU2MTAyNy04MGI2LTRmOTItOGQyNy1lODAyNjZhMzQxYjciXQAABiAHMwoRca7Gm6OwOjtNMtC4GrAfkrXMlhwGcR6L7D2JFw"
# twine upload dist/* -u __token__ -p $token

# sleep 10

# PS_FILES="/home/prism/miniconda3/envs/prism/conda-bld/linux-64/prismstudio-*"
# rm $PS_FILES
# conda activate prism
# conda build conda-receipe --no-test
# for f in $PS_FILES
# do
#     echo "Processing $f file..."
#     conda convert -f --platform all $f -o dist/
# done

# ARCH=( "win-64" "osx-arm64" "linux-aarch64" )
# for ar in "${ARCH[@]}"
# do
#     FILES="dist/$ar/*"
#     for f in $FILES
#     do
#         echo "Uploading $f ..."
#         anaconda upload $f
#     done
# done
