import logging
import os
import pathlib


def list_projectfiles(project_name):

    # TODO parameterize
    return list_files("/share/data/labdb/projects/" + str(project_name))

def list_experimentfiles(experiment_id):

    # TODO parameterize
    return list_files("/share/data/labdb/experiments/")

def list_files(input_path):

    logging.debug("input_path:" + str(input_path))

    files = list(pathlib.Path(input_path).rglob("*.*"))

    logging.debug("files:" + str(files))

    return files

# def list_files(input_path):
# 
#     logging.debug("input_path:" + str(input_path))
# 
#     files = list(pathlib.Path(input_path).rglob("*.*"))
# 
#     logging.debug("files:" + str(files))
# 
#     # create a table of the files with only one column and one file per row (each row is represented as a list)
#     result_table = []
# 
#     # Then add the files
#     for file in files:
#         relative_file = file.relative_to(input_path)
#         result_table.append( {"path": str(relative_file)} )
# 
#     #logging.debug("result_table:" + str(result_table))
# 
#     return result_table
