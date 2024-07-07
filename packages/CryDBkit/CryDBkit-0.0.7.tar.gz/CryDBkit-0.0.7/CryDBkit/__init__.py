import datetime
import pkg_resources
import importlib.util
import sys
import os


__description__ = 'ToolKit for CryDB'
__email__ = 'binjacobcao@gmail.com'

now = datetime.datetime.now()
formatted_date_time = now.strftime('%Y-%m-%d %H:%M:%S')
print('CryDB, Bin CAO, HKUST.GZ' )
print('Executed on :',formatted_date_time, ' | Have a great day.')  
print('='*80)




compiled_module_path = os.path.join(
    pkg_resources.get_distribution('CryDBkit').location,
    'CryDBkit/__pycache__/website.cpython-39.pyc'
)


# Load the module
spec = importlib.util.spec_from_file_location("CryDBkit.website", compiled_module_path)
website = importlib.util.module_from_spec(spec)
sys.modules["CryDBkit.website"] = website
spec.loader.exec_module(website)