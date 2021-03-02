from datetime import datetime
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--token', type=str, default=None)
    args = parser.parse_args()
    print("用户信息：", args)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
