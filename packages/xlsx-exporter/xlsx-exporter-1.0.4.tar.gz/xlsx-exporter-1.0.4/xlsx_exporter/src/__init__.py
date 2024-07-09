# src/__init__.py

# Импортируем необходимые модули из TestY
from testy.plugins.hooks import TestyPluginConfig, hookimpl

# Импорт моделей, представлений и форм из вашего плагина
from .views import upload_file, success_view
from .models import TestCase, TestSuite, TestCaseStep, Project
from .forms import UploadFileForm

# Конфигурация плагина для TestY
class ImportPluginConfig(TestyPluginConfig):
    package_name = 'xlsx-exporter'
    verbose_name = 'XLSX Exporter Plugin'
    description = 'Export test cases to XLSX format for TestY'
    version = '1.0.3'
    plugin_base_url = 'xlsx-exporter'
    author = 'Maxim Tuchkov'
    index_reverse_name = 'index'

    # Указываем URL-ы вашего плагина
    urls_module = 'src.urls'

# Регистрируем конфигурацию плагина
@hookimpl
def config():
    return ImportPluginConfig
