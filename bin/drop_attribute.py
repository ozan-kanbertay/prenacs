#!/usr/bin/env python3

#
# (c) 2021-2022 Giorgio Gonnella, University of Goettingen, Germany
#

"""
Drop an attribute definition record and attribute columns in the
attribute_value tables.

Usage:
  drop_attribute.py [options] {db_args_usage} <name>

Arguments:
{db_args}
  <name>       name of the attribute

Options:
{common}
"""
from schema import And, Or
from sqlalchemy import create_engine
import snacli
from attrtables import AttributeValueTables
from provbatch import scripts_helpers,\
                      AttributeDefinitionsManager,\
                      AttributeDefinition

def main(args):
  engine = create_engine(scripts_helpers.database.connection_string_from(args),
                         echo=args["--verbose"],
                         future=True)
  with engine.connect() as connection:
    with connection.begin():
      avt = AttributeValueTables(connection,
                                 attrdef_class=AttributeDefinition,
                                 tablename_prefix="_".join(\
                                     args["--dbpfx"], "attribute_value_t"))
      adm = AttributeDefinitionsManager(avt, connection)
      adm.drop(args["<name>"])

def validated(args):
  return scripts_helpers.validate(args, scripts_helpers.database.ARGS_SCHEMA,
      {"<name>": And(str, len),
       "--testmode":   Or(None, True, False)})

with snacli.args(scripts_helpers.database.SNAKE_ARGS,
                 input=["<name>"],
                 params=["--verbose"],
                 docvars={"common": scripts_helpers.common.ARGS_DOC,
                          "db_args": scripts_helpers.database.ARGS_DOC,
                          "db_args_usage": scripts_helpers.database.ARGS_USAGE},
                 version="1.0") as args:
  if args: main(validated(args))
