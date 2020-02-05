from pix4dengine import create_project, login_seat
from pix4dengine.pipeline import Pipeline
from pix4dengine.constants.processing import ProcessingStep
from pix4dengine.exports import get_report

# Acquire the authorization to use Pix4Dengine from the Pix4D licensing system
login_seat("pix4d@unr.edu", "UNRua$2018")

# Create a project
project = create_project(proj_name='carson_valley_test',
                         image_dirs='home/theo/Pictures/carson_river_1',
                         work_dir='home/theo/Desktop/carson_valley_test')
# Calibrate the cameras in the project
pipeline = Pipeline(project, algos=("CALIB", "DEF_PROC_AREA", "DENSE", "ORTHO"))
pipeline.run()

# Access the calibration quality report
quality_report = get_report(project)
print(quality_report.calibration_quality_status())

