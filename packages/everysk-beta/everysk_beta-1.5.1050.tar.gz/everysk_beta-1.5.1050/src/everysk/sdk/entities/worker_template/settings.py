###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################

###############################################################################
#   Imports
###############################################################################
from everysk.core.fields import StrField, ListField, IntField

###############################################################################
#   Settings Implementation
###############################################################################
WORKER_TEMPLATE_ID_PREFIX = StrField(default='wrkt_', readonly=True)

WORKER_TEMPLATE_STARTER_TYPE = StrField(default='STARTER', readonly=True)
WORKER_TEMPLATE_BASIC_TYPE = StrField(default='BASIC', readonly=True)
WORKER_TEMPLATE_FORKER_TYPE = StrField(default='FORKER', readonly=True)
WORKER_TEMPLATE_BARRIER_TYPE = StrField(default='BARRIER', readonly=True)
WORKER_TEMPLATE_CONDITIONAL_TYPE = StrField(default='CONDITIONAL', readonly=True)
WORKER_TEMPLATE_TRY_TYPE = StrField(default='TRY', readonly=True)
WORKER_TEMPLATE_CATCH_TYPE = StrField(default='CATCH', readonly=True)
WORKER_TEMPLATE_ENDER_TYPE = StrField(default='ENDER', readonly=True)

WORKER_TEMPLATE_DEFAULT_TYPE = StrField(default='{WORKER_TEMPLATE_BASIC_TYPE}', readonly=True)
WORKER_TEMPLATE_TYPES = ListField(
    default=['STARTER', 'BASIC', 'FORKER', 'BARRIER', 'CONDITIONAL', 'TRY', 'CATCH', 'ENDER'],
    readonly=True
)

WORKER_TEMPLATE_CATEGORIES = ListField(
    default=[
        'portfolio',
        'parsers',
        'datastore',
        'datastore_generators',
        'report',
        'custom_index',
        'file',
        'OCR',
        'compliance',
        'flow_control',
        'calculation',
        'network',
        'signals',
        'trades',
        'connectors',
        'private_security',
        'miscellaneous'
    ],
    readonly=True
)

WORKER_TEMPLATE_ICONS = ListField(
    default=[
        'analysis',
        'attribution',
        'bridge',
        'bring',
        'brokerage_inserter',
        'calc',
        'calendar',
        'chart',
        'checklist',
        'compliance',
        'conditional',
        'data',
        'default',
        'delete',
        'developers',
        'distribuition',
        'envelope',
        'exposure',
        'fee',
        'file',
        'generator',
        'graphDown',
        'graphUp',
        'guideline',
        'historic',
        'http',
        'image',
        'info',
        'live',
        'look',
        'mapping',
        'matrix',
        'merge',
        'money',
        'notification',
        'optimize',
        'portfolio',
        'positions',
        'property',
        'provision',
        'ranking',
        'retriever',
        'scale',
        'search',
        'sensitivities',
        'sensitivity',
        'settle_provisions',
        'sftp',
        'stress',
        'table',
        'target',
        'text',
        'time',
        'title',
        'trade_allocation',
        'trade_blotter',
        'trade_inserter',
        'trade_position_provision',
        'upgrade',
        'variable',
        'wall',
        'waves',
        'whatIf',
        'window',
        'zip'
    ],
    readonly=True
)

WORKER_TEMPLATE_SCRIPT_SOURCE_MIN_SIZE = IntField(default=1, readonly=True)
WORKER_TEMPLATE_SCRIPT_SOURCE_MAX_SIZE = IntField(default=500000, readonly=True)

WORKER_TEMPLATE_DEFAULT_SCRIPT_RUNTIME = StrField(default='python', readonly=True)
WORKER_TEMPLATE_SCRIPT_RUNTIMES = ListField(default=['python311', 'python', 'ecmascript5'], readonly=True)

WORKER_TEMPLATE_SCRIPT_OUTPUTS_MAX_SIZE = IntField(default=100, readonly=True)
WORKER_TEMPLATE_SCRIPT_INPUTS_MAX_SIZE = IntField(default=200, readonly=True)
