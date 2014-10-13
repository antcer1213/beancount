"""Write output files for the tutorial commands.
"""
import argparse
import logging
import subprocess
import os
from os import path


COMMANDS = [
    ('balances'                 , "bean-query {} balances"),
    ('help-reports'             , "bean-query --help-reports"),
    ('help-subcmd'              , "bean-query {} balances --help"),
    ('help-global'              , "bean-query --help"),
    ('help-formats'             , "bean-query --help-formats"),
    ('balances-restrict'        , "bean-query {} balances -e ETrade"),
    ('balances-restrict-cost'   , "bean-query {} balances -e ETrade -c"),
    ('balances-tree'            , "bean-query {} balances | treeify"),
    ('balsheet'                 , "bean-query {} balsheet"),
    ('journal'                  , "bean-query {} journal -w 120 -a Assets:US:BofA:Checking"),
    ('journal-with-balance'     , "bean-query {} journal -w 120 -a Assets:US:BofA:Checking -b"),
    ('invest'                   , "bean-query {} journal -w 120 -a Assets:US:ETrade:GLD -b"),
    ('invest-with-cost'         , "bean-query {} journal -w 120 -a Assets:US:ETrade:GLD -b -c"),
    ('journal-unrestricted'     , "bean-query {} journal -w 120 -b"),
    ('holdings'                 , "bean-query {} holdings"),
    ('holdings-by-account'      , "bean-query {} holdings --by account"),
    ('holdings-by-root-account' , "bean-query {} holdings --by root-account"),
    ('holdings-by-commodity'    , "bean-query {} holdings --by commodity"),
    ('holdings-by-currency'     , "bean-query {} holdings --by currency"),
    ('networth'                 , "bean-query {} networth"),
    ('accounts'                 , "bean-query {} accounts"),
    ('events'                   , "bean-query {} events"),
    ('stats-directives'         , "bean-query {} stats-directives"),
    ('stats-postings'           , "bean-query {} stats-postings"),
    ('holdings-csv'             , "bean-query -f csv {} holdings"),
    ]


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s: %(message)s')
    parser = argparse.ArgumentParser(__doc__.strip())
    parser.add_argument('filename', help='Beancount filename')
    parser.add_argument('output_directory', help='Output directory for the tutorial files')
    args = parser.parse_args()

    for report_name, command_template in COMMANDS:
        logging.info('Generating %s: %s', report_name, command_template)
        output_filename = path.join(args.output_directory, '{}.output'.format(report_name))
        errors_filename = path.join(args.output_directory, '{}.errors'.format(report_name))
        with open(output_filename, 'w') as output_file:
            with open(errors_filename, 'w') as errors_file:
                command = command_template.format(args.filename)
                pipe = subprocess.Popen(command, shell=True,
                                        stdout=output_file,
                                        stderr=errors_file)
                pipe.communicate()
                assert pipe.returncode == 0, pipe.returncode

        if path.getsize(errors_filename) == 0:
            os.remove(errors_filename)


if __name__ == '__main__':
    main()
