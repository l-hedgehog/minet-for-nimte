from distutils.core import setup
import py2exe

setup(
  name = 'minet-gui',
  description = 'MINET',
  version = '0.1',

  windows = [
              {
                'script': 'minet-gui.pyw',
                'icon_resources': [(1, 'pics/minet.ico')],
              }
            ],

  options = {
              'py2exe': {
                'packages': 'encodings',
                'includes': 'cairo, pango, atk, pangocairo, gobject',
                'bundle_files': 1,
              }
            },

  data_files=[],
  
  zipfile=None
)