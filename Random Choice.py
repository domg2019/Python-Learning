import random


def main():
    # 输入功能：输入一些英语人名作为一个pool
    names_pool = input("请输入一些英语人名，用逗号分隔: ").strip().split(',')

    # 去除名字前后的空格
    names_pool = [name.strip() for name in names_pool if name.strip()]

    # 检查pool是否为空
    if not names_pool:
        print("名字池为空，请至少输入一个名字。")
        return

    # 逐次随机选择名字，直到pool为空
    print("开始随机选择名字：")
    while names_pool:
        # 随机选择一个名字
        selected_name = random.choice(names_pool)
        print(f"随机选择的名字是: {selected_name}")

        # 从pool中移除已选中的名字
        names_pool.remove(selected_name)

    print("名字池已空，所有名字已被选中。")


if __name__ == "__main__":
    main()