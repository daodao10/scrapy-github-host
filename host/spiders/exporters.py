from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

class HostItem_CsvExporter(CsvItemExporter):
    def __init__(self, file, include_headers_line=False, join_multivalued=', ', **kwargs):
        delimiter = settings.get('CSV_DELIMITER', '  ')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export

        super(HostItem_CsvExporter, self).__init__(file, include_headers_line, join_multivalued, **kwargs)

