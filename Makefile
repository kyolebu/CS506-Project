ENV_NAME=myenv

# Create the conda environment
setup:
	conda env create -f environment.yml

# Run all analysis scripts
run:
	conda run -n $(ENV_NAME) python ./analysis/roster/roster.py
	conda run -n $(ENV_NAME) python ./analysis/roster/roster2.py
	conda run -n $(ENV_NAME) python ./analysis/roster/decision_tree.py

# Remove the conda environment
clean:
	conda env remove -n $(ENV_NAME)
