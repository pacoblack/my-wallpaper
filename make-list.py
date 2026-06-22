import os
import json
import random 

# ==================== 🛠️ 路径与配置自定义区域 ====================
# 重要提示：由于浏览器的安全限制，如果你的 HTML 文件在 D 盘，
# 这里的 TARGET_DIR 文件夹【必须】也在 D 盘（不能跨盘符，例如 HTML 在 C 盘而图片在 D 盘是不行的）。
# 建议直接使用默认的 "images" 相对路径，或者跟 HTML 在同个盘符下的路径。

# 在这里填写你想要扫描的【绝对路径】或【相对路径】（注意：Windows 路径中的 \ 要换成 /）
# 示例 1 (读取外部任意文件夹): TARGET_DIR = "D:/Pictures/MyWallpapers"
# 示例 2 (读取默认自带文件夹): TARGET_DIR = "images"
TARGET_DIR = "D:/recycler-paper/逼纸/林希威-白模特"

# 支持的图片格式后缀
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp')
# ===============================================================

def generate_image_list():
    output_file = "images.js"
    
    if not os.path.exists(TARGET_DIR):
        print(f"❌ 错误：你配置的目录不存在！路径为: {TARGET_DIR}")
        os.system("pause")
        return
        
    print(f"🔍 正在扫描目标目录: {TARGET_DIR} ...")
    
    final_paths = []

    try:
        # 1. 扫描目标目录顶层的图片文件
        for item in os.listdir(TARGET_DIR):
            item_path = os.path.join(TARGET_DIR, item)
            
            if os.path.isfile(item_path) and item.lower().endswith(SUPPORTED_FORMATS):
                # 统一斜杠为 /，直接生成对前端最友好的相对路径
                web_path = f"{TARGET_DIR}/{item}".replace("\\", "/")
                final_paths.append({"name": item, "path": web_path})
            
            # 2. 如果检测到子文件夹，深入扫描内部的图片
            elif os.path.isdir(item_path):
                for sub_item in os.listdir(item_path):
                    sub_item_path = os.path.join(item_path, sub_item)
                    if os.path.isfile(sub_item_path) and sub_item.lower().endswith(SUPPORTED_FORMATS):
                        web_path = f"{TARGET_DIR}/{item}/{sub_item}".replace("\\", "/")
                        final_paths.append({"name": sub_item, "path": web_path})
                        
    except Exception as e:
        print(f"❌ 扫描过程中发生未知错误: {e}")
        os.system("pause")
        return

    # 随机打乱图片顺序，实现随机播放
    random.shuffle(final_paths)

    # 3. 直接输出一个扁平化的纯净数组给前端
    js_content = "/* 此文件由 python 脚本自动生成，请勿手动修改 */\n\n"
    js_content += f"const ALL_IMAGE_DATA = {json.dumps(final_paths, ensure_ascii=False, indent=4)};\n"

    # 4. 写入根目录下的 images.js 文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"\n✨ 成功更新 images.js 文件！")
    print(f"🚀 统共识别并载入了 {len(final_paths)} 张图片，快去刷新网页试试吧！")

if __name__ == "__main__":
    generate_image_list()
