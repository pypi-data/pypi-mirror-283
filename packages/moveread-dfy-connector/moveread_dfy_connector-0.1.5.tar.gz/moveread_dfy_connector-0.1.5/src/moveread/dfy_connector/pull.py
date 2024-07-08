from typing import NamedTuple, Sequence
import asyncio
from uuid import uuid4
from sqlmodel import Session, select
from haskellian import either as E, dicts as D
from kv import KV
import pure_cv as vc
from pipeteer import WriteQueue
from moveread.dfy import Game, Pairing, SheetModel, Tournament
from moveread.pipelines.dfy import Input
from dslog import Logger

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
  print('Read online')
  jpg = vc.encode(vc.decode(img), '.jpg')
  return (await pipeline_images.insert(url_to, jpg)).unsafe()

async def copy_images(
  from_urls: Sequence[str], to_urls: Sequence[str], *, id: str,
  online_images: KV[bytes], pipeline_images: KV[bytes]
):
  tasks = [jpg_copy(from_, to, online_images=online_images, pipeline_images=pipeline_images) for from_, to in zip(from_urls, to_urls)]
  results = await asyncio.gather(*tasks)
  return E.sequence(results)

def inputId(tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId}/{group}/{round}/{board}_{uuid4()}'

@E.do()
async def pull_game(
  game: Game, model: str, *,
  online_images: KV[bytes], blobs: KV[bytes], Qpush: WriteQueue[Input]
):
  id = inputId(**game.gameId())
  x = new_input(id, game, model=model)
  (await copy_images(x.from_urls, x.to_urls, id=id, online_images=online_images, pipeline_images=blobs)).unsafe()
  (await Qpush.push(id, x.input)).unsafe()


async def pull_games(
  session: Session, games: Sequence[Game], *, logger: Logger = Logger.click(),
  online_images: KV[bytes], blobs: KV[bytes], Qpush: WriteQueue[Input],
):
  tnmt_games = D.group_by(lambda g: g.tournId, games)
  for tournId, games in tnmt_games.items():
    model = sheet_model(session, tournId)
    if model is None:
      logger(f'No model for tournament "{tournId}"', level='WARNING')
      continue

    for game in games:
      r = await pull_game(game, model, online_images=online_images, blobs=blobs, Qpush=Qpush)
      if r.tag == 'left':
        logger(f'Error pulling game {game.gameId()}: {r.value}', level='ERROR')
      else:
        game.status = Game.Status.doing
        session.add(game)
        session.commit()
        logger(f'Pulled game {game.gameId()}')