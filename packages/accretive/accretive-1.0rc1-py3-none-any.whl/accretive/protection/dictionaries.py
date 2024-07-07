# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Protected accretive dictionaries. '''


from .. import __
from .. import dictionaries as _dictionaries
from . import classes as _classes


class Dictionary(
    _dictionaries.Dictionary,
    metaclass = _classes.Class,
    docstring = __.generate_docstring(
        _dictionaries.Dictionary, 'protection of class' )
):
    ''' Accretive dictionary. '''


class ProducerDictionary(
    _dictionaries.ProducerDictionary,
    metaclass = _classes.Class,
    docstring = __.generate_docstring(
        _dictionaries.ProducerDictionary, 'protection of class' )
):
    ''' Accretive dictionary with default values for missing entries. '''


__all__ = __.discover_public_attributes( globals( ) )
