_J='propagate'
_I='logging.StreamHandler'
_H='formatter'
_G='console_verbose'
_F='console_simple'
_E='format'
_D='withfile'
_C='simple'
_B=False
_A='handlers'
import logging,os
from logging.config import dictConfig
from detail.client.instrumentation.base import DisableDetail
level=os.environ.get('DETAIL_LOG_LEVEL','INFO')
config={'version':1,'disable_existing_loggers':_B,'formatters':{_C:{_E:'%(levelname)s: [%(asctime)s] %(name)s: %(message)s'},_D:{_E:'%(levelname)s: [%(asctime)s] (%(module)s:%(lineno)s): %(message)s'}},_A:{_F:{'class':_I,_H:_C},_G:{'class':_I,_H:_D}},'loggers':{'detail':{_A:[_G],'level':level,_J:_B},'vcr.stubs':{_A:[_F],'level':level,_J:_B}}}
def init():dictConfig(config)
class DetailLogger(logging.Logger):
	def _log(C,*A,**B):
		with DisableDetail():return super()._log(*A,**B,stacklevel=2)
def get_detail_logger(*B,**C):A=logging.Logger.manager;D=A.loggerClass;A.loggerClass=DetailLogger;E=logging.getLogger(*B,**C);A.loggerClass=D;return E