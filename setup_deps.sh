#!/bin/bash

VENV_NAME="venv_server_auto_utils"
DIR_NAME_EZ_START="ez_start"

echo "Creating virtual environment..."
python3.12 -m venv $VENV_NAME

echo "Activating virtual environment..."
source $VENV_NAME/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Deactivating virtual environment..."
deactivate

echo "Setting up permissions for python scripts..."
chmod +x scripts/*.py

echo "Creating easy-start bash scripts..."
mkdir -p $DIR_NAME_EZ_START

for file in scripts/*.py; do
    script_name=$(basename "$file" .py)
    echo -e "#!/bin/bash\n\ncd ../ && $VENV_NAME/bin/python3.12 scripts/$script_name.py \"\$@\"" > $DIR_NAME_EZ_START/"$script_name".sh
    chmod +x $DIR_NAME_EZ_START/"$script_name".sh
done

echo "Setup complete!"
