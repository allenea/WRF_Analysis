"""Copyright (C) 2018-Present E. Allen, D. Veron - University of Delaware"""
#
# You may use, distribute and modify this code under the
# terms of the GNU Lesser General Public License v3.0 license.
#
# https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Imports
from __future__ import print_function

def split_list(lst, split):
    """Yield successive n-sized chunks from l."""
    if not split:#is 0
        split = len(lst)
    return [lst[i:i + split] for i in range(0, len(lst), split)]
