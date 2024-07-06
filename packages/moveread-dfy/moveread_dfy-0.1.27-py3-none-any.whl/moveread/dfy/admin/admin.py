from typing import Sequence
from sqlmodel import Session
from dslog import Logger
from moveread.dfy import Tournament, Group, SheetModel, queries

def upsert_tnmt(session: Session, tnmt: Tournament, *, logger: Logger = Logger.click()):
  if (curr := session.exec(queries.select_tnmt(tnmt.tournId)).first()):
    logger('Deleting existing entry:', tnmt)
    session.delete(curr)
  logger('Inserting new entry:', tnmt)
  session.add(tnmt)

def upsert_group(
  session: Session, tournId: str, group: str, *,
  logger: Logger = Logger.click(), rounds: Sequence[str] = []
):
  if (grp := session.exec(queries.select_group(tournId, group)).first()):
    logger('Deleting existing groups:', group)
    session.delete(grp)
  
  grp = Group(tournId=tournId, name=group, rounds=rounds)
  logger('Inserting new group:', grp)
  session.add(grp)

def upsert_model(session: Session, tournId: str, model: str, *, logger: Logger = Logger.click()):
  if (curr := session.exec(queries.select_model(tournId)).first()):
    if curr.model == model:
      logger(f'Model "{model}" already set for "{tournId}"')
    else:
      logger(f'Updating model for "{tournId}": "{curr.model}" -> "{model}"')
      curr.model = model
      session.add(curr)
  else:
    logger(f'Inserting new model for "{tournId}": "{model}"')
    session.add(SheetModel(tournId=tournId, model=model))


class API:
  def __init__(self, session: Session, logger: Logger = Logger.click()):
    self.session = session
    self.logger = logger

  def upsert_tnmt(self, tnmt: Tournament):
    upsert_tnmt(self.session, tnmt, logger=self.logger)

  def upsert_group(self, tournId: str, group: str, *, rounds: Sequence[str] = []):
    upsert_group(self.session, tournId, group, rounds=rounds, logger=self.logger)

  def upsert_model(self, tournId: str, model: str):
    upsert_model(self.session, tournId, model, logger=self.logger)
