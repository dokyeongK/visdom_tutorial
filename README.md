# visdom_tutorial
basic visdom function summary 

😇 [Visdom](https://github.com/fossasia/visdom) 정리 Repository 😇 

위 repo에 있는 visdom function들이 각각 어떤 plot을 그리는지 정리해보고자 함. `exam.py` 에서 조금 더 구체적인 주석 달려있음. (+ option들은 추가 예정.)

👉 사용해보면서 추가적으로 필요한 visdom function들은 업데이트 할 예정!

### Overview

Visdom은 데이터의 시각화를 위한 도구. 해당 코드들은 `Ubuntu 18.04` & `python 3.6` 환경에서 실행.

### visdom setup

```bash
# install using pip
$ pip install visdom

# install using Anaconda
$ conda install -c conda-forge visdom

#conda 가상환경 사용시
$ conda activate "가상환경이름"

$ pip install visdom
#or
$ conda install -c conda-forge visdom
```

### visdom server start

```bash
$ visdom # or python -m visdom.server

# http://localhost:8097/ 👉 브라우저에서 열기
```

👉브라우저에서 아래와 같은 창이 뜨면 설치 성공.

<p align="center"><img src = "https://user-images.githubusercontent.com/28749482/108316418-3a620180-7200-11eb-9174-c24b2a32b9e8.png" width="500">

### How to use visdom (Python)

- **Windows**

Visdom UI에는 **plot, image, text**를 띄울 수 있으며, **drag, drop, resize, destroy**가 가능한 창에 띄워진다. 창은 `envs` 에 있으며, `envs` 의 상태는 session 전체에 저장되고, 창에 있는 것을 다운로드 할 수 있다. (ex, 띄워진 plots을 이미지로 저장 가능)

> The UI begins as a blank slate – you can populate it with plots, images, and text. These appear in windows that you can drag, drop, resize, and destroy. The windows live in envs and the state of envs is stored across sessions. You can download the content of windows – including your plots in svg.

- **Environments**

<p align="center"><img src = "https://user-images.githubusercontent.com/28749482/108316821-c2e0a200-7200-11eb-961f-7ada9fc1f556.png" width="700">

Environment를 이용하여 공간(창)을 분리할 수 있다. (default : main) [http://localhost:8097/env/main](http://localhost:8097/env/main) 이와 같은 링크로 접속하거나 토글로 이동이 가능하다. 예를 들어, 다른 종류의 data를 한 창에 띄우고 싶지 않을 때 envs를 다르게 해 주어 띄우면 됨.

- **State**

<p align="center"><img src = "https://user-images.githubusercontent.com/28749482/108316827-c411cf00-7200-11eb-84cf-348a3fbf1794.png" width="700">


Environment 옆의 폴더 버튼을 누르고, `save` 를 누르면 환경 저장이 가능하다. `Fork` 를 누르면 새로운 env 생성이 가능하다. 

- **View & Filters**

<p align="center"><img src = "https://user-images.githubusercontent.com/28749482/108316830-c542fc00-7200-11eb-9f56-b3ec874505f3.png" width="700">

각 창들을 드래그하여 관리할 수도 있고, `view` 의 폴더 버튼을 눌러 창을 관리할 수도 있다. 뷰를 저장하면 envs에서 모든 창의 위치와 크기가 유지됨. 또한 `filter` 를 사용하면 envs에 있는 창 중에서 보고 싶은 창만 볼 수 있음.

- **Start**

```python
# visdom 시작 방법
import visdom
vis = visdom.Visdom()

# ------------------------------------
# 아래와 같이 Arg Option 줄 수도 있음. (자세한 argments 정보는 https://github.com/fossasia/visdom#visdom-arguments-python-only)
# ------------------------------------

DEFAULT_PORT = 8097
    DEFAULT_HOSTNAME = "http://localhost"
    parser = argparse.ArgumentParser(description='Demo arguments')
    parser.add_argument('-port', metavar='port', type=int, default=DEFAULT_PORT,
                        help='port the visdom server is running on.')
    parser.add_argument('-server', metavar='server', type=str,
                        default=DEFAULT_HOSTNAME,
                        help='Server address of the target to run the demo on.')
    parser.add_argument('-base_url', metavar='base_url', type=str,
                    default='/',
                    help='Base Url.')
    parser.add_argument('-username', metavar='username', type=str,
                    default='',
                    help='username.')
    parser.add_argument('-password', metavar='password', type=str,
                    default='',
                    help='password.')
    parser.add_argument('-use_incoming_socket', metavar='use_incoming_socket', type=bool,
                    default=True,
                    help='use_incoming_socket.')
    FLAGS = parser.parse_args()

    vis = visdom.Visdom(port=FLAGS.port, server=FLAGS.server, base_url=FLAGS.base_url, username=FLAGS.username, password=FLAGS.password, \
                use_incoming_socket=FLAGS.use_incoming_socket)
```

- **Basics**

아래의 function들은 visdom에서 제공하는 기본적인 visualization function들이다.

1) `vis.text` : text를 visdom 창에 띄움.

```python
import visdom

vis = visdom.Visdom()
textwindow = vis.text('Hello World!')
```

2) `vis.image` : CXHXW의 img를 visdom 창에 띄운다. ( 여러개 : `vis.images`)

```python
import visdom

vis = visdom.Visdom()
# 512 X 256 임의의 데이터가 있는 이미지 Example
vis.image(np.random.rand(3, 512, 256))
# 5개의 512 X 256 임의의 데이터가 있는 이미지들 Example
vis.images(np.random.rand(5, 3, 512, 256))
```

3) `vis.matplot` : Matplotlib plot을 visdom 창에 그려준다.

```python
import visdom
import matplotlib.pyplot as plt

vis = visdom.Visdom()
plt.plot([1, 23, 2, 4])
plt.ylabel('some numbers')
vis.matplot(plt)
```

- **Plotting**

visdom은 기본 visualization을 쉽게 만들 수 있는 plot 유형을 제공. (이러한 visualization은 [Plotly](https://plotly.com/) 에서 제공.)

1) `vis.scatter` : 2D나 3D의 scatter plot을 그려줌.

```python
import visdom
vis = visdom.Visdom()Y = np.random.rand(100)
# 2D scatter 예시
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
# 3D scatter 예시
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

# 📌 커스터마이징 & text labels & legend 넣기 등은 exam.py 참고!
```

2) `vis.line` : plot에 line을 그려줌.

```python
# X, Y 값에 맞는 선을 그림.
import visdom
vis = visdom.Visdom()

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
webgl_x = np.linspace(-1, 0,
webgl_y = webgl_x ** 3      
vis.line(X=webgl_x, Y=webgl_
       opts=dict(title='{}
       win="WebGL demo")

# line update Example. WebGL 창에 업데이트하기.
vis.line(
    X=webgl_x + 1.,
    Y=(webgl_x + 1.) ** 3,
    win="WebGL demo", # -> 해당 이름을 가진 win에 업데이트.
    update='append',
    opts=dict(title='{} points using WebGL'.format(webgl_num_points * 2), webgl=True)
)

# 📌 커스터마이징 & area & legend 넣기 등은 exam.py 참고!
```

3) `vis.stem` : stem plot을 그려줌.

```python
import visdom
vis = visdom.Visdom()

Y = np.linspace(0, 2 * math.pi, 70)
    X = np.column_stack((np.sin(Y), np.cos(Y)))
    vis.stem(
        X=X,
        Y=Y,
        opts=dict(legend=['Sine', 'Cosine'])
    )
```

4) `vis.heatmap` : heatmap plot 그려줌.

```python
import visdom
vis = visdom.Visdom()
vis.heatmap(
        X=np.outer(np.arange(1, 6), np.arange(1, 11)),
        opts=dict(
            columnnames=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
            rownames=['y1', 'y2', 'y3', 'y4', 'y5'],
            colormap='Electric',
        )
    )
```

5) `[vis.bar](http://vis.bar)` : bar 모양의 plot 그려줌.

```python
import visdom
vis = visdom.Visdom()

vis.bar(X=np.random.rand(20))
    vis.bar(
        X=np.abs(np.random.rand(5, 3)),
        opts=dict(
            stacked=True,
            legend=['Facebook', 'Google', 'Twitter'],
            rownames=['2012', '2013', '2014', '2015', '2016']
        )
    )

vis.bar(
    X=np.random.rand(20, 3),
    opts=dict(
        stacked=False,
        legend=['The Netherlands', 'France', 'United States']
    )
)
```

6) `vis.histogram` : historgram 모양 plot 그려줌.

```python
import visdom
vis=visdom.Visdom()
vis.histogram(X=np.random.rand(10000), opts=dict(numbins=50)) # numbins : bin 갯수 벡터.
```

7) `vis.boxplot` : box 모양의 plot 그려줌.

```python
import visdom
vis = visdom.Visdom()

X = np.random.rand(100, 2)
    X[:, 1] += 2
    vis.boxplot(
        X=X,
        opts=dict(legend=['Men', 'Women'])
    )
```

8) `vis.surf` : surface plots 그려줌.

```python
import visdom
vis = visdom.Visdom()

x = np.tile(np.arange(1, 101), (100, 1))
y = x.transpose()
X = np.exp((((x - 50) ** 2) + ((y - 50) ** 2)) / -(20.0 ** 2))

vis.surf(X=X, opts=dict(colormap='Hot'))
```

9) `vis.contour` : contour plot 그려줌.

```python
import visdom
vis = visdom.Visdom()
x = np.tile(np.arange(1, 101), (100, 1))
y = x.transpose()
X = np.exp((((x - 50) ** 2) + ((y - 50) ** 2)) / -(20.0 ** 2))

vis.contour(X=X, opts=dict(colormap='Viridis'))
```

10) `vis.quiver` : quiver plot 그려줌.

```python
import visdom
vis = visdom.Visdom()
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
```

11) `vis.mesh` : mesh 형태의 surface 그려줌.

```python
import visdom
vis = visdom.Visdom()
x = [0, 0, 1, 1, 0, 0, 1, 1]
y = [0, 1, 1, 0, 0, 1, 1, 0]
z = [0, 0, 0, 0, 1, 1, 1, 1]
X = np.c_[x, y, z]
i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]
Y = np.c_[i, j, k]
vis.mesh(X=X, Y=Y, opts=dict(opacity=0.5))
```
