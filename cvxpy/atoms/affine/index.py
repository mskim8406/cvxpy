"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from affine_atom import AffAtom
from ... import utilities as u
from ...utilities import bool_mat_utils as bu
from ...utilities import key_utils as ku
from ...expressions.variables import Variable
import cvxpy.lin_ops.lin_utils as lu
import cvxpy.lin_ops.lin_op as lo
from cvxpy.lin_ops import LinExpr

class index(AffAtom):
    """ Indexing/slicing into a matrix. """
    # expr - the expression indexed/sliced into.
    # key - the index/slicing key (i.e. expr[key[0],key[1]]).
    def __init__(self, expr, key):
        # Format and validate key.
        self.key = ku.validate_key(key, expr.shape)
        super(index, self).__init__(expr)

    # The string representation of the atom.
    def name(self):
        return self.args[0].name() + "[%s, %s]" % ku.to_str(self.key)

    # Returns the index/slice into the given value.
    @AffAtom.numpy_numeric
    def numeric(self, values):
        return values[0][self.key]

    # The shape, sign, and curvature of the index/slice.
    def init_dcp_attr(self):
        self._dcp_attr = self.args[0]._dcp_attr[self.key]

    def graph_implementation(self, arg_objs):
        x = arg_objs[0]
        index_op = lo.LinOp(lo.INDEX, x.var_id, x.var_size, 1.0, self.key)
        obj = LinExpr([index_op], self.size)
        return (obj, [])
