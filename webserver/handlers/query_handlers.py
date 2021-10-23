#!/usr/bin/env python3
"""
This is where most of the logic goes.
"""
import json
import logging

import tornado.web
from dbqueries import (list_protocols, save_protocol, delete_protocol, list_all_projects, select_labfile_description,
                       list_all_experiments, list_experiments, list_experiment)
from fileutils import list_projectfiles

class DeleteProtocolQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, protocol):
        """Handles GET requests.
        """
        logging.info("plate_name: " + str(protocol))

        result = delete_protocol(protocol)

        logging.debug(result)
        self.finish({'result':result})


class SaveProtocolQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method
    """
    The query handler handles form posts and returns list of results
    """
    def post(self):
        """Handles POST requests.
        """
        
        # log all input parameters
        logging.debug("%r %s" % (self.request, self.request.body.decode()))

        protocol_steps = self.get_argument("plate-protocol-steps")
        new_name = self.get_argument("new_name")
        
        #logging.debug("form_data:" + str(form_data))

        results = save_protocol(new_name, protocol_steps)
        logging.debug(results)
        self.finish({'results':results})


class ListProtocolsQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, protocol):
        """Handles GET requests.
        """
        logging.info("plate_name: " + str(protocol))

        result = list_protocols()

        logging.debug(result)
        self.finish({'result':result})


class ListAllProjectsQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        """Handles GET requests.
        """

        result = list_all_projects()

        logging.debug(result)
        self.finish({'result':result})

class ListProjectfilesHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, project_name):
        """Handles GET requests.
        """
        logging.info("inside ListProjectfilesHandler")

        projfiles = list_projectfiles(project_name)

        logging.debug("projfiles:" + str(projfiles))

        # return as list of list with first row as headers
        result = []
        result.append(["path", "description"])

        # Add description from db to each file
        for path in projfiles:
            logging.debug(path)
            description = select_labfile_description(str(path))
            result.append([str(path), description])

        logging.debug(result)
        self.finish({'result':result})

class ListExperimentfilesHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, experiment_id):
        """Handles GET requests.
        """
        logging.info("inside ListExperimentfilesHandler")

        result = fileutils.list_experimentfiles(experiment_id)

        logging.debug(result)
        self.finish({'result':result})


class ListAllExperimentsQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        """Handles GET requests.
        """

        logging.info("inside ListAllExperimentsQueryHandler")

        result = list_all_experiments()

        logging.debug(result)
        self.finish({'result':result})


class ListExperimentsQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, project_name):
        """Handles GET requests.
        """

        logging.info("inside ListExperimentsQueryHandler, project_name=" + str(project_name))

        result = list_experiments(project_name)

        logging.debug(result)
        self.finish({'result':result})

class ListExperimentQueryHandler(tornado.web.RequestHandler): # pylint: disable=abstract-method

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, experiment_id):
        """Handles GET requests.
        """

        logging.info("inside ListExperimentQueryHandler, experiment_id=" + str(experiment_id))

        result = list_experiment(experiment_id)

        logging.debug(result)
        self.finish({'result':result})


