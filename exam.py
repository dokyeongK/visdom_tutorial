#!/usr/bin/env python3

# Copyright 2017-present, The Visdom Authors
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import visdom
import matplotlib.pyplot as plt
import argparse
import numpy as np
import math
import os.path
import time
import tempfile
import urllib

def basic_text(vis):
    # -------------------------------
    #        text 사용 예시
    # -------------------------------

    # 창에 글씨 띄우기
    vis.text('Hello World!')

    # 다른 방법
    text = 'Hello World'
    vis.text(text)

def basic_image(vis):
    # -------------------------------
    #        image & images 사용 예시
    # -------------------------------

    # 512 X 256 임의의 데이터가 있는 이미지 Example
    vis.image(np.random.rand(3, 512, 256))
    # 5개의 512 X 256 임의의 데이터가 있는 이미지들 Example
    vis.images(np.random.rand(5, 3, 512, 256))



def basic_matplot(vis):
    # -------------------------------
    #        matplot 사용 예시
    # -------------------------------

    plt.plot([1, 23, 2, 4])
    plt.ylabel('some numbers')
    vis.matplot(plt)

def plotting_scatter(vis):
    # -------------------------------
    #        scatter 사용 예시
    # -------------------------------

    Y = np.random.rand(100)
    vis.scatter(
        X=np.random.rand(100, 2),
        Y=(Y[Y > 0] + 1.5).astype(int),
        opts=dict(
            legend=['Apples', 'Pears'],
            xtickmin=0,
            xtickmax=1,
            xtickstep=0.5,
            ytickmin=0,
            ytickmax=1,
            ytickstep=0.5,
            markersymbol='cross-thin-open',
        ),
    )

    # # 3d scatterplot with custom labels and ranges
    vis.scatter(
        X=np.random.rand(100, 3),
        Y=(Y + 1.5).astype(int),
        opts=dict(
            legend=['Men', 'Women'],
            markersize=5,
            xtickmin=0,
            xtickmax=2,
            xlabel='Arbitrary',
            xtickvals=[0, 0.75, 1.6, 2],
            ytickmin=0,
            ytickmax=2,
            ytickstep=0.5,
            ztickmin=0,
            ztickmax=1,
            ztickstep=0.5,
        )
    )

    # 2D scatterplot 커스터마이징
    win = vis.scatter(
        X=np.random.rand(255, 2),
        Y=(np.random.rand(255) + 1.5).astype(int),
        opts=dict(
            markersize=10, # 동그라미 크기
            markercolor=np.random.randint(0, 255, (2, 3,)), # [[x,x,x],[x,x,x]] 타입의 ndarray 2 : 라벨 color 갯수
        ),
    )

    # 2D scatter plot에 text labels 붙이기
    vis.scatter(
        X=np.random.rand(10, 2),
        opts=dict(
            textlabels=['Label %d' % (i + 1) for i in range(10)]
        )
    )

    # legend 넣기
    vis.scatter(
        X=np.random.rand(10, 2),
        Y=[1] * 5 + [2] * 3 + [3] * 2,
        opts=dict(
            legend=['A', 'B', 'C'],
            textlabels=['Label %d' % (i + 1) for i in range(10)]
        )
    )

def plotting_line(vis):
    # -------------------------------
    #        line 사용 예시
    # -------------------------------

    # X, Y 값에 맞는 선을 그림.
    Y = np.linspace(-5, 5, 100)
    vis.line(
        Y=np.column_stack((Y * Y, np.sqrt(Y + 5))),
        X=np.column_stack((Y, Y)),
        opts=dict(markers=False,
                  showlegend=True,
                  ),
    )

    # WebGL을 이용하여 라인 그리기 Example
    webgl_num_points = 200000
    webgl_x = np.linspace(-1, 0, webgl_num_points)
    webgl_y = webgl_x ** 3
    vis.line(X=webgl_x, Y=webgl_y,
             opts=dict(title='{} points using WebGL'.format(webgl_num_points), webgl=True),
             win="WebGL demo")

    # line 업데이트하기 Example (win에다가 append하는 형식, delete, insert 가능)
    win = vis.line(
        X=np.column_stack((np.arange(0, 10), np.arange(0, 10))),
        Y=np.column_stack((np.linspace(5, 10, 10),
                           np.linspace(5, 10, 10) + 5)),
    )
    vis.line(
        X=np.column_stack((np.arange(10, 20), np.arange(10, 20))),
        Y=np.column_stack((np.linspace(5, 10, 10),
                           np.linspace(5, 10, 10) + 5)),
        win=win,
        update='append'
    )
    vis.line(
        X=np.arange(21, 30),
        Y=np.arange(1, 10),
        win=win,
        name='2',
        update='append'
    )
    vis.line(
        X=np.arange(1, 10),
        Y=np.arange(11, 20),
        win=win,
        name='delete this',
        update='append'
    )
    vis.line(
        X=np.arange(1, 10),
        Y=np.arange(11, 20),
        win=win,
        name='4',
        update='insert' # line 추가하기 가능.
    )
    vis.line(X=None, Y=None, win=win, name='delete this', update='remove') # name에 해당하는 line 삭제

    # line update Example 2. WebGL 창에 업데이트하기.
    vis.line(
        X=webgl_x + 1.,
        Y=(webgl_x + 1.) ** 3,
        win="WebGL demo", # 해당 win에 업데이트.
        update='append',
        opts=dict(title='{} points using WebGL'.format(webgl_num_points * 2), webgl=True)
    )

    # line의 모양 다르게하기 Example.

    vis.line(
        X=np.column_stack((
            np.arange(0, 10),
            np.arange(0, 10),
            np.arange(0, 10),
        )),
        Y=np.column_stack((
            np.linspace(5, 10, 10),
            np.linspace(5, 10, 10) + 5,
            np.linspace(5, 10, 10) + 10,
        )),
        opts={
            'dash': np.array(['solid', 'dash', 'dashdot']),
            'linecolor': np.array([
                [0, 191, 255],
                [0, 191, 255],
                [255, 0, 0],
            ]),
            'title': 'Different line dash types'
        }
    )

    # plot에 area 표시하기 Example.
    Y = np.linspace(0, 4, 200)
    vis.line(
        Y=np.column_stack((np.sqrt(Y), np.sqrt(Y) + 2)),
        X=np.column_stack((Y, Y)),
        opts=dict(
            fillarea=True,
            showlegend=False,
            width=800,
            height=800,
            xlabel='Time',
            ylabel='Volume',
            ytype='log',
            title='Stacked area plot',
            marginleft=30,
            marginright=30,
            marginbottom=80,
            margintop=30,
        ),
    )

def plotting_stem(vis):
    Y = np.linspace(0, 2 * math.pi, 70)
    X = np.column_stack((np.sin(Y), np.cos(Y)))
    vis.stem(
        X=X,
        Y=Y,
        opts=dict(legend=['Sine', 'Cosine'])
    )

def plotting_heatmap(vis):
    vis.heatmap(
        X=np.outer(np.arange(1, 6), np.arange(1, 11)),
        opts=dict(
            columnnames=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],  # col 에 주석
            rownames=['y1', 'y2', 'y3', 'y4', 'y5'],  # row 에 주석
            colormap='Electric',
        )
    )

def plotting_bar(vis):
    # bar 모양 plot
    vis.bar(X=np.random.rand(20))
    vis.bar(
        X=np.abs(np.random.rand(5, 3)),
        opts=dict(
            stacked=True,
            legend=['Facebook', 'Google', 'Twitter'],
            rownames=['2012', '2013', '2014', '2015', '2016'] # row 에 주석
        )
    )
    vis.bar(
        X=np.random.rand(20, 3),
        opts=dict(
            stacked=False,
            legend=['The Netherlands', 'France', 'United States']
        )
    )

def plotting_histogram(vis):
    vis.histogram(X=np.random.rand(10000), opts=dict(numbins=50)) # numbins : bin 갯수 벡터.

def plotting_boxplot(vis):
    X = np.random.rand(100, 2)
    X[:, 1] += 2 # 100 X 2 형태 ( random한 벡터 1개랑 그 벡터에 2씩 더한 벡터 1개. )
    vis.boxplot(
        X=X,
        opts=dict(legend=['Men', 'Women'])
    )

def plotting_surf(vis):

    # 임의 x, y값 설정 후 plot 찍기 Example
    x = np.tile(np.arange(1, 101), (100, 1))
    y = x.transpose()

    X = np.exp((((x - 50) ** 2) + ((y - 50) ** 2)) / -(20.0 ** 2))

    vis.surf(X=X, opts=dict(colormap='Viridis')) # or 'Hot'

def plotting_contour(vis):
    # 임의 x, y값 설정 후 plot 찍기 Example
    x = np.tile(np.arange(1, 101), (100, 1))
    y = x.transpose()

    X = np.exp((((x - 50) ** 2) + ((y - 50) ** 2)) / -(20.0 ** 2))

    vis.contour(X=X, opts=dict(colormap='Hot')) # or 'Viridis'

def plotting_quiver(vis):
    # quiver 모양의 plot 그리기.
    X = np.arange(0, 2.1, .2)
    Y = np.arange(0, 2.1, .2)
    X = np.broadcast_to(np.expand_dims(X, axis=1), (len(X), len(X)))
    Y = np.broadcast_to(np.expand_dims(Y, axis=0), (len(Y), len(Y)))
    U = np.multiply(np.cos(X), Y)
    V = np.multiply(np.sin(X), Y)
    vis.quiver(
        X=U,
        Y=V,
        opts=dict(normalize=0.9),
    )

def plotting_mesh(vis):
    x = [0, 0, 1, 1, 0, 0, 1, 1]
    y = [0, 1, 1, 0, 0, 1, 1, 0]
    z = [0, 0, 0, 0, 1, 1, 1, 1]
    X = np.c_[x, y, z]
    i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
    Y = np.c_[i, j, k]
    vis.mesh(X=X, Y=Y, opts=dict(opacity=0.5))

def plotting_dual_axis_lines(vis):
    X = np.arange(20)
    Y1 = np.random.randint(0, 20, 20)
    Y2 = np.random.randint(0, 20, 20)
    vis.dual_axis_lines(X, Y1, Y2)

if __name__ == '__main__':

    vis = visdom.Visdom()




