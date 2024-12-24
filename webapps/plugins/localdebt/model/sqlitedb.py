

from webapps.modules.dbbroker.sqlite import Sqlitedbs
from webapps.plugins.localdebt.model.dao.debt import LocalPublicDebt


db = Sqlitedbs(db_store='./.db_store/localdebt.db')


LocalPublicDebt