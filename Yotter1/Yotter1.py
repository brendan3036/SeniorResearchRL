from tools import  *
from objects import *
from routines import *


# Naive approach rule-set: centered in goal, attempts to rush ball or save any direction
# If nothing in stack: wait centered in goal
#   If ball less than 4032 units from our net, rush ball
#       else: Wait

#This file is for strategy

class Yotter1(GoslingAgent):
    def run(agent):
        # Variables for distance from ball to our goal
        my_goal_to_ball,ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        # Distance from our car to our goal
        goal_to_me = agent.me.location - agent.friend_goal.location
        # Dot product of distance from ball to our goal and goal to us
        my_distance = my_goal_to_ball.dot(goal_to_me)

        # Variable for which team touched the ball last (0 for blue, 1 for orange)
        ball_last_touched = agent.ball.latest_touched_team

        # Variable for magnitude of distance between agent's goal and ball
        distance_net_to_ball = abs(agent.friend_goal.location.y - agent.ball.location.y)
    
        if agent.team == 0:
            # This line will show the current routine on the in-game UI
            agent.debug_stack()
            # These lines are again just for visual debugging reasons
            agent.line(agent.friend_goal.location, agent.ball.location, [255,255,255])
            my_point = agent.friend_goal.location + (my_goal_to_ball * my_distance)
            agent.line(my_point - Vector3(0,0,100), my_point + Vector3(0,0,100), [0,255,0])
            
        if len(agent.stack) < 1:
            # At the beginning of our testing, go for kickoff (optional)
            if agent.kickoff_flag:
                agent.push(kickoff())
            # If agent has just saved the ball, it may go for boost until I do the next test shot
            elif ball_last_touched == 0:
                hitting_ball = False
                # Sets boosts to a list of boosts that are in order of closeness to our goal
                boosts = [boost for boost in agent.boosts if boost.large and boost.active and abs(agent.friend_goal.location.y - boost.location.y) - 200 < abs(agent.friend_goal.location.y - agent.me.location.y)]
                if len(boosts) > 0:
                    closest = boosts[0]
                    # We want the agent to go for the closest boost
                    for boost in boosts:
                            if (boost.location - agent.me.location).magnitude() < (closest.location - agent.me.location).magnitude():
                                closest = boost
                    agent.push(goto_boost(closest, agent.friend_goal.location))
            # If the ball is too close, go and save it!
            elif (distance_net_to_ball - 200) < 4032:
                # Declare left and right field as bounds for where the "upfield" hit will aim at
                left_field = Vector3(4200 * -side(agent.team), agent.ball.location.y + (1000 * -side(agent.team)), 0)
                right_field = Vector3(4200 * side(agent.team), agent.ball.location.y + (1000 * side(agent.team)), 0)
                targets = {"goal":(agent.foe_goal.left_post, agent.foe_goal.right_post), "upfield": (left_field,right_field)}
                shots = find_hits(agent, targets)
                # If we have no shots ready, push a shot to the stack
                if len(shots["goal"]) > 0:
                    agent.push(shots["goal"][0])
                # If there's no upfield hit in stack and the ball is less than X units (about less than halffield) away from goal:
                elif len(shots["upfield"]) > 0 and distance_net_to_ball < 8490:
                    agent.push(shots["upfield"][0])
            else:
                # Go to the center of the goal
                agent.push(goto(Vector3(0, -1 * 5100, 320)))
    

                
    

                


                    
                


        
            


        
        
