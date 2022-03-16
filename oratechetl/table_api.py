from etlhelper

class TableGenericAPI():
    connection = None
    table_name = 'inv_item_categories'
    pk = 'category_id'
    dmltype = 'select'
    genseq = False
    datadict = {}
    def __init__(self, p_connection, p_table:str,
                 p_pk,p_dmltype:str ='select',
                 p_data:{}={},
                 p_genseq:bool = False):
        self.connection = p_connection
        self.table_name = p_table
        self.pk = p_pk
        self.dmltype = p_dmltype
        self.genseq = p_genseq
        sefl.data = p_data

    def test_connection(self):
        try:
            with self.connection as conn:
                re