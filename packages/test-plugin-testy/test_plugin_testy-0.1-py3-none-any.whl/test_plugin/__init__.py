from testy.plugins.hooks import TestyPluginConfig, hookimpl

class TestPluginConfig(TestyPluginConfig):
    package_name = 'test_plugin'
    verbose_name = 'Test Plugin'
    description = 'Plugin for uploading files'
    version = '0.1'
    plugin_base_url = 'test_plugin'
    index_reverse_name = 'upload-file-form'
    urls_module = 'test_plugin.urls'

@hookimpl
def config():
    return TestPluginConfig
