import pyxel
import math
import numpy as np

WINDOW_WIDTH = 120 # 画面の横幅
WINDOW_HEIGHT = 80 # 画面の高さ

NUM_CIRCLE = 5 # 丸の数
NUM_TRIANGLE = 10 # 三角の数

TIMER_COLOR = 12 # タイマーの色(1~15で設定)
SUCCESS_COLOR = 11 # 成功メッセージの色(1~15で設定)
FAILED_COLOR = 8 # 失敗メッセージの色(1~15で設定)

import pyxel
from sched import scheduler

# タイマー関連
class Timer:
    def __init__(self, fps=30):
        self.fps = fps
        self.scheduler = scheduler(self.tick)

    def tick(self):
        return pyxel.frame_count

    def update(self):
        self.scheduler.run(blocking=False)

    def call_later(self, interval, func, priority=1):
        self.scheduler.enter(
            interval*self.fps,
            priority,
            func
        )

    def call_soon(self, func):
        self.call_later(0, func)

    def set_interval(self, interval, func):
        def callback():
            if not func():
                self.call_later(interval, callback)
        self.call_later(interval, callback)

    def start_generator(self, gen):
        def _next():
            interval = next(gen, None)
            if interval is not None:
                self.call_later(interval, _next)
        self.call_soon(_next)

    def show_timer(self, time):
        if time < 10:
            return '00:0' + str(time)
        elif time >= 10:
            return '00:' + str(time)

# 二次元(x座標, y座標)
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 三次元(x座標, y座標, z座標)
class Position3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# 丸
class Circle:
    def __init__(self):
        self.r = pyxel.rndf(3,10) # 半径を3~10の中からランダムに選ぶ

        # x座標とy座標を画面の範囲内の中でランダムに決定
        self.pos = Position(
            pyxel.rndf(self.r, WINDOW_WIDTH - self.r), # x座標
            pyxel.rndf(self.r, WINDOW_HEIGHT - self.r) # y座標
        )

        self.color = pyxel.rndi(1, 15) # 色をランダムに決定

# 三角
class Triangle:
    def __init__(self):
        self.l = pyxel.rndf(10,15) # 1辺の長さを3~10の中からランダムに選ぶ

        # 各頂点のx座標とy座標を画面の範囲内の中でランダムに決定
        # 左下の頂点(基準)
        pos1 = Position(
            pyxel.rndf(0, WINDOW_WIDTH - self.l), # x座標
            pyxel.rndf(self.l * (math.sqrt(3) / 2), WINDOW_HEIGHT) # y座標
        )
        # 右下の頂点
        pos2 = Position(
            pos1.x + self.l, # x座標
            pos1.y # y座標
        )
        # 上の頂点
        pos3 = Position(
            pos1.x + (self.l / 2), # x座標
            pos1.y - (self.l * math.sqrt(3) / 2) # y座標
        )
        self.pos = [pos1, pos2, pos3]

        self.color = pyxel.rndi(1, 15) # 色をランダムに決定

# メイン実行部分
class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH,WINDOW_HEIGHT) # 画面の大きさを決定
        pyxel.mouse(True) # マウスカーソルを有効化

        self.circles = [Circle() for _ in range(NUM_CIRCLE)] # NUM_CIRCLEの数だけ丸を生成
        self.triangles = [Triangle() for _ in range(NUM_TRIANGLE)] # NUM_TRIANGLEの数だけ三角を生成
        self.clear = None

        # タイマー関連
        self.timer = Timer()
        self.timer.call_later(10, self.game_over) # 10秒後にゲームオーバー
        self.time = 0

        def count():
            self.time += 1
            return self.time >= 10 # 10秒経ったかどうかをTrue or Falseで返す
        self.timer.set_interval(1, count)

        # 1秒ずつカウント
        def count_gen():
            for num in range(10):
                self.time = num
                yield 1 # 1秒間隔でカウント
        self.timer.start_generator(count_gen())

        pyxel.run(self.update, self.draw)
    
    # ゲームクリアの場合
    def game_clear(self):
        self.clear = True

    # ゲーム失敗の場合
    def game_over(self):
        self.clear = False

    def update(self):
        # ゲームに成功or失敗したらタイマーを止めるのでupdateしない
        if self.clear == None:
            self.timer.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit() # Qキーを押したら終了
        
        num_circles = len(self.circles) # 丸の数
        num_triangles = len(self.triangles) # 三角の数
        # クリックが行われたときの処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # 丸を押したか一個ずつ確認
            for i in range(num_circles):
                circle = self.circles[i] # i番目の丸
                dx = circle.pos.x - pyxel.mouse_x # クリックした場所のx座標と丸のx座標の差
                dy = circle.pos.y - pyxel.mouse_y # クリックした場所のy座標と丸のy座標の差
                if dx * dx + dy * dy < circle.r * circle.r: # 円の中心からクリックした座標までの距離が半径よりも小さい場合はクリックしたとみなす
                    self.circles.pop(i) # 配列から消す
                    if len(self.circles) == 0:
                        self.game_clear() # 丸がなくなったらゲームクリア
                    return # 一個丸をクリックした時点で処理を終了

            # 三角を押したか確認
            for i in range(num_triangles):
                triangle = self.triangles[i] # i番目の三角形
                start_pos = triangle.pos[2] # ベクトルの始点
                for j in range(3):
                    end_pos = triangle.pos[j] # ベクトルの終点
                    tri_vector = Position3D(end_pos.x - start_pos.x, end_pos.y - start_pos.y, 0) # 三角形の一辺部分を三次元ベクトルにする
                    click_vector = Position3D(pyxel.mouse_x - start_pos.x, pyxel.mouse_y - start_pos.y, 0) # クリックした場所への辺の始点からの三次元ベクトル
                    cross = np.cross(np.array([tri_vector.x, tri_vector.y, tri_vector.z]), np.array([click_vector.x, click_vector.y, click_vector.z])) # 外積
                    if cross[2] > 0: # 外積のz座標がプラスの場合は三角形の外側と判定される
                        break # 一つでも外側にあればクリックしてないと判断して終了
                    if j == 2:
                        self.game_over() # 最後までbreakされなかった場合クリックしたと判定
                        return
                    start_pos = end_pos # ベクトルの始点を移動

    def draw(self):
        pyxel.cls(0) # 背景色を黒に設定

        # 生成された丸をfor文でそれぞれ描画
        for circle in self.circles:
            pyxel.circ(circle.pos.x, circle.pos.y, circle.r, circle.color)

        # 生成された三角をfor文でそれぞれ描画
        for triangle in self.triangles:
            pyxel.tri(triangle.pos[0].x, triangle.pos[0].y, triangle.pos[1].x, triangle.pos[1].y, triangle.pos[2].x, triangle.pos[2].y, triangle.color)

        pyxel.text(0,0,self.timer.show_timer(self.time),TIMER_COLOR) # タイマーを表示
        
        # 丸がひとつもない場合成功
        if self.clear:
            text = "CONGRATULATIONS!!" if self.time <= 5 else "GREAT!" if self.time <= 7 else "GOOD" # 5秒以内それ以上で分ける
            pyxel.text(WINDOW_WIDTH/2 - len(text) * 2, WINDOW_HEIGHT/2, text, SUCCESS_COLOR) # 中心にテキストを表示

        # 失敗の場合
        if self.clear == False:
            pyxel.text(WINDOW_WIDTH/2 - 4 * 4, WINDOW_HEIGHT/2, "FAILED!!", FAILED_COLOR) # 中心にテキストを表示

App()