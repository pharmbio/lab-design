#!/usr/bin/env python3
"""
This is where most of the logic goes.
"""
import json
import logging

import tornado.web
import dbqueries
import fileutils

class DeleteProtocolQueryHandler(tornado.web.RequestHandler):

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, protocol):
        """Handles GET requests.
        """
        logging.info("plate_name: " + str(protocol))

        result = dbqueries.delete_protocol(protocol)

        logging.debug(result)
        self.finish({'result':result})


class ImportTableRowsQueryHandler(tornado.web.RequestHandler):
    """
    The query handler handles form posts and returns list of results
    """
    def post(self):
        """Handles POST requests.
        """

        # log all input parameters
        logging.debug("%r %s" % (self.request, self.request.body.decode()))

        table_name = self.get_argument("table_name")
        file_body = self.request.files['new_table_rows_file'][0]['body']
        body_as_string = str(file_body, encoding='utf-8')

        results = dbqueries.import_table_data(table_name, body_as_string)
        logging.debug(results)
        self.finish({'results':results})


class SaveProtocolQueryHandler(tornado.web.RequestHandler):
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

        results = dbqueries.save_protocol(new_name, protocol_steps)
        logging.debug(results)
        self.finish({'results':results})


class ListProtocolsQueryHandler(tornado.web.RequestHandler):
    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, protocol):
        """Handles GET requests.
        """
        logging.info("plate_name: " + str(protocol))

        result = dbqueries.list_protocols()

        logging.debug(result)
        self.finish({'result':result})


class ListAllProjectsQueryHandler(tornado.web.RequestHandler):

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        """Handles GET requests.
        """

        result = dbqueries.list_all_projects()

        logging.debug(result)
        self.finish({'result':result})

class ListProjectfilesHandler(tornado.web.RequestHandler):

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, project_name):
        """Handles GET requests.
        """
        logging.info("inside ListProjectfilesHandler")

        projfiles = fileutils.list_projectfiles(project_name)

        logging.debug("projfiles:" + str(projfiles))

        # return as list of list with first row as headers
        result = []
        result.append(["path", "description"])

        # Add description from db to each file
        for path in projfiles:
            logging.debug(path)
            description = dbqueries.select_labfile_description(str(path))
            result.append([str(path), description])

        logging.debug(result)
        self.finish({'result':result})

class ListExperimentfilesHandler(tornado.web.RequestHandler):

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


class ListAllExperimentsQueryHandler(tornado.web.RequestHandler):

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self):
        """Handles GET requests.
        """

        logging.info("inside ListAllExperimentsQueryHandler")

        result = dbqueries.list_all_experiments()

        logging.debug(result)
        self.finish({'result':result})


class ListExperimentsQueryHandler(tornado.web.RequestHandler):

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, project_name):
        """Handles GET requests.
        """

        logging.info("inside ListExperimentsQueryHandler, project_name=" + str(project_name))

        result = dbqueries.list_experiments(project_name)

        logging.debug(result)
        self.finish({'result':result})

class ListExperimentQueryHandler(tornado.web.RequestHandler):

    def prepare(self):
        header = "Content-Type"
        body = "application/json"
        self.set_header(header, body)

    def get(self, experiment_id):
        """Handles GET requests.
        """

        logging.info("inside ListExperimentQueryHandler, experiment_id=" + str(experiment_id))

        result = dbqueries.list_experiment(experiment_id)

        logging.debug(result)
        self.finish({'result':result})


