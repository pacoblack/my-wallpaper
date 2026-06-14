import os
import json

# ============================ 核心配置区域 ============================
# 1. 严格继承您原本的绝对路径配置，可以随时修改它
# 2. 如果视频在其他盘符，先执行 mklink /d "D:/recycler-paper/c_videos" "C:/你的视频文件夹路径/"
TARGET_DIR = "D:/recycler-paper/c_videos/"

# 2. 升级为视频专属格式支持后缀
SUPPORTED_FORMATS = ('.mp4', '.webkitmp4', '.webm', '.ogg', '.mov', '.avi', '.mkv', '.wmv')
# =====================================================================

def generate_video_list():
    # 统一输出视频专属的数据库文件名
    output_file = "videos.js"
    
    if not os.path.exists(TARGET_DIR):
        print(f"❌ 错误：你配置的视频目录不存在！路径为: {TARGET_DIR}")
        os.system("pause")
        return
        
    print(f"🔍 正在扫描目标视频目录: {TARGET_DIR} ...")
    
    final_paths = []

    try:
        # 升级为 os.walk，实现对指定目录及其所有子文件夹的深度自动化、无死角扫描
        for root, dirs, files in os.walk(TARGET_DIR):
            for file in files:
                # 过滤隐藏文件，且后缀必须符合视频格式
                if not file.startswith('.') and file.lower().endswith(SUPPORTED_FORMATS):
                    # 获取该视频的绝对物理全路径
                    full_path = os.path.join(root, file)
                    
                    # 👈 核心兼容对齐：严格延续您之前的路径拼接逻辑，转换为对前端最友好的斜杠
                    web_path = full_path.replace("\\", "/")
                    
                    final_paths.append({
                        "name": file, 
                        "path": web_path
                    })
                    print(f"  [发现视频] -> {file}")
                        
    except Exception as e:
        print(f"❌ 扫描过程中发生未知错误: {e}")
        os.system("pause")
        return

    # 3. 将变量名更替为视频专属的全局静态数组变量名
    js_content = "/* 此文件由 python 脚本自动生成，请勿手动修改 */\n\n"
    js_content += f"const ALL_VIDEO_DATA = {json.dumps(final_paths, ensure_ascii=False, indent=4)};\n"

    # 4. 写入根目录下的 videos.js 文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"\n✨ 成功更新 {output_file} 文件！")
    print(f"🚀 统共识别并载入了 {len(final_paths)} 个视频，快去刷新网页试试吧！")

if __name__ == "__main__":
    generate_video_list()
