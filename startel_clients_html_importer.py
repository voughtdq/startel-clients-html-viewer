import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clients.settings')
django.setup()

from django.db.migrations.executor import MigrationExecutor
from django.db import connections, DEFAULT_DB_ALIAS

from agent.models import ClientPage
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

def is_database_synchronized(database):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    
    return not executor.migration_plan(targets)

class MigrationException(Exception):
    pass

class StartelClientsHTMLImporter:
    def __init__(self, report_path):
        self.report_path = report_path

    def start(self):
        self._raise_if_not_synchronized()

        updated_count = 0
        created_count = 0

        with open(self.report_path, 'r') as report:
            for block in report.read().split('<BR class=brk>'):
                client_id = self._get_client_id(block)
                try:
                    client_id = int(client_id)
                except ValueError:
                    logger.warning(f'Skipping non-integer {client_id}')
                    continue

                client, created = ClientPage.objects.update_or_create(client_id=client_id, data=block)

                if created:
                    created_count += 1
                    logger.info(f'Adding {client_id}')
                else:
                    updated_count += 1
                    logger.warning(f'Updating {client_id}')
        
        logger.info(f'''
        Import finished

        Updated:\t{updated_count}
        Created:\t{created_count}
        Total:\t\t{updated_count+created_count}
        ''')
                
    @staticmethod
    def _get_client_id(block):
        # first td in second tr of first tbody
        soup = BeautifulSoup(block, 'html5lib')
        client_id = soup.find('tbody').find_all('tr')[2].find('td').text

        return client_id
    
    @staticmethod
    def _raise_if_not_synchronized():
        if not is_database_synchronized(DEFAULT_DB_ALIAS):
            raise MigrationException('Database not migrated. Run `manage.py migrate` before importing.')

if __name__ == '__main__':
    try:
        report_path = sys.argv[1]
    except IndexError:
        sys.exit(f'Please provide a report path: `{sys.argv[0]} path/to/the/report.htm`')
    
    try:
        StartelClientsHTMLImporter(report_path).start()
    except MigrationException as e:
        sys.exit(e)