'''
@Time    : 2022/5/23 17:32
@Author  : leeguandon@gmail.com
'''
import os
import cv2
import time
import numpy as np
import multiprocessing
from multiprocessing.context import Process
from ..builder import build_render
from loguru import logger

cv2.setNumThreads(1)

STOP_TOKEN = "kill"


def train_data(cfg, dataset):
    multiprocessing.set_start_method('spawn', force=True)
    manager = multiprocessing.Manager()
    data_queue = manager.Queue()

    for generator_cfg in cfg.generator_cfg:
        db_writer_process = DBWriterProcess(
            dataset, data_queue, generator_cfg, cfg)
        db_writer_process.start()

        if cfg.num_processes == 0:  # 单进程
            process_setup(generator_cfg)  # render的初始化，每次初始化不同
            for _ in range(cfg.num_images):
                generate_img(data_queue)
            data_queue.put(STOP_TOKEN)
            db_writer_process.join()
        else:  # 多进程用进程池
            with multiprocessing.Pool(
                    processes=cfg.num_processes,
                    initializer=process_setup,
                    initargs=(generator_cfg,),
            ) as pool:
                for _ in range(cfg.num_images):
                    pool.apply_async(generate_img, args=(data_queue,))

                pool.close()
                pool.join()

            data_queue.put(STOP_TOKEN)
            db_writer_process.join()


def generate_img(data_queue):
    data = render()  # forward过程
    if data is not None:
        data_queue.put({"image": data[0], "label": data[1]})


def process_setup(generator_cfg):
    global render

    # Make sure different process has different random seed
    np.random.seed()

    render = build_render(generator_cfg)  # 类的初始化
    logger.info(f"Finish setup image generate process: {os.getpid()}")


class DBWriterProcess(Process):
    def __init__(
            self,
            dataset,
            data_queue,
            generator_cfg,
            cfg,
            # logger
    ):
        super().__init__()
        self.cfg = cfg
        self.dataset = dataset
        self.data_queue = data_queue
        self.generator_cfg = generator_cfg
        self.log_interval = cfg.log_interval
        # self.logger = logger

    def run(self):
        num_image = self.cfg.num_images
        work_dir = self.cfg.work_dir
        log_interval = max(1, int(self.log_interval / 100 * num_image))
        try:
            with self.dataset as db:
                exist_count = db.read_count()
                count = 0
                logger.info(f"Exist image count in {work_dir}: {exist_count}")
                start = time.time()
                while True:
                    m = self.data_queue.get()
                    if m == STOP_TOKEN:
                        logger.info("DBWriterProcess receive stop token")
                        break

                    name = "{:09d}".format(exist_count + count)
                    db.write(name, m["image"], m["label"])
                    count += 1
                    if count % log_interval == 0:
                        logger.info(
                            f"{(count/num_image)*100:.2f}%({count}/{num_image}) {log_interval/(time.time() - start + 1e-8):.1f} img/s"
                        )
                        start = time.time()
                db.write_count(count + exist_count)
                logger.info(f"{(count / num_image) * 100:.2f}%({count}/{num_image})")
                logger.info(f"Finish generate: {count}. Total: {exist_count+count}")
        except Exception as ee:
            logger.exception("DBWriterProcess error")
            raise ee
