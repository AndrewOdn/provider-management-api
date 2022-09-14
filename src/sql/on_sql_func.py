
async def isinstance_list(item, l):
    for object_type in l:
        if isinstance(item, object_type):
            return True
    return False


async def dict_transform(data, object_list):
    for k, v in data.items():
        if await isinstance_list(v, object_list):
            data[k] = v.__dict__
    return data
