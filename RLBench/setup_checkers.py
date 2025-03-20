from typing import List
import numpy as np
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from rlbench.backend.task import Task
from rlbench.backend.conditions import DetectedCondition, NothingGrasped

MAX_CHECKERS_TO_SETUP = 3


class SetupCheckers(Task):

    def init_task(self) -> None:
        self.checkers_placed = -1
        self.checkers = [Shape('checker%d' % i)
                         for i in range(24)]

        self.chess_board = Shape('chess_board_base')

        self.checkers_starting_pos_list = [
            checker.get_position(self.chess_board) for checker in self.checkers]
        self.checkers_starting_orientation = \
            self.checkers[0].get_orientation(self.chess_board)

        self.register_graspable_objects(self.checkers)
        self.success_detectors = [ProximitySensor('detector%d' % i)
                                  for i in range(24)]
        self.success_conditions = [NothingGrasped(self.robot.gripper)]
        for i in range(len(self.checkers)):
            self.success_conditions.append(
                DetectedCondition(self.checkers[i], self.success_detectors[i]))

        self.register_success_conditions(self.success_conditions)
        self.cleanup()

    def init_episode(self, index: int) -> List[str]:
        self.cleanup()

        # CHANGED 1 -> 24
        
        self.checkers_to_setup = 3 + index % MAX_CHECKERS_TO_SETUP

        # Use to showcase episode variations while rlbench backend gets fixed:

        self.register_waypoint_ability_start(0, self._move_above_next_target)
        self.register_waypoints_should_repeat(self._repeat)

        target_checkers_unordered = np.random.choice(self.checkers,
                                                     self.checkers_to_setup,
                                                     replace=False)
        self.target_indexes = []
        self.target_checkers = []
        for checker in self.checkers:
            if checker in target_checkers_unordered:
                self.target_checkers.append(checker)

        self.target_pos_list = []

        # ADDED
        self.checkers_setup = [False] * self.checkers_to_setup

        pos_delta = 0.045
        start_pos_list = [+0.0070816, +0.31868, -0.094908]

        for i, checker in enumerate(self.checkers):
            if checker in self.target_checkers:
                self.target_indexes.append(i)
                # CHANGED (original code did = which is obviously wrong)
                self.target_pos_list.append(checker.get_position())
                checker.set_position(start_pos_list,
                                     relative_to=self.chess_board,
                                     reset_dynamics=False)
                start_pos_list[2] += pos_delta

        if self.checkers_to_setup == 1:
            rtn = ['place the remaining checker '
                   'in its initial position on the board']
        else:
            rtn = ['place the %d remaining checkers in '
                   'their initial positions on the board'
                   % self.checkers_to_setup]

        rtn.extend(['prepare the checkers board',
                    'get the chess board ready for a game of checkers',
                    'setup the checkers board', 'setup checkers',
                    'arrange the checkers ready for a game',
                    'get checkers ready'])

        return rtn

    # ADDED
    def reward(self) -> float:
        success = float(self.success()[0])  # Important to force NothingGrasped
        new_checkers_setup = 0
        total_target_distance = 0
        arm_to_checker_distance = 0

        for i, ti in enumerate(self.target_indexes):
            setup = self.success_conditions[1 + ti].condition_met()[0]
            if not setup:
                checker_pos = self.target_checkers[i].get_position()

                target_pos = self.target_pos_list[i]
                total_target_distance += \
                    np.linalg.norm(checker_pos - target_pos)

                if arm_to_checker_distance == 0:
                    # First not setup checker
                    arm_pos = self.robot.arm.get_tip().get_position()
                    arm_to_checker_distance = \
                        np.linalg.norm(arm_pos - checker_pos)
            else:
                if not self.checkers_setup[i]:
                    self.checkers_setup[i] = True
                    new_checkers_setup += 1

        return 10 * success \
               + new_checkers_setup \
               - 0.01 * (total_target_distance
                         + arm_to_checker_distance)

    def variation_count(self) -> int:
        return MAX_CHECKERS_TO_SETUP

    def cleanup(self) -> None:
        self.checkers_placed = -1
        for i, checker in enumerate(self.checkers):
            checker.set_position(self.checkers_starting_pos_list[i],
                                 self.chess_board)
            checker.set_orientation(self.checkers_starting_orientation,
                                    self.chess_board)

    def _move_above_next_target(self, waypoint):
        self.checkers_placed += 1
        self.target_index = self.target_indexes[self.checkers_placed]

        if self.checkers_placed > self.checkers_to_setup:
            raise RuntimeError('Should not be here')

        w1 = Dummy('waypoint1')
        # self.w2.set_parent(target_checkers[self.checkers_placed]

        unplaced_x, unplaced_y, unplaced_z = self.target_checkers[
            self.checkers_placed].get_position()

        z_offset_pickup = 0

        w1.set_position([unplaced_x, unplaced_y, unplaced_z - z_offset_pickup],
                        reset_dynamics=False)

        w4 = Dummy('waypoint4')

        target_x, target_y, target_z = self.checkers_starting_pos_list[
            self.target_index]
        z_offset_placement = 1.00 * 10 ** (-3)

        w4.set_position([target_x - z_offset_placement, target_y, target_z],
                        relative_to=self.chess_board, reset_dynamics=False)

        if self.checkers_to_setup > 1:
            if self.target_index == self.target_indexes[0]:
                self.target_index = self.target_indexes[1]
            if self.target_index == self.target_indexes[1] \
                    and self.checkers_to_setup == 3:
                self.target_index = self.target_indexes[2]

    def _repeat(self):
        return self.checkers_placed + 1 < self.checkers_to_setup





# from typing import List
# import numpy as np
# from pyrep.objects.proximity_sensor import ProximitySensor
# from pyrep.objects.shape import Shape
# from pyrep.objects.dummy import Dummy
# from rlbench.backend.task import Task
# from rlbench.backend.conditions import DetectedCondition, NothingGrasped
# from rlbench.backend.waypoints import Point

# MAX_CHECKERS_TO_SETUP = 3


# class SetupCheckers(Task):

#     def init_task(self) -> None:
#         self.checkers_placed = -1
#         self.checkers = [Shape('checker%d' % i)
#                          for i in range(24)]
        
        
#         self.chess_board = Shape('chess_board_base')


#         # Getting Initial Positions of Checkers
#         self.checkers_starting_pos_list = [
#             checker.get_position(self.chess_board) for checker in self.checkers]

#         # Define initial positions beside the board
#         # start_x = +0.007  # Adjust based on your scene
#         # start_y = +0.01  # Position behind or beside the board
#         # start_z = self.chess_board.get_position()[2] + 0.01
        
#         # self.checkers_starting_pos_list = []
#         # for i, checker in enumerate(self.checkers):
#         #     x_offset = (i % 6) * 0.035  # Spread checkers in a row
#         #     y_offset = (i // 6) * 0.035  # Stack checkers in rows
        
#         #     pos = [start_x + x_offset, start_y + y_offset, start_z]
#         #     self.checkers_starting_pos_list.append(pos)
        
#         #     # Move checkers to these positions immediately
#         #     checker.set_position(pos, relative_to=self.chess_board, reset_dynamics=True)
#         #     checker.set_dynamic(True)
        
#         #     print(f"Checker {i} placed at: {pos}")  # Debugging print

#         self.checkers_starting_orientation = \
#             self.checkers[0].get_orientation(self.chess_board)
        
#         # print out the position for all checkers to debug
#         for i, checker in enumerate(self.checkers):
#             pos = checker.get_position()
#             print(f"checker {i} position: {pos}")

#         # add the checkers to the graspable set
#         self.register_graspable_objects(self.checkers)
#         self.success_detectors = [ProximitySensor('detector%d' % i)
#                                   for i in range(24)]
#         self.success_conditions = [NothingGrasped(self.robot.gripper)]
#         for i in range(len(self.checkers)):
#             self.success_conditions.append(
#                 DetectedCondition(self.checkers[i], self.success_detectors[i]))

#         self.register_success_conditions(self.success_conditions)
        
#         self.cleanup()

#     def init_episode(self, index: int) -> List[str]:
#         self.cleanup()
      
#         self.checkers_to_setup = 1 + index % MAX_CHECKERS_TO_SETUP

#         ## Use to showcase episode variations while rlbench backend gets fixed:

#         self.register_waypoint_ability_start(0, self._move_above_next_target)
#         self.register_waypoints_should_repeat(self._repeat)

#         # Selecting Random Checkers to Move
#         target_checkers_unordered = np.random.choice(self.checkers,
#                                                      self.checkers_to_setup,
#                                                      replace=False)
#         self.target_indexes = []
#         self.target_checkers = []
#         for checker in self.checkers:
#             if checker in target_checkers_unordered:
#                 self.target_checkers.append(checker)

#         self.target_pos_list = []

#         # Setting New Positions for Checkers
#         pos_delta = 0.045
#         start_pos_list = [+0.0070816, +0.31868, -0.094908]

#         for i, checker in enumerate(self.checkers):
#             if checker in self.target_checkers:
#                 self.target_indexes.append(i)
#                 self.target_pos_list = checker.get_position()
                
#                 # update the reset_dynamics from false to true 
#                 checker.set_position(start_pos_list,
#                                      relative_to=self.chess_board,
#                                      reset_dynamics=False) 
#                 start_pos_list[2] += pos_delta


#         # perform the pick-up and placement actions for the selected checkers
#         for checker in self.target_checkers:
#             self._pick_up_checker(checker)
#             self._place_checker(checker)
            
#         if self.checkers_to_setup == 1:
#             rtn = ['place the remaining checker '
#                    'in its initial position on the board']
#         else:
#             rtn = ['place the %d remaining checkers in '
#                    'their initial positions on the board'
#                    % self.checkers_to_setup]

#         rtn.extend(['prepare the checkers board',
#                     'get the chess board ready for a game of checkers',
#                     'setup the checkers board', 'setup checkers',
#                     'arrange the checkers ready for a game',
#                     'get checkers ready'])

#         return rtn

#     def variation_count(self) -> int:
#         return MAX_CHECKERS_TO_SETUP

#     def cleanup(self) -> None:
#         self.checkers_placed = -1
#         for i, checker in enumerate(self.checkers):
#             checker.set_position(self.checkers_starting_pos_list[i],
#                                  self.chess_board)
#             checker.set_orientation(self.checkers_starting_orientation,
#                                     self.chess_board)

#     def _move_above_next_target(self, waypoint):
#         self.checkers_placed += 1
#         self.target_index = self.target_indexes[self.checkers_placed]

#         if self.checkers_placed > self.checkers_to_setup:
#             raise RuntimeError('Should not be here')

#         w1 = Dummy('waypoint1')
#         # self.w2.set_parent(target_checkers[self.checkers_placed]

#         unplaced_x, unplaced_y, unplaced_z = self.target_checkers[
#             self.checkers_placed].get_position()

#         z_offset_pickup = 0

#         w1.set_position([unplaced_x, unplaced_y, unplaced_z - z_offset_pickup],
#                         reset_dynamics=False)

#         w4 = Dummy('waypoint4')

#         target_x, target_y, target_z = self.checkers_starting_pos_list[
#             self.target_index]
#         z_offset_placement = 1.00 * 10 ** (-3)

#         w4.set_position([target_x - z_offset_placement, target_y, target_z],
#                         relative_to=self.chess_board, reset_dynamics=False)
#         # w4.set_position([target_x, target_y, target_z], relative_to = self.chess_board, reset_dynamics = False)

#         if self.checkers_to_setup > 1:
#             if self.target_index == self.target_indexes[0]:
#                 self.target_index = self.target_indexes[1]
#             if self.target_index == self.target_indexes[1] \
#                     and self.checkers_to_setup == 3:
#                 self.target_index = self.target_indexes[2]

#     # add code to pick up and place the checkers
#     def _pick_up_checker(self, checker):
#         """Move the arm to the checker and pick it up."""
#         # Get the current position of the checker and move the arm above it
#         checker_pos = checker.get_position()
    
#         # Create a Dummy object at the position of the checker
#         waypoint_object = Dummy.create()
#         waypoint_object.set_position(checker_pos)
    
#         # Create a waypoint using the Dummy object (not the robot)
#         waypoint = Point(self.robot, waypoint_object, checker_pos)
    
#         # Get the path to the target position using the waypoint
#         path = waypoint.get_path()
    
#         # The robot arm will automatically move along the path by executing this command
#         path.execute()
    
#         # Close the gripper to pick up the checker
#         self.robot.gripper.close()
    
#         # Allow time for the gripper to close
#         time.sleep(0.5)
        
#     def _place_checker(self, checker):
#         """Place the checker at the target position."""
#         # Get the target position where the checker should be placed
#         target_position = self.checkers_starting_pos_list[self.target_indexes[self.checkers_placed]]

#          # Create a Dummy object at the position of the checker
#         waypoint_object = Dummy.create()
#         waypoint_object.set_position(target_position)
        
#         # Create a waypoint object for the target position
#         waypoint = Point(self.robot, self.robot.arm, target_position)
    
#         # Get the path to the target position using the waypoint
#         path = waypoint.get_path()
    
#         # The robot arm will automatically move along the path by executing this command
#         # This assumes RLBench or PyRep internally handles moving the arm via configuration path
#         path.execute()
    
#         # Open the gripper to release the checker
#         self.robot.gripper.open()
    
#         # Allow time for the gripper to open
#         time.sleep(0.5)

#     def _repeat(self):
#         return self.checkers_placed + 1 < self.checkers_to_setup
