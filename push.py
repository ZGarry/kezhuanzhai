def get_date_str():
    from datetime import datetime
    now = datetime.now()
    date_string = f"{now.year}-{now.month:02d}-{now.day:02d}"
    return date_string

def quickPush():
    # 移动到当前目录
    import os
    current_file = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file)
    os.chdir(current_directory)

    # 获取当前仓库&提交代码
    import git
    repo = git.Repo('.')
    repo.git.add('--all')
    # repo.git.commit('-m', get_date_str())
    repo.git.commit('-m', 'Automatic commit')

    # 推送到远程仓库的main分支(github默认main，其他工具可能不同)
    origin = repo.remote(name='origin')
    origin.push('master')


if __name__ == "__main__":
    quickPush()
