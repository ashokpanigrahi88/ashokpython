import oratechexport
import dbconfig
oratechexport.exportdata(p_frequency=int(dbconfig.DATA_FREQUENCY))