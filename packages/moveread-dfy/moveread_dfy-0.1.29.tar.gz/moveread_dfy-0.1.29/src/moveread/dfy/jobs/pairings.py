from typing import Sequence
from datetime import datetime, timedelta
from sqlmodel import select, Session
import chess_pairings as cp
from moveread.dfy import Group, Pairings, Game, Pairing, Tournament, queries
from haskellian import Either, Left, Right
from dslog import Logger

def current_pairings(session: Session, now: datetime):
  tomorrow = now + timedelta(days=1)
  yesterday = now - timedelta(days=1)
  stmt = select(Tournament, Pairings) \
    .where(Tournament.start_date < tomorrow, yesterday < Tournament.end_date) \
    .join(Pairings, Tournament.tournId == Pairings.tournId) # type: ignore
  return session.exec(stmt).all()

def update_rounds(session: Session, tnmt: Tournament, group: str, rounds: Sequence[str]) -> Either[str, str]:
  """Update the group's `rounds` list"""
  grp = session.get(Group, (tnmt.tournId, group))
  if grp is None:
    return Left(f'Group "{tnmt.tournId}/{group}" not found')
  elif grp.rounds != rounds:
    og_rounds = [*grp.rounds]
    grp.rounds = rounds
    session.add(grp)
    session.commit()
    return Right(f'Updated group "{tnmt.tournId}/{group}". Rounds {og_rounds} -> {rounds}')
  else:
    return Right(f'Group "{tnmt.tournId}/{group}" already has rounds {rounds}')
  

def update_pairings(session: Session, *, tournId: str, group: str, pairings: cp.GroupPairings):
    """Insert/update pairings"""
    group_games = session.exec(queries.select_group_games(tournId, group)).all()
    games_idx = cp.GamesMapping[Game].from_pairs([(g.gameId(), g) for g in group_games])
    added: list[cp.GameId] = []
    updated: list[cp.GameId] = []

    for round, rnd_pairings in pairings.items():
      for board, pair in rnd_pairings.items():
        gid = cp.gameId(tournId, group, round, board)
        if gid in games_idx:
          game = games_idx[gid]
          if game.pairing.root != pair:
            game.pairing = Pairing(pair)
            updated.append(gid)
        else:
          game = Game(tournId=tournId, group=group, round=round, board=board, index=int(board)-1, pairing=Pairing(pair))
          added.append(gid)
        
        session.add(game)
    
    session.commit()
    return added, updated


async def update_current_pairings(session: Session, *, now: datetime, logger: Logger = Logger.click()):
  """Updates pairings for all ongoing tournaments"""
  pairing_sources = current_pairings(session, now)
  current_tnmts = [tnmt.tournId for tnmt, _ in pairing_sources]
  logger(f'Updating current tournaments: {", ".join(current_tnmts)}')
  for tnmt, src in pairing_sources:
    e = await cp.scrape_pairings(src.pairings)
    if e.tag == 'left':
      logger(f'Error fetching pairings for "{tnmt.tournId}/{src.group}"', e.value, level='ERROR')
      continue
    pairings = e.value
    rounds = [str(i+1) for i in range(len(pairings))]
    r = update_rounds(session, tnmt, src.group, rounds)
    logger(r.value, level='DEBUG' if r.tag == 'right' else 'ERROR')
    added, updated = update_pairings(session, tournId=tnmt.tournId, group=src.group, pairings=pairings)
    logger(f'Updated pairings for "{tnmt.tournId}/{src.group}", added {len(added)} and updated {len(updated)} games', level='DEBUG')