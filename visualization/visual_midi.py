import pretty_midi
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 第二步：核心可视化函数 ---
def plot_piano_roll(midi_file, start_pitch=0, end_pitch=127, fs=100):
    """
    midi_file: MIDI文件路径
    start_pitch: 显示的最低音高 (默认为0)
    end_pitch: 显示的最高音高 (默认为127)
    fs: 采样频率 (决定时间轴的精度，100表示每秒100个采样点)
    """
    # 1. 加载 MIDI 文件
    try:
        pm = pretty_midi.PrettyMIDI(midi_file)
    except Exception as e:
        print(f"无法加载文件: {e}")
        return

    # 2. 获取钢琴卷帘矩阵
    # get_piano_roll 返回一个 (128, time_steps) 的 numpy 数组
    piano_roll = pm.get_piano_roll(fs=fs)

    # 3. 裁剪音高范围 (可选，为了让图更好看，去掉空白的低音和高音区)
    # MIDI 音高范围通常是 0-127，但钢琴通常在 21(A0) 到 108(C8) 之间
    piano_roll = piano_roll[start_pitch:end_pitch, :]

    # 4. 绘图
    plt.figure(figsize=(12, 4.5),dpi=320)
    
    # 使用 imshow 绘制热力图
    # aspect='auto' 自动调整长宽比
    # origin='lower' 让低音在底部 (符合直觉)
    # cmap='magma' / 'inferno' / 'viridis' 是比较好看的配色
    plt.imshow(piano_roll, aspect='auto', origin='lower', cmap='magma',
               extent=[0, pm.get_end_time(), start_pitch, end_pitch])

    plt.title(f'Piano Roll: {midi_file}')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Pitch (MIDI Note Number)')
    plt.colorbar(label='Velocity')
    plt.tight_layout()
    plt.savefig('visual_gen.png',dpi=320)
    plt.show()

# --- 主程序执行 ---
if __name__ == "__main__":
    # 1. 生成测试文件 (或者替换为你自己的 .mid 文件路径)
    midi_filename = '../generated/gen.mid'
    
    # 2. 可视化
    # 我们限制显示范围从 40 到 90，这样看的更清楚
    plot_piano_roll(midi_filename, start_pitch=40, end_pitch=90)