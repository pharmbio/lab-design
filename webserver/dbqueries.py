#!/usr/bin/env python3
import logging
import json
from typing import Tuple
import psycopg2
import psycopg2.extras
import settings as labdesign_settings
import csv
import io

def get_connection():

    return psycopg2.connect(host=labdesign_settings.DB_HOSTNAME,
                                 database=labdesign_settings.DB_NAME,
                                 user=labdesign_settings.DB_USER, password=labdesign_settings.DB_PASS)

def put_connection(connection):
    connection.close()




def list_all_plate_layout():

    logging.debug("list_all_plate_layout")

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT DISTINCT(layout_id) "
                 "FROM plate_layout "
                 "ORDER BY layout_id")

        logging.info("query" + str(query))

        cursor = conn.cursor()
        cursor.execute(query)

        resultlist = []

        for row in cursor:
            resultlist.append({'layout_id': row[0]})

        cursor.close()
        put_connection(conn)
        conn = None

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def list_plate_layout(layout_id):

    logging.debug("list_plate_layout(layout_id), " + str(layout_id))

    conn = None
    try:

        conn = get_connection()

        table_columns = ['layout_id',
                         'well_id',
                         'batch_id',
                         'solvent',
                         'stock_conc',
                         'stock_conc_unit',
                         'cmpd_vol',
                         'cmpd_vol_unit',
                         'well_vol',
                         'well_vol_unit',
                         'pert_type',
                         'cmpd_conc',
                         'cmpd_conc_unit',
                         'batchid',
                         'cbkid',
                         'libid',
                         'libtxt',
                         'smiles',
                         'inchi',
                         'inkey'
                        ]


        query = ("SELECT " + ",".join(table_columns) +
                 " FROM plate_layout_v1 "
                 " WHERE layout_id LIKE %s"
                 " ORDER BY well_id")

        logging.info("query" + str(query))

        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cursor.execute(query, (layout_id,))

        #logging.info("cursor.mogrify: " + str(cursor.mogrify(query, (layout_id,))))


        resultdict = cursor.fetchall()

        cursor.close()

        #logging.debug(json.dumps(resultdict, indent=2))

        return resultdict

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)


def list_plate(barcode):

    logging.debug("list_plate(barcode), " + str(barcode))

    conn = None
    try:

        conn = get_connection()




        query = ("SELECT * "
                 " FROM plate "
                 " WHERE barcode LIKE %s"
                 " ORDER BY barcode")

        logging.info("query" + str(query))

        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cursor.execute(query, (barcode,))

        #logging.info("cursor.mogrify: " + str(cursor.mogrify(query, (layout_id,))))


        resultdict = cursor.fetchall()

        cursor.close()

        #logging.debug(json.dumps(resultdict, indent=2))

        return resultdict

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def list_all_plates():

    logging.debug("list_all_plates")

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT barcode "
                 "FROM plate "
                 "ORDER BY barcode")

        logging.info("query" + query)

        cursor = conn.cursor()
        cursor.execute(query)

        resultlist = []

        for row in cursor:
            resultlist.append({'barcode': row[0]})

        cursor.close()
        put_connection(conn)
        conn = None

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)


def list_all_image_analyses_per_plate(project_filter: str = '%'):

    logging.info("project_filter:" + str(project_filter))

    columns = ['project',
               'plate_barcode',
               'plate_acq_name',
               'meta',
               'analysis_date',
               'analysis_error',
               'pipeline_name',
               'plate_acq_id',
               'analysis_id',
               'results'
               ]

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT " + ",".join(columns) + " "
                 " FROM image_analyses_per_plate "
                 " WHERE project LIKE %s"
                 " ORDER BY project, plate_barcode, plate_acq_name, meta, analysis_date")

        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cursor.execute(query, (project_filter,))
        executed_sql = cursor.mogrify(query, (project_filter,))
        logging.info("cursor._last_executed: " + executed_sql.decode("utf-8") )

        resultdict = cursor.fetchall()

        cursor.close()

        return resultdict

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)


def select_compounds():

    logging.debug("select_compounds")

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT * "
                 "FROM compound "
                 "LIMIT 100")

        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

        cursor.execute(query)

        resultdict = cursor.fetchall()

        cursor.close()

        return resultdict

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)


def list_all_projects():

    logging.debug("list_all_projects")

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT name "
                 "FROM project "
                 "ORDER BY name")

        logging.info("query" + str(query))

        cursor = conn.cursor()
        cursor.execute(query)

        resultlist = []

        for row in cursor:
            resultlist.append({'name': row[0]})

        cursor.close()
        put_connection(conn)
        conn = None

        #logging.debug(json.dumps(resultlist, indent=2))

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)


def list_all_experiments():

    logging.debug("inside list_all_experiments")

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT id, name "
                 "FROM experiment "
                 "ORDER BY name")

        logging.info("query" + str(query))

        cursor = conn.cursor()
        cursor.execute(query)

        resultlist = []

        for row in cursor:
            resultlist.append({'id': row[0]})
            resultlist.append({'name': row[1]})

        cursor.close()

        logging.debug(json.dumps(resultlist, indent=2))

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def list_experiments(project_name):

    logging.debug("list_experiments(project_name), " + str(project_name))

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT id, name "
                 "FROM experiment "
                 "WHERE project_name = %s"
                 "ORDER BY name")

        logging.info("query" + str(query))

        cursor = conn.cursor()
        cursor.execute(query, (project_name,))

        resultlist = []

        for row in cursor:
            resultlist.append({'id': row[0]})
            resultlist.append({'name': row[1]})

        cursor.close()

        logging.debug(json.dumps(resultlist, indent=2))

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def list_experiment(experiment_id):

    logging.debug("list_experiment(experiment_id), " + str(experiment_id))

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT id, name "
                 "FROM experiment "
                 "WHERE experiment_id = %s"
                 "ORDER BY name")

        logging.info("query" + str(query))

        cursor = conn.cursor()
        cursor.execute(query, (experiment_id,))

        resultlist = []

        for row in cursor:
            resultlist.append({'id': row[0]})
            resultlist.append({'name': row[1]})

        cursor.close()

        logging.debug(json.dumps(resultlist, indent=2))

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def list_protocols():

    logging.debug("list_protocols")

    conn = None
    try:

        conn = get_connection()

        query = ("SELECT name, steps "
                 "FROM protocols "
                 "ORDER BY name")

        logging.info("query" + str(query))

        cursor = conn.cursor()
        cursor.execute(query)

        resultlist = []

        for row in cursor:
            resultlist.append({'name': row[0],
                               'steps': row[1]
                               })

        cursor.close()

        logging.debug(json.dumps(resultlist, indent=2))

        return resultlist

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def import_table_data(table_name: str, table_data: str, delimiter: str = '\t') -> str:

    logging.debug("Inside import_plate_layout, plate_layout_file:" + table_data)

    allowed_tables = ['plate',
                      'plate_layout']
    if table_name not in allowed_tables:
        raise Exception(f"table_name: {table_name} not in list allowed_tables")


    conn = None
    try:

        # First just read the columns
        memory_file = io.StringIO(table_data)
        reader = csv.reader(memory_file, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        columns = next(reader)
        columns_delimited = ",".join(columns)

        # Build query
        query = ("INSERT INTO "+ table_name + "(" + columns_delimited + ")"
                 "VALUES %s ")

        logging.info("query" + str(query))

        conn = get_connection()
        cursor = conn.cursor()

        retval = cursor.copy_from(memory_file, table_name, sep=delimiter, null='')
        logging.debug("retval:" + str(retval))

        conn.commit()
        cursor.close()

        return "OK"

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)




def save_protocol(name, data):

    logging.debug("save_protocol")

    conn = None
    try:

        conn = get_connection()

        # Build query
        query = ("INSERT INTO protocols(name, steps)"
                 "VALUES (%s, %s)")
        logging.info("query" + str(query))

        # Add protocol steps into a json array
        #steps_array = data.splitlines()
        #json_array = [];
        #for stp in steps_array:
        #  json_array.append(json.loads(step))

        #logging.debug("data_json" + str(jsodatan_array))

        cursor = conn.cursor()
        retval = cursor.execute(query, (name, data))
        conn.commit()
        cursor.close()

        return "OK"

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def delete_protocol(name):

    logging.debug("delete_protocol")
    logging.debug("name" + str(name))

    conn = None
    try:

        conn = get_connection()

        # Build query
        query = ("DELETE FROM protocols WHERE name = %s")
        logging.info("query" + str(query))

        cursor = conn.cursor()
        retval = cursor.execute(query, (name,))
        conn.commit()
        cursor.close()

        return "OK"

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)


def select_labfile_description(path):

    conn = None
    try:

        query = ("SELECT description "
                 "FROM labfiles "
                 "WHERE path = %s")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (path,))
        description = cursor.fetchone()
        cursor.close()

        return description

    except (Exception, psycopg2.DatabaseError) as err:
        logging.exception("Message")
        raise err
    finally:
        if conn is not None:
            put_connection(conn)

def get_project(project_name):
    return None




