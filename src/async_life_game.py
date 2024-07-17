import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt

class AsyncLifeGame:
    def __init__(self, size, cnt_states, probabilities, async_p):
        self.size = size # 一辺のセル数
        self.cnt_states = cnt_states # 各セルの状態数
        self.probabilities = probabilities # 初期状態における各状態の発生確率
        self.async_p = async_p # 非同期確率変数
        self.current_state = self._initialize_automaton(size, cnt_states, probabilities) # 現在の世代情報
        self.state_list = []

    def _is_frozen(self):
        """全体が周期性、つまり凍結相になったか確認する"""
        current_state = self.current_state.copy()
        self.state_list.append(current_state)

        # リストの長さが2未満の場合は比較する必要がない
        if len(self.state_list) < 2:
            return False

        # フロイドの循環検出アルゴリズム
        slow_ptr = 0
        fast_ptr = 1

        while fast_ptr < len(self.state_list):
            if np.array_equal(self.state_list[slow_ptr], self.state_list[fast_ptr]):
                return True
            slow_ptr += 1
            fast_ptr += 2

        # 最大max_statesの状態を保持
        max_states = 5
        if len(self.state_list) > max_states:
            self.state_list.pop(0)

        return False

    def _initialize_automaton(self, size, cnt_state, probabilities):
        """セルオートマトンの初期状態をランダムに生成"""
        assert sum(probabilities) == 1, "Probabilities must sum to 1"
        assert len(probabilities) == cnt_state, "Length of probabilities must match cnt_state"
        return np.random.choice(cnt_state, size=(size, size), p=probabilities)

    def _update_generation(self):
        """次の世代の状態を計算し、確率的に変化させる"""
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])
        neighbor_count = convolve(self.current_state, kernel, mode='wrap', cval=0)
        new_state = ((neighbor_count == 3) | ((self.current_state == 1) & (neighbor_count == 2))).astype(int)
        random_values = np.random.rand(*self.current_state.shape)
        no_change_mask = random_values <= self.async_p
        new_state[no_change_mask] = self.current_state[no_change_mask]
        self.current_state = new_state

    def _run_plot(self, max_t, from_showing_graph=0):
        """実行関数"""
        plt.ion()
        fig, ax = plt.subplots()
        img = ax.imshow(self.current_state)
        plt.show()
        is_frozen = False
        for t in range(max_t):
            self._update_generation()
            img.set_data(self.current_state)
            ax.set_title(f"Async probability: {self.async_p}, Step: {t}")
            is_frozen = self._is_frozen()
            print(f"\r current: {t+1}, Frozen: {is_frozen}", end="")
            if is_frozen:
                break
            if t > from_showing_graph:
                plt.draw()
                plt.pause(0.01)
        print("")
        plt.ioff()
        plt.close()
        return is_frozen, t

    def _execute_plot(self, max_t, from_showing_graph):
        print(f"execute_plot, グリッドサイズ: {self.size}, 世代交代数: {max_t}, 状態数: {self.cnt_states}, 発生確率: {self.probabilities}, 非同期確率(維持): {self.async_p}")
        _is_frozen, t = self._run_plot(max_t, from_showing_graph)
        return _is_frozen, t
    
def main():
    size = 150
    max_t = 10000
    cnt_states = 2
    probabilities = [0.5, 0.5]
    from_showing_graph = 9000
    async_p = 0.085

    game = AsyncLifeGame(size, cnt_states, probabilities, async_p)
    _is_frozen, t = game._execute_plot(max_t, from_showing_graph)
    print(f"is_frozen: {_is_frozen}")

if __name__ == "__main__":
    main()

