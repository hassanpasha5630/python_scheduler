#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 06:17:31 2020

@author: hassanpasha
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 21:39:32 2020

@author: hassanpasha
"""


class scheduler: 
    
    def __init__(self):
        self.schedule = [] #over all list to be accesssed for schedule 
        self.client_facing_result = [] # over all list for merge re

    # give the user the option to add item to his list 
    '''
    We will be working with military time 
    
    '''
    def add_time_to_scheduler(self,start_time,end_time):
        
        self.schedule.append((start_time,end_time))
        if start_time > end_time:
            return "Error: 400 start time is greater than end time"
        if start_time > 24 or end_time > 24:
            return "Error: 401 military time can not accede 24"
        '''
        (1,1) || (x,x) start time and end time can not be same as it does not 
        have enought gap inbetween to be scheduled  
        
        '''
        if start_time == end_time :
            return "Error: 300 time lasp to short to be scheduled"
            
        return "Schedule Updated", self.schedule
    
    #give the user the ablity to add a group of time slots 
    def mass_update(self,time_list:list,over_ride_bool:bool):
        '''
        check to see if the user entered a time larger than 24
        list(sum(time_list, ())):) --> convert list of tuples to a list 
         sort by greatest - least and check if list[0] > 24
        '''    
        sorted_list = list(sum(time_list,()))
        sorted_list.sort(reverse=True)
        if sorted_list[0] > 24 :
            return "Error: 401 military time can not accede 24"
        
        if over_ride_bool == False:
            self.schedule = time_list + self.schedule
            return self.schedule
        else : 
            self.schedule = time_list
            return self.schedule
            
    
    def over_lap(self,t1,t2):
        
     
        t1_start,t1_end = t1[0],t1[1]
        t2_start,t2_end = t2[0],t2[1]
    
        if  t1_end >= t2_start:
            return True 
        else : 
            return False 
        
    
    
    # merge all the time in the scheduler in an easy to read time slot  
    
    '''
    to create own merge result from a list of given times 
    
    sort_list : if passed will run the merge on the given list 
    result : if passed will return result to the given list 
    
    If none arguments are passed function will automatically run from the 
    data in __init__ function 
    '''
    
    def client_facing_calendar(self,sort_list=None,result_list=None):
        if sort_list == None:
            
            sort_list = sorted(set(self.schedule), key=lambda x: x[0])   
        else : 
            sort_list = sorted(set(sort_list), key=lambda x: x[0]) 

        for index in range(0,len(sort_list)):            
            if index+1 >= len(sort_list):
                if result_list == None :
                    self.client_facing_result = sort_list         
                    return  self.client_facing_result
                else :
                    result_list.extend(sort_list)
                    return result_list 
                
            over_lap_result = self.over_lap(sort_list[index],sort_list[index+1])
            print(sort_list,over_lap_result)
            if over_lap_result == True:
                if sort_list[index+1][1] > sort_list[index][1]:
                    result = (sort_list[index][0],sort_list[index+1][1])
                else :
                    result = (sort_list[index][0],sort_list[index][1])
                #Once the the items have been checked pop from list 
                sort_list.pop(index)
                sort_list.pop(index)
                #insert result to top of the list 
                sort_list.insert(0,result)
                # call function on the new list
                if result == None :
                    return self.client_facing_calendar(sort_list)
                else :
                    return self.client_facing_calendar(sort_list,result_list)
            
    
        
    
    def update_schedule(self,previous_schedule,non_availability):
        previous_schedule = self.client_facing_calendar(previous_schedule) 
        non_availability = self.client_facing_calendar(non_availability) 
        #temp data strcture so we can back track the schedule
        temp_data = [] 
        # new list of times 
        new_list = []
        # boolean function to keep track of history
        history_checked = False
        for pre_index in previous_schedule: #(N)
            for non_avail_counter,non_avail_index in enumerate(non_availability) : # N 
                print(pre_index,non_avail_index)
                #temp sorting the data coming in to that combine into a list and sort as needed
                temp_sort = [pre_index,non_avail_index]
                temp_sort = sorted(set(temp_sort), key=lambda x: x[0])   
                print('temp_sort -->',temp_sort)
                # We want to check if the times are overlapping 
                if self.over_lap(temp_sort[0],temp_sort[1]) == True:
                    # Treating this is a minor memory to keep track of the previously updated time
                    if len(temp_data) > 0 :     
                        for index,temp_index in enumerate(temp_data) :# N
                            print('in_temp -->',temp_index,non_avail_index)
                            if self.over_lap(temp_index,non_avail_index) == True:
                                history_checked = True
                                print('temp_data',temp_data)
                                new_value = ((min(temp_index[0],non_avail_index[0]),max(temp_index[0],non_avail_index[0])))
                                temp_data.pop(index)
                                new_list.append(new_value)
                                print('temp_data',temp_data)
                                print('new_list',new_list)
                                if temp_index[1] > non_avail_index[1]:
                                    new_value = ((min(pre_index[1],non_avail_index[1]),max(pre_index[1],non_avail_index[1])))                                    
                                    new_list.append(new_value)
                                    print('temp_data2',temp_data)
                                    print('new_list2',new_list)
                    # to avoid repeative inserts in data                 
                    if history_checked == False:
                        if  pre_index[0] < non_avail_index[0]:
                            new_time = (min(pre_index[0],non_avail_index[0]),max(pre_index[0],non_avail_index[0]))
                            temp_data.append(new_time)
                            #check to see if we should contiune 
                        if pre_index[1] > non_avail_index[1]:
                            new_time = (min(pre_index[1],non_avail_index[1]),max(pre_index[1],non_avail_index[1]))
                            temp_data.append(new_time)                               
                    print('True')
                    print(temp_data)
                else:
                    print('False')
            
        return sorted(set(new_list+temp_data), key=lambda x: x[0])
        
        
        


#########
Test_Case_1 =  {
                
                "old_schedule"  : [(0, 7)],
                "not_available" : [(2,3), (4,5)],
                "true_result"   : [(0, 2), (3, 4), (5,7)],
              }

Test_Case_2 = {
                "old_schedule"  : [(1,3),(2,5),(0, 5),(10,15),(1,7),(1, 7),(9,10),(1,2)],
                "not_available" : [(1,3),(2,6),(8,10),(15,18)],
                "true_result"   : [(0, 1), (6, 7), (10,15)],
              } 

Test_Case_3 = {
                "old_schedule"  : [(1, 7), (0, 5), (10, 15)], 
                "not_available" : [(2,3), (13, 20), (18, 22)],
                "true_result"   : [(0, 2), (3,7), (10, 13)],
              } 
        
     
            

doc_1 = scheduler()
 
doc_1.client_facing_calendar(Test_Case_2["not_available"])

assert doc_1.update_schedule(Test_Case_1['old_schedule'],Test_Case_1['not_available']) == Test_Case_1["true_result"] 
assert doc_1.update_schedule(Test_Case_2['old_schedule'],Test_Case_2['not_available']) == Test_Case_2["true_result"] 
assert doc_1.update_schedule(Test_Case_3['old_schedule'],Test_Case_3['not_available']) == Test_Case_3["true_result"] 
                
        
    