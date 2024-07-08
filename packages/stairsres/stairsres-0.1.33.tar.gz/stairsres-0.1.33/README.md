# Module with time models and resource staff models

___

**!NB: Measurement for resources is not considered here.**

This module contains two main methods:

1. get_resources_volumes

        Input: 
        1. work_name, 
        2. work_volume, 
        3. measurement, 
        4. shift
         
       Returns: {'worker_reqs': [{'kind': 'Геодезист',
                                 'volume': 3,
                                 'min_count': 1,
                                 'max_count': 5}, <...>]}
2. estimate_time

        Input: 
        1. work_unit ({"name": work_name, "volume": work_volume})
        2. worker_list ([{'name': res_name, '_count': amount}]
        3. measurement
       Returns: int (number of calculated shifts)