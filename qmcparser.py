# -*- coding:utf-8 -*-
import os


class QmcParser(object):
    def __init__(self):
        self.x, self.y, self.dx, self.index = -1, 8, 1, -1
        self.seedMap = [
            [0x4a, 0xd6, 0xca, 0x90, 0x67, 0xf7, 0x52],
            [0x5e, 0x95, 0x23, 0x9f, 0x13, 0x11, 0x7e],
            [0x47, 0x74, 0x3d, 0x90, 0xaa, 0x3f, 0x51],
            [0xc6, 0x09, 0xd5, 0x9f, 0xfa, 0x66, 0xf9],
            [0xf3, 0xd6, 0xa1, 0x90, 0xa0, 0xf7, 0xf0],
            [0x1d, 0x95, 0xde, 0x9f, 0x84, 0x11, 0xf4],
            [0x0e, 0x74, 0xbb, 0x90, 0xbc, 0x3f, 0x92],
            [0x00, 0x09, 0x5b, 0x9f, 0x62, 0x66, 0xa1]
        ]

    def _next_mask(self):
        self.index += 1
        ret = None
        if self.x < 0:
            self.dx = 1
            self.y = ((8 - self.y) % 8)
            # ret =((8 -y)%8)
            ret = 0xc3
        elif self.x > 6:
            self.dx = -1
            self.y = 7 - self.y
            ret = 0xd8
        else:
            ret = self.seedMap[self.y][self.x]
        self.x += self.dx
        if self.index == 0x8000 or (self.index > 0x8000 and (self.index + 1) % 0x8000 == 0):
            return self._next_mask()
        return ret

    def _reset(self):
        self.x, self.y, self.dx, self.index = -1, 8, 1, -1

    def _decode_bytes(self, path):
        self._reset()
        with open(path, 'rb') as f:
            buf = f.read()
            buf_len = len(buf)
            buf_temp = bytearray(buf_len)
            for i in range(buf_len):
                buf_temp[i] = self._next_mask() ^ buf[i]
            return buf_temp

    def parse(self, in_, out_):
        decode_buf = self._decode_bytes(in_)
        with open(out_, 'wb') as fout:
            fout.write(decode_buf)