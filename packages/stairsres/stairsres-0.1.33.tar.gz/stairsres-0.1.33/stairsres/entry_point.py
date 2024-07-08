# from stairs_sdk.sdk.job_context.job import Job
# from stairs_sdk.sdk.job_context.job_context import JobContext
# from stairs_sdk.sdk.models.job_context_models import LLMRequest, TextEmbedderRequest
#
# from pydantic import BaseModel
# from typing import Literal, Dict, List, Union
#
# from res_time_model import ResTimeModel
# from idbadapter import MschmAdapter


# class TimeResultModel(BaseModel):
#     # Возвращает время в днях, необходимое для выполнения работы с определенной ресурсной командой
#     result: int
#
#
# class ResourcesResultModel(BaseModel):
#     # возвращает ресурсную команду для работы с заданным объемом
#     result: Dict[Literal["work_name"],
#                  List[
#                     Dict[Literal["kind", "volume", "min_count", "max_count"], Union[str, int]]
#                  ]
#     ]
#
#
# class MyJobResModel(Job):
#     def run(self, job_id: str, ctx: JobContext, **kwargs):
#         # Извлечение параметров из kwargs, все ваши параметры должны быть переданы в kwargs
#         work_name = kwargs.get("work_name")
#         measurement = kwargs.get("measurement")
#         volume = kwargs.get("volume")
#
#         # Выполнение ваших функций
#         # result1 = my_function1(param1)
#         db_wrapper = MschmAdapter(url="postgresql+psycopg2://testuser:pwd@10.32.15.30:25432/test")
#
#         res_time_model = ResTimeModel(dbwrapper=db_wrapper)
#         res_data = res_time_model.get_resources_volumes(work_name=work_name, work_volume=volume,
#                                                         measurement=measurement)
#
#
#         # Выполнение запроса к LLM
#         result_final: str = ctx.llm_api.inference(LLMRequest(job_id=job_id, text=res_data))
#
#         # Сохранение результата в Redis
#         ctx.result_storage.save_dict(job_id, ResourcesResultModel(result=result_final).dict())
#
# class MyJobTimeModel(Job):
#     def run(self, job_id: str, ctx: JobContext, **kwargs):
#         # Извлечение параметров из kwargs, все ваши параметры должны быть переданы в kwargs
#         work_unit = kwargs.get("work_unit")
#         workers = kwargs.get("workers")
#         measurement = kwargs.get("measurement")
#
#         db_wrapper = MschmAdapter(url="postgresql+psycopg2://testuser:pwd@10.32.15.30:25432/test")
#         res_time_model = ResTimeModel(dbwrapper=db_wrapper)
#
#         time = res_time_model.estimate_time(work_unit=work_unit, worker_list=workers, measurement=measurement,
#                                             mode='0.5')
#
#         # Выполнение запроса к LLM
#         result_final: str = ctx.llm_api.inference(LLMRequest(job_id=job_id, text=time))
#
#         # Сохранение результата в Redis
#         ctx.result_storage.save_dict(job_id, TimeResultModel(result=result_final).dict())