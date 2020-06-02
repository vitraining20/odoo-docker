from psycopg2 import IntegrityError
from odoo.tests.common import SavepointCase
from odoo.tools.misc import mute_logger


class TestRequestConstraints(SavepointCase):
    """Test request constraints
    """

    @mute_logger('odoo.sql_db')
    def test_20_request_type_name_uniq(self):
        Model = self.env['request.type']

        # Test name uniq constraint
        data1 = dict(code='TEST-CODE-1', name='Test Type Name 42')
        data2 = dict(code='TEST-CODE-2', name='Test Type Name 42')

        Model.create(dict(data1))
        with self.assertRaises(IntegrityError):
            Model.create(dict(data2))

    @mute_logger('odoo.sql_db')
    def test_30_request_type_code_uniq(self):
        Model = self.env['request.type']

        # Test code uniq constraints
        data1 = dict(code='TEST-CODE-4', name='Test Type Name 44')
        data2 = dict(code='TEST-CODE-4', name='Test Type Name 45')

        Model.create(dict(data1))
        with self.assertRaises(IntegrityError):
            Model.create(dict(data2))

    @mute_logger('odoo.sql_db')
    def test_40_request_type_code_ascii(self):
        Model = self.env['request.type']

        # Test code uniq constraints
        data1 = dict(code='TEST-CODE-4', name='Test Type Name 44')
        data2 = dict(code='Тестовий-код-5', name='Test Type Name 45')

        Model.create(dict(data1))
        with self.assertRaises(IntegrityError):
            Model.create(dict(data2))
