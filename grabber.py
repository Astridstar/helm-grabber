import os
import argparse
import logging

# Setup the loggegr
FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT, level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

# Setup the command line options
parser = argparse.ArgumentParser()
parser.add_argument('--repoName', type=str, help='Repository Name')
parser.add_argument('--repoUrl', type=str, help='URL to the helm repository')
parser.add_argument('--chart', type=str, help='Name of the chart to grab')
parser.add_argument('--version', type=str, help='Version of the chart to retrieve')

# Parse the commands
try:
    args = parser.parse_args()
except argparse.ArgumentError as e:
    logger.warning('%s', e) 
    
print(f"Parsing inputs:")
print(f"  REPO_NAME [{args.repoName}] ")
print(f"  URL       [{args.repoUrl}] ")
print(f"  Chart     [{args.chart}] ")
print(f"  Version   [{args.version}] ")
print("")
print("")

path = "charts-temp-directory"
curr_dir= os.getcwd()

# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:
  # Create a new directory because it does not exist
  os.makedirs(path)
  logger.info("The new directory %s is created!", path)
else:
  os.renames(path, f"{path}" + "_bak")
  logger.info("The old directory %s has been renamed", path)
  os.makedirs(path)

# Change the working directory to the newly created one  
os.chdir(path)

# Add the helm repo first    
logger.info(f"Adding repo {args.repoName} to local")
os.system(f"helm repo add {args.repoName} {args.repoUrl}")
os.system("helm repo update")

logger.debug("Pulling %s now\n", {args.chart})
os.system(f"helm pull {args.repoName}/{args.chart}")

# TODO: Change any container images 

# TODO: Replace the URL

# Clean up
os.system(f"helm repo remove {args.repoName}")
os.chdir(curr_dir)