from tools import  *
from objects import *
from routines import *

n = 0
totalDistance = 0
averageDistance = 10000
#  'Mirroring' strategy
#  After kickoff, get boost if applicable 
#  Then mirror the attacking ball's movement
#  Keep track of the distance to the opposing car, if it goes above what we're used to seeing then attack

class Yotter3(GoslingAgent):
    def run(agent):
        # n will keep track of our game ticks in the loop where attacker has ball control
        global n
        # totalDistance and averageDistance allow us to keep track of avg distance between attacker and ball
        global totalDistance
        global averageDistance

        # Variables for distance from ball to our goal
        my_goal_to_ball,ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        # Distance from our car to our goal
        goal_to_me = agent.me.location - agent.friend_goal.location
        # Dot product of distance from ball to our goal and goal to us
        my_distance = my_goal_to_ball.dot(goal_to_me)

        # Variable for which team touched the ball last (0 for blue, 1 for orange)
        ball_last_touched = agent.ball.latest_touched_team
        # Initialize boolean for whether attacker (me) is hitting the ball
        hitting_ball = False
        # Distance between agent's goal and ball
        distance_goal_to_ball = abs(agent.friend_goal.location.y - agent.ball.location.y)
        
        # Every tick we want the distance between opponent and ball
        currentOpponentToBall = (agent.foes[0].location - agent.ball.location).magnitude()
        
        # If the ball is last touched by opponent, start tracking the average distance between opponent and ball
        # every tick until we will try to save
        if ball_last_touched == 1:
            # Update n every game tick 
            n += 1
            totalDistance += currentOpponentToBall
            # Calculate averageDistance 
            averageDistance = totalDistance / n
        if ball_last_touched == 0:
            n = 0
            totalDistance = 0



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

            # If ball too close or gets more than 2x averageDistance away from attacking opponent, try to save it
            elif (distance_goal_to_ball-200 < 5000 and ball_last_touched == 1) or ((currentOpponentToBall > (averageDistance * 2) and ball_last_touched == 1 and distance_goal_to_ball-200 < 7000)):
                left_field = Vector3(4200 * -side(agent.team), agent.ball.location.y + (1000 * -side(agent.team)), 0)
                right_field = Vector3(4200 * side(agent.team), agent.ball.location.y + (1000 * side(agent.team)), 0)
                targets = {"upfield": (left_field,right_field), "goal":(agent.foe_goal.left_post, agent.foe_goal.right_post)}
                shots = find_hits(agent, targets)
                # Hopefully we have found a possible shot (i.e. save) to push to the stack
                if len(shots["goal"]) > 0:
                    hitting_ball = True
                    agent.push(shots["goal"][0])
                # If not possible, try to save the ball toward upfield
                elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                    agent.push(shots["upfield"][0])

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
        
            
            else: 
                # Mirror the attacker's x coordinate, but stay on y = 3000 (72 is default z height)
                agent.push(goto(Vector3(agent.foes[0].location.x, -3000, 72)))
                    
                    
                    

                

                
    

                


                    
                


        
            


        
        
