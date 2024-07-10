from testy.plugins.hooks import TestyPluginConfig, hookimpl

class XlsxExportPluginConfig(TestyPluginConfig):
    package_name = 'xlsx_export'
    verbose_name = 'XLSX Export Plugin'
    description = 'Export data to XLSX format'
    version = '0.10'
    plugin_base_url = 'xlsx_export/upload'
    index_reverse_name = 'upload'
    urls_module = 'xlsx_export.urls'
    author = 'Maxim Tuchkov'


@hookimpl
def config():
    return XlsxExportPluginConfig
