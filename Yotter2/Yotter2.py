from tools import  *
from objects import *
from routines import *


#  Save from corner strategy
#  After kickoff, go for boost then to either corner.
#  Tries to save the ball the best way possible but can also resort to saving across the net.
#  This file is for strategy

class Yotter2(GoslingAgent):
    def run(agent):
        # Variables for distance from ball to our goal
        my_goal_to_ball,ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        # Distance from our car to our goal
        goal_to_me = agent.me.location - agent.friend_goal.location
        # Dot product of distance from ball to our goal and goal to us
        my_distance = my_goal_to_ball.dot(goal_to_me)
        
        # Variable to keep track of which corner our agent is in, initialized false
        car_is_left_corner = False
        # Variable for which team touched the ball last (0 for blue, 1 for orange)
        ball_last_touched = agent.ball.latest_touched_team

        # Distances from our agent's X coordinate to each corner (2800 is X magnitude of corner)
        dist_to_left_corner = agent.me.location.x - 2800
        dist_to_right_corner = agent.me.location.x + 2800
        # Initialize boolean for whether attacker (me) is hitting the ball
        hitting_ball = False
        # Distance between agent's goal and ball
        distance_goal_to_ball = (agent.friend_goal.location - agent.ball.location).magnitude()
    
        # Target vectors for agent to hit a save across (default saves are aimed at goal or upfield)
        toLeft_left = Vector3(4096, -4096, 0)
        toLeft_right = Vector3(4096, 0, 0)
        toRight_right = Vector3(-4096, -4096, 0)
        toRight_left = Vector3(-4096, 0, 0)


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

            # If the ball gets close, hecking drive/boost at it and save it!
            elif (distance_goal_to_ball < 5500) and ball_last_touched == 1:
                left_field = Vector3(4200 * -side(agent.team), agent.ball.location.y + (2000 * -side(agent.team)), 0)
                right_field = Vector3(4200 * side(agent.team), agent.ball.location.y + (2000 * side(agent.team)), 0)
                if car_is_left_corner:
                    # Make right side a target
                    targets = {"across":(toRight_right, toRight_left), "upfield": (left_field,right_field), "goal":(agent.foe_goal.left_post, agent.foe_goal.right_post)}
                elif not car_is_left_corner:
                    # Make left side a target
                    targets = {"across":(toLeft_left, toLeft_right), "upfield": (left_field,right_field), "goal":(agent.foe_goal.left_post, agent.foe_goal.right_post)}
                shots = find_hits(agent, targets)
                # Hopefully we have found a possible shot (i.e. save) to push to the stack
                if len(shots["goal"]) > 0:
                    print("found shot")
                    hitting_ball = True
                    agent.push(shots["goal"][0])
                # Saves aimed at enemy goal are most ideal so we go for that first
                # If not possible, try to save the ball toward upfield
                elif len(shots["upfield"]) > 0:
                    agent.push(shots["upfield"][0])
                # If upfield save not possible, try to save it across
                elif len(shots["across"]) > 0:
                    agent.push(shots["across"][0])

            # If we just touched (saved) the ball, agent can go for boost
            elif ball_last_touched == 0:
                hitting_ball = False
                boosts = [boost for boost in agent.boosts if boost.large and boost.active and abs(agent.friend_goal.location.y - boost.location.y) - 200 < abs(agent.friend_goal.location.y - agent.me.location.y)]
                if len(boosts) > 0:
                    closest = boosts[0]
                    for boost in boosts:
                            if (boost.location - agent.me.location).magnitude() < (closest.location - agent.me.location).magnitude():
                                closest = boost
                    agent.push(goto_boost(closest, agent.friend_goal.location))
                else: agent.push(goto(Vector3(3072, -1 * 4096, 72)))

                    
            # If no other conditions are present, go to the closest corner
            elif abs(dist_to_left_corner) < abs(dist_to_right_corner) and hitting_ball == False:
                car_is_left_corner = True
                agent.push(goto(Vector3(2500, -1 * 4096, 72)))
            elif abs(dist_to_left_corner) > abs(dist_to_right_corner) and hitting_ball == False:
                car_is_left_corner = False
                agent.push(goto(Vector3(-2500, -1 * 4096, 72)))

                

                
    

                


                    
                


        
            


        
        
