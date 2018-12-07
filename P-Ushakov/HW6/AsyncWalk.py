import asyncio
import os


async def async_tuple(path=""):
    try:
        ld = os.listdir(path)
    except PermissionError:
        ld = ()
    d = tuple(x for x in ld if os.path.isdir(os.path.join(path, x)))
    f = tuple(x for x in ld if os.path.isfile(os.path.join(path, x)))
    return path, d, f


def form_list_dirs(walk_tuple):
    n_p, n_d, n_f = walk_tuple
    return tuple(map(lambda x: os.path.join(n_p, x), n_d))


def task_list(dirs):
    tasks = []
    for d in dirs:
        t = asyncio.create_task(async_tuple(d))
        tasks.append(t)
    return tasks


async def root_dirs(path):
    at = await async_tuple(path)
    dirs = form_list_dirs(at)
    return dirs


async def walk_step_tasks(dirs):
    tasks = task_list(dirs)
    await asyncio.sleep(0)
    for finished_tasks in asyncio.as_completed(tasks):
        yield finished_tasks


async def walk_step(dirs):
    a_w = walk_step_tasks(dirs)
    async for finished_task in a_w:
        walk_tuple = await finished_task
        yield walk_tuple


async def async_walk(path):
    dirs = list(await root_dirs(path))
    tuple_list = []
    while dirs:
        w_s = walk_step(dirs)
        async for walk_tuple in w_s:
            used_path, d, f = walk_tuple
            n_dirs = form_list_dirs(walk_tuple)
            dirs.remove(used_path)
            dirs.extend(n_dirs)
            tuple_list.append(walk_tuple)
    return tuple_list


def awalk(path):
    tuple_list = asyncio.run(async_walk(path))
    for tpl in tuple_list:
        yield (tpl)


if __name__ == '__main__':
    awalk()
