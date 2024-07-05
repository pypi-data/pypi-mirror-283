import extruct


def 网页协议_响应文本_提取JSON_LD(响应文本):
    """
    提取 HTTP 响应文本中的 json-LD 数据，并返回一个包含所有 json-LD 数据的列表。

    参数:
        - 响应文本 (str): 服务器响应的文本内容。

    返回值:
        - 包含所有 json-LD 数据的列表。如果提取过程中出现异常，则返回空列表。
    """
    try:
        # 使用 extruct 提取嵌入的数据
        data = extruct.extract(响应文本)

        # 提取所有的 json-LD 数据并添加到列表中
        json列表 = data.get('json-ld', [])
        return json列表
    except Exception:
        return []
