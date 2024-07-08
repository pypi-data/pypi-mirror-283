import pickle
import os


def save_to_pickle(file_path: str, overwrite=False):
    """
        若函数有返回值，在该函数外层加上该装饰器，则会将函数的返回对象序列化保存到磁盘，下次调用该函数时直接读磁盘的序列化结果
    :param file_path: 需要保存函数返回结果的路径
    :param overwrite: 当置为True时则无论是否已存在保存的结果，重新执行函数体并覆写原有的结果
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if not overwrite and os.path.exists(file_path):  # 已存在保存的副本，直接加载该副本，不会继续执行函数体
                with open(file_path, "rb") as file:
                    func_result = pickle.load(file)
            else:  # 若不存在保存的副本，则调用函数返回结果，并保存返回结果
                func_result = func(*args, **kwargs)
                with open(file_path, "wb") as file:
                    pickle.dump(func_result, file)
            return func_result

        return wrapper

    return decorator


def load_pickle(file_path: str):
    """
        简化pickle读取操作
    """
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except Exception as e:
        print(e)
