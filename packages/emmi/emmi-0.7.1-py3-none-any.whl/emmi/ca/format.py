#!/usr/bin/python3

from caproto.asyncio.client import Context as ClientContext
from caproto import ChannelType

import logging, asyncio
logger = logging.getLogger(__name__)

class PvStringFormatter:
    def __init__(self, fmt, **components):
        ''' Follows the PVs in `components` and formats `fmt` according to component names.
        '''
        self.comp_format = fmt
        self.comp_dict = components.copy()
        self._comp_rev_dict = { v:k for k,v in self.comp_dict.items() }
        self.comp_pvs = None
        self.comp_monitors = None
        self.ctx = None
        self.comp_data = {}


    async def connect(self, ctx=None):
        if ctx is not None:
            self.ctx = ctx
        if self.ctx is None:
            self.ctx = ClientContext()

        self.comp_pvs = {
            k:v for k,v in zip(
                self.comp_dict.keys(),
                await ctx.get_pvs(*[f for f in self.comp_dict.values()])
            )
        }

        tmp = {p[0]:p[1].name for p in self.comp_pvs.items()}
        logger.info(f'String formatter PVs: {tmp}')

        self.comp_monitors = {
            k:v.subscribe() for k,v in self.comp_pvs.items()
        }

        logger.info(f'String element monitors: {self.comp_monitors}')

        for m in self.comp_monitors.values():
            m.add_callback(self._incoming)


    def _incoming(self, pv, data):
        pv_name = pv.pv.name
        pv_data = data.data[0]
        pv_key = self._comp_rev_dict[pv_name]
        
        if data.data_type == ChannelType.STRING:
            pv_data = pv_data.decode()
            
        self.comp_data[pv_key] = pv_data
        print(f'{pv_key}: {pv_data}')


    @property
    def current(self):
        try:
            return self.comp_format.format(**self.comp_data)
        except KeyError as e:
            logger.error(f'Not enough keys for "{self.comp_format}": {e}')
            return None
