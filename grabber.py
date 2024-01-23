import os
import argparse
import logging

from chartConfig import ChartConfig
from downloadChart import ChartDetails, Chart

# Setup the loggegr
FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT, level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

# Grab the configuration from config file
chartsConfig = ChartConfig('charts.ini')  # creating object of HostConfig
chartsConfig.readConfig()                 # Reading config file 
charts = chartsConfig.getCharts()         # Getting the list of sections (servers)
print("Charts: ", charts)

# Processing starts .....
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

for chartname in charts:
  chart = Chart( chartsConfig.getChart(chartname, "repoUrl"),
                 chartsConfig.getChart(chartname, "repoName"),
                 chartsConfig.getChart(chartname, "chartName"),
                 chartsConfig.getChart(chartname, "chartVersion")
                )
  chart.download()
  chart.process()
  chart.cleanup()
  
os.chdir(curr_dir)