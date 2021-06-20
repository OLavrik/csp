import numpy as np
from random import random, seed
import cv2 
from collections import defaultdict
data = defaultdict(list)

VERBOSE = True

with open('train.csv', 'rt') as fp:
  for i, line in enumerate(fp):
    if i > 0:
      _id, _time, _x, _y = [int(_.strip(' \t\r\n')) for _ in line.split(',')]
      data[_id].append({'t': _time, 'rr': _x, 'y': _y})


print(len(data))


def check_if_anomaly(t, x):
  (t_1, t0, a, b, c, d, tn) = t
  (x_1, x0, x1, x2, x3, x4, x5) = x
  d_1, d0, d1, d2, d3, d4, d5 = t_1 - t0, a - t0, b - a, c - b, d - c, tn - d, t0 - tn

  MIN_DY = 17
  MAX_DY = 85

  FLUCT_COEFF = 0.39
  
  FLOAT_COEFF = 1.112
  
  if MIN_DY < d1 < MAX_DY:
    dst = d1
    if -2 * dst * (1 + FLOAT_COEFF) < d2 < -2 * dst * (1 - FLOAT_COEFF):
      if dst * (1 - 2*FLOAT_COEFF) < d3 < dst * (1 + 2*FLOAT_COEFF):
        dst = min(-d2, 2 * d1, 2 * d3)
        if b > a > c and c < d < b and abs(d4) < abs(dst) * 1 * FLUCT_COEFF and \
                abs(d0) < abs(dst) * FLUCT_COEFF and \
                abs(d5) < abs(dst) * 1 * FLUCT_COEFF and \
                c > 400:
          return True
  return False

import time
seed(time.time())

for key, value in data.items():
  if key < 20 or key > 140:
    continue
  W = 1000
  H = 1000

  max_t = 0
  min_t = 10000000
  for _ in value:
    max_t = max(max_t, _['t'])
    min_t = min(min_t, _['t'])

  print(f'seria {key}: {len(value)}, min: {min_t}, max: {max_t}')

  scale = W / max_t

  SCALE = 100
  INDENT = 0
  i = 0
  _c = value[0]
  draw_green = 0

  if VERBOSE:
    cv2.namedWindow('frame')

  def handle_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      print(f'{key}, s, {x * SCALE + INDENT}')
    if event == cv2.EVENT_RBUTTONDOWN:
      print(f'{key}, e, {x * SCALE + INDENT}')


  if VERBOSE:
    cv2.setMouseCallback('frame', handle_mouse)

  while INDENT < max_t:
    frame_img = np.zeros((W, H, 3)).astype(np.uint8)

    while (_c['t'] - INDENT < SCALE * W) and i < len(value) - 1:
      if i >= 0:
        _c = value[i]
        _n = value[i + 1]

        if i > 0 and i < len(value) - 6 and check_if_anomaly(
                (value[i - 1]['rr'],value[i]['rr'], value[i + 1]['rr'], value[i + 2]['rr'], value[i + 3]['rr'], value[i + 4]['rr'], value[i + 5]['rr']),
                (value[i - 1]['t'],value[i]['t'], value[i + 1]['t'], value[i + 2]['t'], value[i + 3]['t'], value[i + 4]['t'], value[i + 5]['t'])):

          _x0 = (value[max(0, i - 1)]["t"] - 1000)
          _x1 = (value[max(0, i + 5)]["t"])

          print(f'{key}, s, {_x0}')
          print(f'{key}, e, {_x1}')

          _x0 = int((_x0 - INDENT) // SCALE)
          _x1 = int((_x1 - INDENT) // SCALE)

          cv2.line(frame_img, (_x0, 100), (_x0, 900), (255, 255, 0), 1)
          cv2.line(frame_img, (_x1, 100), (_x1, 900), (255, 255, 0), 1)
          draw_green = 5



        x0 = int((_c['t'] - INDENT) // SCALE)
        x1 = int((_n['t'] - INDENT) // SCALE)

        y0= _c['rr']//3
        y1= _n['rr']//3

        clr = (255, 255, 255) if not(_c['y'] and _n['y']) else (0, 0, 255)
        cv2.line(frame_img, (x0, y0), (x1, y1), clr, 1)
 
        if 0 < x0 < W and 0 < y0 < H:
          frame_img[y0, x0] = (0, 255, 0)

        if draw_green > 0:
          cv2.line(frame_img, (x0, y0 + 4), (x1, y1 + 4), (0, 255, 0), 1)
          draw_green -= 1

      i += 1
    INDENT += SCALE * W
    if VERBOSE:
      cv2.imshow('frame', frame_img)
      cv2.waitKey(0)
    
     