# MIT License

# Copyright (c) 2018 shotariya

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

bl_info = {
    'name': "Shotariya's Material Combiner",
    'description': 'Public Release Material Combiner 2',
    'author': 'shotariya + Urmom',
    'version': (0, 0, 3),
    'blender': (4, 2, 0),
    'location': 'View3D',
    'wiki_url': 'https://github.com/Grim-es/material-combiner-addon',
    'tracker_url': 'https://github.com/Grim-es/material-combiner-addon/issues',
    'category': 'Object'
}

from .registration import register_all
from .registration import unregister_all


def register() -> None:
    print('Loading Material Combiner..')
    register_all(bl_info)


def unregister() -> None:
    unregister_all()
