#!/usr/bin/env python3
"""
Simple Tornado server.
"""

import os
import logging
import tornado
import tornado.web
import html_snipps as html_snipps


from handlers import query_handlers

import dbqueries

import settings as labdesign_settings

SETTINGS = {
    'debug': True,
    'develop': True,
    'template_path':'templates/',
    'xsrf_cookies': False, # Anders disabled this - TODO enable again....maybe...
    'cookie_secret':'some-really-secret-secret',
    # static path is defined in handler below
}

class ProjectTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application
    """
    def get(self):

        logging.info("inside ProjectTemplateHandler")

        project_name = self.get_arguments("project_name")

        logging.debug("project_name=" + str(project_name))

        projects = dbqueries.list_all_projects()

        logging.debug("projects:" + str(projects))

        project = dbqueries.get_project(project_name)

        logging.debug(self.request.path)

        self.render(self.request.path.strip('/'), page_name=self.request.path.strip('/'),
                                                  adminer_url=labdesign_settings.ADMINER_URL,
                                                  projects=projects,
                                                  project=project,
                                                  debug=logging.debug)

class PlateLayoutTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application
    """
    def get(self):
        logging.info("inside PlateLayoutTemplateHandler")

        plate_layouts = dbqueries.list_all_plate_layout()

        selected_layout_list = self.get_arguments("layout-select")
        logging.info("selected_layout_list:" + str(selected_layout_list))

        # get first item in options list
        if selected_layout_list:
            selected_layout_id = selected_layout_list[0]
        # set first as selected by default
        else:
            selected_layout_id = ""
            # if plate_layouts:
            #     first_row = plate_layouts[0]
            #     selected_layout_id = first_row['layout_id']


        logging.debug("selected_layout_id" + str(selected_layout_id))


        layout_dictrows = dbqueries.list_plate_layout(selected_layout_id)

        visualPlateLayout = html_snipps.drawVisualPlateLayout(layout_dictrows)
        plateLayoutTable = html_snipps.drawPlateLayoutTable(layout_dictrows)
        layout_select_options = html_snipps.drawLayoutSelect(plate_layouts, selected_layout_id)

        self.render(self.request.path.strip('/'), page_name=self.request.path.strip('/'),
                                                  adminer_url=labdesign_settings.ADMINER_URL,
                                                  layout_select_options=layout_select_options,
                                                  visualPlateLayout=visualPlateLayout,
                                                  plateLayoutTable=plateLayoutTable,
                                                  debug=logging.debug)

class PlateTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application
    """
    def get(self):
        logging.info("inside PlateTemplateHandler")

        plates = dbqueries.list_all_plates()

        selected_plates_list = self.get_arguments("plate-select")
        logging.info("selected_plates_list:" + str(selected_plates_list))

        # get first item in options list
        if selected_plates_list:
            selected_plate_id = selected_plates_list[0]
        # set first as selected by default
        else:
            selected_plate_id = ""


        logging.debug("selected_plate_id" + str(selected_plate_id))


        plate_dictrows = dbqueries.list_plate(selected_plate_id)

        plateTable = html_snipps.drawPlateTable(plate_dictrows)
        plate_select_options = html_snipps.drawPlateSelect(plates, selected_plate_id)

        self.render(self.request.path.strip('/'), page_name=self.request.path.strip('/'),
                                                  adminer_url=labdesign_settings.ADMINER_URL,
                                                  plate_select_options=plate_select_options,
                                                  plateTable=plateTable,
                                                  debug=logging.debug)

class ImageAnalysesTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application
    """
    def get(self):
        logging.info("inside ImageAnalysesTemplateHandler")

        project_filter_list = self.get_arguments("project-select")

        # get first item in options list
        if project_filter_list:
            project_filter = project_filter_list[0]
        # set all as selected by default
        else:
            project_filter = "All"

        tablerows = dbqueries.list_all_image_analyses_per_plate(project_filter)

        imgAnalysesTable = html_snipps.drawImageAnalysesPerPlateTable(tablerows)

        project_select_options = html_snipps.drawProjectSelect(project_filter)

        self.render(self.request.path.strip('/'), page_name=self.request.path.strip('/'),
                                                  adminer_url=labdesign_settings.ADMINER_URL,
                                                  imgAnalysesTable=imgAnalysesTable,
                                                  project_select_options=project_select_options,
                                                  debug=logging.debug)


class CompoundsTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application
    """
    def get(self):
        logging.info("inside CompoundsTemplateHandler")

        tablerows = dbqueries.select_compounds()

        compounds_table = html_snipps.drawTable(tablerows)

        logging.info("compounds_table" + compounds_table)

        self.render(self.request.path.strip('/'), page_name=self.request.path.strip('/'),
                                                  adminer_url=labdesign_settings.ADMINER_URL,
                                                  compounds_table=compounds_table,
                                                  debug=logging.debug)



class DefaultTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application
    """
    def get(self):

        logging.debug(self.request.path)

        self.render(self.request.path.strip('/'), page_name=self.request.path.strip('/'), adminer_url=labdesign_settings.ADMINER_URL)


class IndexTemplateHandler(tornado.web.RequestHandler): #pylint: disable=abstract-method
    """
    This is the main handler of the application, which serves the index.html template
    """
    def get(self):

        self.redirect('/project.html')


ROUTES = [
          (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static')}),
          (r'/files/(.*)', tornado.web.StaticFileHandler, {'path': '/share/data/labdb/'}),
          (r'/api/list/projects/all', query_handlers.ListAllProjectsQueryHandler),
          (r'/api/list/projectfiles/(?P<project_name>.+)', query_handlers.ListProjectfilesHandler),
          (r'/api/list/experiments/all', query_handlers.ListAllExperimentsQueryHandler),
          (r'/api/list/experiments/(?P<project_name>.+)', query_handlers.ListExperimentsQueryHandler),
          (r'/api/list/experiment/(?P<experiment_id>.+)', query_handlers.ListExperimentQueryHandler),
          (r'/api/protocols/(?P<protocol>.+)', query_handlers.ListProtocolsQueryHandler),
          (r'/api/protocol/save', query_handlers.SaveProtocolQueryHandler),
          (r'/api/table_rows/import', query_handlers.ImportTableRowsQueryHandler),
          (r'/api/protocol/delete/(?P<protocol>.+)', query_handlers.DeleteProtocolQueryHandler),
          (r'/project.html', ProjectTemplateHandler),
          (r'/protocols.html', DefaultTemplateHandler),
          (r'/platelayout.html', PlateLayoutTemplateHandler),
          (r'/well.html', DefaultTemplateHandler),
          (r'/compound.html', CompoundsTemplateHandler),
          (r'/experiment.html', DefaultTemplateHandler),
          (r'/plate.html', PlateTemplateHandler),
          (r'/imageanalyses.html', ImageAnalysesTemplateHandler),
          (r'/index.html', IndexTemplateHandler),
          (r'/', IndexTemplateHandler),
         ]

if __name__ == '__main__':

    tornado.log.enable_pretty_logging()

    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.getLogger().setLevel(logging.DEBUG)

    APP = tornado.web.Application(ROUTES, **SETTINGS)
    APP.listen(8080)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logging.info("Shutting down")
