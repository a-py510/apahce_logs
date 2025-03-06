Background

The criticalmention/interview-apache-logs repository was cloned, the code is written in the codespace reimagined fortnight, install the extension for python (run [python --version] to confirm)

The Steps to Run the file 

1. Clone the repository 
git clone https://github.com/a-py510/apahce_logs

2. Run the generate-logs.py script to create the website access log list in the Evaludation folder

cd scripts (Change the directory to scripts)

 ./generate-logs.py -f ../Evaluation/1.log --aggressive (Run the log generator to make a file 1.log in the Evaluation folder)

 3. Run the python script to output the statistical data for the website access logs

 git init . (Reinitialize the repository)

 cd .. & cd Evaludation (Change the directory to Evaluation where the log file while and code is)

 python eval.py (To run the python script) (The output file 1_web_output.log would be generated, change the log_filename file if want to test it for a different file, change the output_filename as well)
