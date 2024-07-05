from typing import NamedTuple, Sequence
import asyncio
from sqlmodel import Session, select
from haskellian import either as E
from kv.api import KV
import pure_cv as vc
from moveread.dfy.types import Game, Pairing, SheetModel
from moveread.pipelines.dfy import Input

def pairing_display(pairing: Pairing):
  pair = pairing.root
  if pair.tag == 'unpaired':
    return 'Unpaired!?'
  
  s = f'{pair.white} - {pair.black}'
  if pair.result is not None:
    s += f' {pair.result}'
  return s


def title(pairing: Pairing, tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId} {group}/{round}/{board} {pairing_display(pairing)}'

class NewInput(NamedTuple):
  input: Input
  """Pipeline input"""
  from_urls: Sequence[str]
  to_urls: Sequence[str]

def new_input(uuid: str, game: Game, *, model: str):
  gid = game.gameId()
  from_urls = [img.url for img in game.imgs]
  to_urls = [f'{uuid}/{i}.jpg' for i in range(len(from_urls))]
  endpoint = f'/v1/models/{gid["tournId"]}-{gid["group"]}:predict'
  task = Input(gameId=gid, model=model, imgs=to_urls, title=title(game.pairing, **gid), serving_endpoint=endpoint)
  return NewInput(input=task, from_urls=from_urls, to_urls=to_urls)


def sheet_model(session: Session, tournId: str) -> str | None:
  stmt = select(SheetModel).where(SheetModel.tournId == tournId)
  obj = session.exec(stmt).first()
  return obj and obj.model

@E.do()
async def jpg_copy(
  url_from: str, url_to: str, *,
  online_images: KV[bytes], pipeline_images: KV[bytes]
):
  """Copies the image by downloading it first, encoding it as JPG, then inserting"""
  img = (await online_images.read(url_from)).unsafe()
  jpg = vc.encode(vc.decode(img), '.jpg')
  return (await pipeline_images.insert(url_to, jpg)).unsafe()

async def copy_images(
  from_urls: Sequence[str], to_urls: Sequence[str], *, id: str,
  online_images: KV[bytes], pipeline_images: KV[bytes]
):
  tasks = [jpg_copy(from_, to, online_images=online_images, pipeline_images=pipeline_images) for from_, to in zip(from_urls, to_urls)]
  results = await asyncio.gather(*tasks)
  return E.sequence(results)
