from haskellian import Either, Left, either as E
from bs4 import BeautifulSoup
from chess_pairings import GroupPairings
from chess_scraping import ParsingError
from .system import find_system

def parse_rounds(soup: BeautifulSoup) -> Either[ParsingError, GroupPairings]:
  match find_system(soup):
    case None:
      return Left(ParsingError('No tournament type found'))
    case 'round-robin':
      from .single_robin import parse_single_round_robin
      return parse_single_round_robin(soup).mapl(ParsingError)
    case 'swiss':
      from .single_swiss import parse_single_swiss
      return parse_single_swiss(soup).mapl(ParsingError)
    case 'team-round-robin' | 'team-swiss':
      return Left(ParsingError('Team tournaments not supported'))
  

@E.do[ParsingError]()
def parse_round(soup: BeautifulSoup):
  rounds = parse_rounds(soup).unsafe()
  if len(rounds) == 1:
    return list(rounds.values())[0]
  else:
    return Left(ParsingError(f'Expected 1 round in HTML, found {len(rounds)}')).unsafe()