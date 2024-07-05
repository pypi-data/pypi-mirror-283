from sqlalchemy import (Boolean, Column, DateTime, Integer, String, text)
from . import CreatedModifiedBase, Base


class Linescore(CreatedModifiedBase, Base):
    __tablename__ = 'linescores'

    game_id = Column(Integer, primary_key=True)
    tgt_id = Column(Integer, primary_key=True)
    opp_id = Column(Integer, primary_key=True)
    tgt_score_period_1 = Column(Integer)
    tgt_score_period_2 = Column(Integer)
    tgt_score_period_3 = Column(Integer)
    tgt_score_period_4 = Column(Integer)
    tgt_score_period_5 = Column(Integer)
    tgt_score_cuml_1 = Column(Integer)
    tgt_score_cuml_2 = Column(Integer)
    tgt_score_cuml_3 = Column(Integer)
    tgt_score_cuml_4 = Column(Integer)
    tgt_score_cuml_5 = Column(Integer)
    opp_score_period_1 = Column(Integer)
    opp_score_period_2 = Column(Integer)
    opp_score_period_3 = Column(Integer)
    opp_score_period_4 = Column(Integer)
    opp_score_period_5 = Column(Integer)
    opp_score_cuml_1 = Column(Integer)
    opp_score_cuml_2 = Column(Integer)
    opp_score_cuml_3 = Column(Integer)
    opp_score_cuml_4 = Column(Integer)
    opp_score_cuml_5 = Column(Integer)
