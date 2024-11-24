import urllib.request
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 基础URL
base_url = "test.com"
query = "?test=1"

# 下载的片段总数
total_segments = 1

# 最大重试次数
max_retries = 10

# 输出目录
output_dir = "./downloads/"
failed_segments = []

# 线程池的最大线程数
max_threads = 10

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 下载函数
def download_segment(segment):
    """下载单个视频片段"""
    filename = f"{segment:05d}.mp4"  # 格式化文件名为4位
    url = f"{base_url}{segment}.mp4{query}"
    output_file = os.path.join(output_dir, filename)
    retries = 0

    while retries < max_retries:
        try:
            # 下载文件
            urllib.request.urlretrieve(url, output_file)
            return True
        except Exception as e:
            print(f"Error for segment {filename}: {e}, retrying...")
            retries += 1
            time.sleep(2)  # 等待2秒再重试
    return False

# 主函数
def main():
    # 使用多线程池下载
    with ThreadPoolExecutor(max_threads) as executor:
        # 提交任务
        future_to_segment = {executor.submit(download_segment, segment): segment for segment in range(0, total_segments)}
        for future in as_completed(future_to_segment):
            segment = future_to_segment[future]
            try:
                if not future.result():  # 下载失败
                    failed_segments.append(segment)
            except Exception as e:
                print(f"Unhandled error for segment {segment:04d}: {e}")
                failed_segments.append(segment)

    # 打印所有失败的片段
    if failed_segments:
        print([f"{seg:05d}" for seg in failed_segments])
    else:
        print("\nAll segments downloaded successfully.")

if __name__ == "__main__":
    main()
