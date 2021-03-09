# Dremio Query Analyzer - VDS Creator
This tool will automatically create the Space, Folders and VDSs required to analyse queries.json files.

## Usage
On the command line, navigate to /path_to_dremio-query-analyzer/scripts/vdscreator.

Open run_vdscreator.sh in a text editor and ensure the following parameters are configured correctly at the top of the script:
dremio_url - Dremio UI URL for where the VDS definitions will be created e.g. http://localhost:9047
user_name - username of a Dremio user capable of creating VDSs
pwd - password of the user

Save the file.

Execute the following command:

./run_vdscreator.sh
