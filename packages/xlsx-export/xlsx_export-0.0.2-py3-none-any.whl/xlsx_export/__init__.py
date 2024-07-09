from testy.plugins.hooks import TestyPluginConfig, hookimpl
from django.urls import path
from . import views

class XlsxExportPluginConfig(TestyPluginConfig):
    package_name = 'xlsx_export'
    verbose_name = 'XLSX Export Plugin'
    description = 'Export data to XLSX format'
    version = '0.2'
    plugin_base_url = 'xlsx-export-plugin'
    index_reverse_name = 'index'
    urls_module = 'xlsx_export.urls'

@hookimpl
def config():
    return XlsxExportPluginConfig
