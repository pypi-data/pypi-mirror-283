from typing import Sequence, Literal, TypeAlias, Unpack, Any, Iterable, Coroutine
import asyncio
from uuid import uuid4
from sqlalchemy import Engine
from sqlmodel import Session, select
from fastapi import UploadFile
from haskellian import either as E, Left, Either, promise as P, Iter
import pure_cv as vc
from kv import KV, InexistentItem
import chess_pairings as cp
from .pgns import export_all
from .util import TimedIterableCache
from moveread.dfy import Game, Token, Group, Image, Tournament, FrontendPGN, queries

ImgExtension: TypeAlias = Literal['.jpg', '.png', '.webp']
MimeType: TypeAlias = str

def stringify(tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId}/{group}/{round}/{board}'

def safe_extension(file: UploadFile) -> str | None:
  if file.filename and len(parts := file.filename.split('.')) == 2:
    return parts[1]
  
def descale2jpg(img: bytes, height: int):
  mat = vc.decode(img)
  return vc.encode(vc.descale_h(mat, height), format='.jpg')
  
class SDK:

  def __init__(self, images: KV[bytes], engine: Engine, *, cache_ttl: float = 30, cache_max_entries: int = 1000):
    self._images = images
    self._engine = engine
    self.pgns_cache = TimedIterableCache(self._round_pgn, ttl_secs=cache_ttl, max_entries=cache_max_entries)

  def __repr__(self) -> str:
    return f'SDK(images={self._images}, engine={self._engine})'

  def authorize(self, token: str, tournId: str) -> bool:
    with Session(self._engine) as ses:
      results = ses.exec(select(Token).where(Token.token == token, Token.tournId == tournId))
      return results.first() is not None

  def tournaments(self) -> Sequence[Tournament]:
    with Session(self._engine) as ses:
      return ses.exec(select(Tournament)).all()

  def tournament(self, tournId: str) -> Tournament | None:
    with Session(self._engine) as ses:
      return ses.exec(queries.select_tnmt(tournId)).first()
    
  def group(self, tournId: str, group: str) -> Group | None:
    with Session(self._engine) as ses:
      return ses.exec(queries.select_group(tournId, group)).first()
  
  def round(self, **roundId: Unpack[cp.RoundId]) -> Sequence[Game]:
    with Session(self._engine) as ses:
      order: Any = Game.index # order_by's typing is messed up
      stmt = select(Game).where(*queries.round_games(**roundId)).order_by(order)
      return ses.exec(stmt).all()
    
  def _round_pgn(self, roundId: tuple[str, str, str]):
    rid = cp.roundId(*roundId)
    with Session(self._engine) as ses:
      order: Any = Game.index
      round = ses.exec(queries.select_round(**rid)).first()
      stmt = select(Game).where(*queries.round_games(**rid)).order_by(order)
      games = ses.exec(stmt).all()
      tnmt = ses.exec(queries.select_tnmt(rid['tournId'])).first()
      yield from export_all(games, tnmt, round)
    
  def round_pgn(self, *, skip: int = 0, take: int | None = None, tournId: str, group: str, round: str, no_cache: bool = False) -> Iterable[str]:
    id = (tournId, group, round)
    iter = self.pgns_cache[id] if not no_cache else self.pgns_cache.insert(id)
    iter = Iter(iter).skip(skip)
    return iter.take(take) if take is not None else iter  

  def group_pgn(self, *, skip: int = 0, take: int | None = None, no_cache: bool = False, **groupId: Unpack[cp.GroupId]) -> Iterable[str]:
    with Session(self._engine) as ses:
      group = ses.exec(queries.select_group(**groupId)).first()
      if group:
        for round in group.rounds:
          yield from self.round_pgn(skip=skip, take=take, **groupId, round=round, no_cache=no_cache)

  def game_pgn(self, **gameId: Unpack[cp.GameId]) -> FrontendPGN | None:
    with Session(self._engine) as ses:
      game = ses.exec(queries.select_game(**gameId)).first()
      if game and game.pgn:
        return game.pgn
      
  def images(self, **gameId: Unpack[cp.GameId]) -> Sequence[str] | None:
    with Session(self._engine) as ses:
      game = ses.exec(queries.select_game(**gameId)).first()
      if game:
        return [img.descaled_url for img in game.imgs]
  
  async def _upload(self, image: UploadFile, url: str):
    return await self._images.insert(url, await image.read())
  
  async def _descale_imgs(self, imgs: Sequence[tuple[str, bytes]], target_height: int):
    """Descales and uploads the images. Expects `(url, img)` tuples"""
    descaled = [descale2jpg(img, target_height) for _, img in imgs]
    uploads = [self._images.insert(url, img) for (url, _), img in zip(imgs, descaled)]
    return await asyncio.gather(*uploads)

  async def post_game(
    self, images: Sequence[UploadFile],
    descaled_height: int = 768, **gameId: Unpack[cp.GameId]
  ) -> tuple[Either, Coroutine]:
    """ - Runs tasks that must happen before responding to the client.
    - Returns the result + a coroutine that must run after responding (independent of the result)
    """
    img_urls = []
    descaled_urls = []
    delete_urls = []
    imgs = []

    try:
      with Session(self._engine) as ses:
        game = ses.exec(queries.select_game(**gameId)).first()
        if game is None:
          return Left(InexistentItem(detail=f'Game {gameId} not found in DB')), P.of(None).run()
        
        uuid = f'{stringify(**gameId)}_{uuid4()}'
        img_urls = [f'{uuid}/{i}.' + (safe_extension(img) or 'jpg') for i, img in enumerate(images)]
        descaled_urls = [f'{uuid}/{i}-{descaled_height}.jpg' for i in range(len(images))]

        imgs = await asyncio.gather(*[img.read() for img in images])
        original_uploads = [self._images.insert(url, img) for url, img in zip(img_urls, imgs)]
        res = E.sequence(await asyncio.gather(*original_uploads))

        delete_urls = [img.url for img in game.imgs] + [img.descaled_url for img in game.imgs]
        [ses.delete(img) for img in game.imgs]
        game.imgs = [Image(url=url, descaled_url=url) for url in img_urls]
        game.status = Game.Status.uploaded
        ses.add(game)
        ses.commit()
    except Exception as e:
      res = Left(e)

    if res.tag == 'right':
      async def post_tasks():
        deletions = [self._images.delete(url) for url in delete_urls]
        descaled_uploads = self._descale_imgs(list(zip(descaled_urls, imgs)), descaled_height)
        await asyncio.gather(*deletions, descaled_uploads)

        with Session(self._engine) as ses:
          if (game := ses.exec(queries.select_game(**gameId)).first()):
            for img, descaled_url in zip(game.imgs, descaled_urls):
              img.descaled_url = descaled_url
              ses.add(img)
            ses.commit()

    else:
      async def post_tasks():
        await asyncio.gather(*[self._images.delete(url) for url in img_urls]) # not to leak storage

    return res, post_tasks()
