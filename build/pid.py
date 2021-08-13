#!/usr/bin/env python

import numpy as np


class PID:
    def __init__(self, kp=0.0, ki=0.0, kd=0.0):
       
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

       
        self.PID = 0.0
        self.CTE = []
        self.cte_sum = 0.0

    def Update(self, cte, speed, angle, applied_steer_value, applied_throttle_value):  # TODO: Update PID errors based on cte
        
        self.response_cte = cte
        self.response_speed = speed
        self.response_angle = angle

        self.response_throttle_value = applied_throttle_value
        self.response_steer_value = applied_steer_value

        self.CTE.append(self.response_cte)
        if len(self.CTE) > 15:
            self.CTE.remove(self.CTE[0])
        _sum = np.sum(self.CTE)

        self.PID = - self.Kp * self.response_cte - self.Ki * _sum - self.Kd * (self.response_cte - self.previous_given_cte)

        if self.PID < -1:
            self.PID = -1

        if self.PID > 1:
            self.PID = 1

    def TotalError(self):  # TODO: Calculate and return the total error
        return 0.0
