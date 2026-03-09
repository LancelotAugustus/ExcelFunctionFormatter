import subprocess
import sys
import difflib

def run_script(script_path):
    """运行Python脚本并捕获输出"""
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=60
    )
    return result.stdout

def main():
    script1 = r"d:\Develop\ExcelFunctionFormatter\tools\777.py"
    script2 = r"d:\Develop\ExcelFunctionFormatter\tools\666.py"

    print("=" * 60)
    print("运行重构后的代码 (777.py)...")
    output1 = run_script(script1)

    print("运行原始代码 (666.py)...")
    output2 = run_script(script2)

    print("\n" + "=" * 60)
    print("对比结果:")
    print("=" * 60)

    if output1 == output2:
        print("✅ 两个脚本的输出完全一致！")
        return 0

    print("❌ 输出存在差异！\n")

    diff = difflib.unified_diff(
        output2.splitlines(keepends=True),
        output1.splitlines(keepends=True),
        fromfile='666.py (原始)',
        tofile='777.py (重构后)',
        lineterm=''
    )

    diff_content = ''.join(diff)
    if diff_content:
        print(diff_content)
    else:
        lines1 = output1.splitlines()
        lines2 = output2.splitlines()
        print(f"777.py 输出行数: {len(lines1)}")
        print(f"666.py 输出行数: {len(lines2)}")

        for i, (l1, l2) in enumerate(zip(lines1, lines2)):
            if l1 != l2:
                print(f"\n第 {i+1} 行存在差异:")
                print(f"  666.py: {repr(l2)}")
                print(f"  777.py: {repr(l1)}")

        if len(lines1) != len(lines2):
            print(f"\n行数不同: 777.py={len(lines1)}, 666.py={len(lines2)}")

    return 1

if __name__ == '__main__':
    sys.exit(main())
