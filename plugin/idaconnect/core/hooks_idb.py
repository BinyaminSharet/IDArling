import logging

import idc
import ida_idp

# Import ABC and events
from hooks_abc import Hooks
from ..events.events_idb import *


logger = logging.getLogger('IDAConnect.Core')

# -----------------------------------------------------------------------------
# IDB Hooks
# -----------------------------------------------------------------------------


class IDBHooks(ida_idp.IDB_Hooks, Hooks):

    def __init__(self, plugin):
        ida_idp.IDB_Hooks.__init__(self)
        Hooks.__init__(self, plugin)

    def make_code(self, insn):
        self._sendEvent(MakeCodeEvent(insn.ea))
        return 0

    def make_data(self, ea, flags, tid, size):
        self._sendEvent(MakeDataEvent(ea, flags, tid, size))
        return 0

    def renamed(self, ea, new_name, local_name):
        self._sendEvent(RenamedEvent(ea, new_name, local_name))
        return 0

    def func_added(self, func):
        self._sendEvent(FuncAddedEvent(func.startEA, func.endEA))
        return 0

    def deleting_func(self, func):
        self._sendEvent(DeletingFuncEvent(func.startEA))
        return 0

    def set_func_start(self, func, new_ea):
        self._sendEvent(SetFuncStartEvent(func.startEA, new_ea))
        return 0

    def set_func_end(self, func, new_ea):
        self._sendEvent(SetFuncEndEvent(func.startEA, new_ea))
        return 0

    def cmt_changed(self, ea, repeatable_cmt):
        cmt = idc.get_cmt(ea, repeatable_cmt)
        if not cmt:
            cmt = ""
        self._sendEvent(CmtChangedEvent(ea, repeatable_cmt, cmt))
        return 0

    def ti_changed(self, ea, t, fname):
        t = idc.GetTinfo(ea)
        self._sendEvent(TiChangedEvent(ea, t))
        return 0
    
    def op_type_changed(self, ea, n):
        flags = idc.get_full_flags(ea)
        if n == 0:
            if idc.isHex0(flags):
                op = "hex"
            if idc.isBin0(flags):
                op = "bin"
            if idc.isDec0(flags):
                op = "dec"
            if idc.isChar0(flags):
                op = "chr"
            if idc.isOct0(flags):
                op = "oct"
        else:
            if idc.isHex1(flags):
                op = "hex"
            if idc.isBin1(flags):
                op = "bin"
            if idc.isDec1(flags):
                op = "dec"
            if idc.isChar1(flags):
                op = "chr"
            if idc.isOct1(flags):
                op = "oct"
        self._sendEvent(OpTypeChangedEvent(ea, n, flags, op))
        return 0
