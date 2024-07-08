from typing import Literal
from dataclasses import dataclass, field
from moveread.core import Image, Rectangle

@dataclass
class ImgOutput:
  img: str
  meta: Image.Meta = field(default_factory=Image.Meta)

@dataclass
class Output:
  original: ImgOutput
  corrected: ImgOutput
  boxes: list[str]

@dataclass
class BaseInput:
  img: str
  model: str

@dataclass
class Uncorrected(BaseInput):
  tag: Literal['uncorrected'] = 'uncorrected'

@dataclass
class BaseCorrected(BaseInput):
  corrected: str

@dataclass
class Corrected(BaseCorrected):
  tag: Literal['corrected'] = 'corrected'

@dataclass
class BaseExtracted(BaseCorrected):
  contours: list
  contoured: str

@dataclass
class Extracted(BaseExtracted):
  tag: Literal['extracted'] = 'extracted'

@dataclass
class Selected(BaseCorrected):
  grid_coords: Rectangle
  tag: Literal['selected'] = 'selected'