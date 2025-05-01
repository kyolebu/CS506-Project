ENV_NAME=myenv

# Create the conda environment
setup:
	conda env create -f environment.yml

# Run all analysis scripts
run:
	conda run -n $(ENV_NAME) python ./analysis/roster/roster.py
	conda run -n $(ENV_NAME) python ./analysis/roster/roster2.py
	conda run -n $(ENV_NAME) python ./analysis/roster/decision_tree.py
	
	conda run -n $(ENV_NAME) python ./analysis/earnings/earnings_bpd_breakdown.py
	conda run -n $(ENV_NAME) python ./analysis/earnings/earnings_intradepartment_ot_gross.py
	conda run -n $(ENV_NAME) python ./analysis/earnings/earnings_intradepartment.py

	conda run -n $(ENV_NAME) python ./analysis/overtime/linear-regression-per-employee.py
	conda run -n $(ENV_NAME) python ./analysis/overtime/linear-regression.py
	conda run -n $(ENV_NAME) python ./analysis/overtime/pdf.py
	conda run -n $(ENV_NAME) python ./analysis/overtime/random-forest-regressor.py
	conda run -n $(ENV_NAME) python ./analysis/overtime/overtime-ratio.py

# Run tests to make sure figures were created
test:
	conda run -n $(ENV_NAME) python tests.py

# Remove the conda environment
clean:
	conda env remove -n $(ENV_NAME)
