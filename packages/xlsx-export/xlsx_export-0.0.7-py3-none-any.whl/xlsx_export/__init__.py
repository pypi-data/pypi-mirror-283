from testy.plugins.hooks import TestyPluginConfig, hookimpl

class XlsxExportPluginConfig(TestyPluginConfig):
    package_name = 'xlsx_export'
    verbose_name = 'XLSX Export Plugin'
    description = 'Export data to XLSX format'
    version = '0.7'
    plugin_base_url = 'xlsx_export'
    index_reverse_name = 'index'
    urls_module = 'xlsx_export.urls'
    author = 'Maxim Tuchkov'


@hookimpl
def config():
    return XlsxExportPluginConfig
